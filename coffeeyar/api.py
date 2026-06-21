from __future__ import annotations

import re
import secrets
from typing import Any

import frappe
import requests
from frappe import _
from frappe.utils import cint, flt, get_url


PRODUCT_DOCTYPE = "Product"
CATEGORY_DOCTYPE = "Product Category"
VARIANT_DOCTYPE = "Product Variant"
ATTRIBUTE_DOCTYPE = "Product Attribute"
ATTRIBUTE_OPTION_DOCTYPE = "Product Attribute Option"
ORDER_DOCTYPE = "Order"
SETTINGS_DOCTYPE = "Store Settings"


def _to_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value or 0))
    except Exception:
        return default


def _slugify(text: str) -> str:
    value = "-".join((text or "").strip().lower().split())
    value = value.replace("_", "-")
    value = re.sub(r"[^a-z0-9\u0600-\u06FF-]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")


def _parse_json_payload(payload: bytes | str | dict[str, Any] | None) -> dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")
    if isinstance(payload, str) and payload.strip():
        return frappe.parse_json(payload)
    return {}


def _get_settings() -> frappe.model.document.Document:
    settings = frappe.get_single(SETTINGS_DOCTYPE)
    if not settings.get("shipping_fee_toman"):
        settings.shipping_fee_toman = 120000
    if not settings.zarinpal_request_url:
        settings.zarinpal_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    if not settings.zarinpal_verify_url:
        settings.zarinpal_verify_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    if not settings.zarinpal_startpay_url:
        settings.zarinpal_startpay_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    return settings


def _category_title(category_name: str | None) -> str:
    if not category_name:
        return ""
    return frappe.db.get_value(CATEGORY_DOCTYPE, category_name, "item_group_name") or ""


def _effective_price(price: Any, discount: Any) -> int:
    return max(_to_int(price) - max(0, _to_int(discount)), 0)


def _variant_price(variant: frappe.model.document.Document | frappe._dict, product: Any) -> tuple[int, int, int]:
    price = _to_int(variant.price_toman) or _to_int(product.price_toman)
    discount = max(0, _to_int(variant.discount_toman))
    if not discount:
        discount = max(0, _to_int(product.discount_toman))
    return price, discount, _effective_price(price, discount)


def _variant_attribute_value(row: Any) -> str:
    value = (getattr(row, "attribute_value", None) or "").strip()
    if value:
        return value
    value = (getattr(row, "option_title", None) or "").strip()
    if value:
        return value
    option = getattr(row, "option", None)
    if option and frappe.db.table_exists(ATTRIBUTE_OPTION_DOCTYPE):
        return frappe.db.get_value(ATTRIBUTE_OPTION_DOCTYPE, option, "title") or ""
    return ""


def _variant_attributes_payload(variant: frappe.model.document.Document) -> list[dict[str, Any]]:
    out = []
    for row in variant.attributes or []:
        value = _variant_attribute_value(row)
        title = row.attribute_title or frappe.db.get_value(ATTRIBUTE_DOCTYPE, row.attribute, "title") or row.attribute
        out.append(
            {
                "attribute": row.attribute,
                "attribute_title": title,
                "attribute_value": value,
                "option": getattr(row, "option", None),
                "option_title": getattr(row, "option_title", None) or value,
                "numeric_values": cint(getattr(row, "numeric_values", 0)),
            }
        )
    return out


def _variant_display_title(variant: frappe.model.document.Document) -> str:
    if variant.title:
        return variant.title
    values = [_variant_attribute_value(row) for row in variant.attributes or []]
    values = [value for value in values if value]
    return " / ".join(values) or variant.name


def _variant_payload(variant: frappe.model.document.Document, product: Any | None = None) -> dict[str, Any]:
    product = product or frappe.get_doc(PRODUCT_DOCTYPE, variant.product)
    price, discount, effective = _variant_price(variant, product)
    return {
        "name": variant.name,
        "product": variant.product,
        "title": _variant_display_title(variant),
        "sku": variant.sku,
        "image": variant.image or product.image,
        "price_toman": price,
        "discount_toman": discount,
        "effective_price_toman": effective,
        "stock_qty": _to_int(variant.stock_qty),
        "is_published": cint(variant.is_published),
        "attributes": _variant_attributes_payload(variant),
    }


def _get_variants(product_name: str) -> list[dict[str, Any]]:
    product = frappe.get_doc(PRODUCT_DOCTYPE, product_name)
    variants = frappe.get_all(
        VARIANT_DOCTYPE,
        filters={"product": product_name, "is_published": 1},
        fields=["name"],
        order_by="display_order asc, creation asc",
    )
    return [_variant_payload(frappe.get_doc(VARIANT_DOCTYPE, row.name), product) for row in variants]


def _product_variant_attributes(doc: frappe.model.document.Document) -> list[dict[str, Any]]:
    out = []
    for row in doc.attributes or []:
        if not row.attribute:
            continue
        attr = frappe.get_doc(ATTRIBUTE_DOCTYPE, row.attribute)
        item = {
            "attribute": attr.name,
            "title": attr.title,
            "slug": attr.slug,
            "numeric_values": cint(getattr(attr, "numeric_values", 0)),
            "from_range": flt(getattr(attr, "from_range", 0)),
            "to_range": flt(getattr(attr, "to_range", 0)),
            "increment": flt(getattr(attr, "increment", 0)),
            "values": [],
        }
        if not item["numeric_values"]:
            item["values"] = [
                {"value": (value.attribute_value or "").strip(), "abbr": (value.abbr or "").strip()}
                for value in (attr.attribute_values or [])
                if (value.attribute_value or "").strip()
            ]
        out.append(item)
    return out


def _safe_product_payload(doc: frappe.model.document.Document, include_variants: bool = True) -> dict[str, Any]:
    price = _to_int(doc.price_toman)
    discount = max(0, _to_int(doc.discount_toman))
    variants = _get_variants(doc.name) if include_variants else []
    effective = _effective_price(price, discount)
    if variants:
        effective = min(row["effective_price_toman"] for row in variants)
    return {
        "name": doc.name,
        "title": doc.item_name,
        "slug": doc.slug,
        "category": doc.item_group,
        "category_title": _category_title(doc.item_group),
        "short_description": doc.short_description,
        "description": doc.description,
        "price_toman": price,
        "discount_toman": discount,
        "effective_price_toman": effective,
        "stock_qty": _to_int(doc.stock_qty),
        "has_variants": cint(doc.has_variants) or bool(variants),
        "sku": doc.sku,
        "image": doc.image,
        "gallery_json": doc.gallery_json,
        "is_featured": cint(doc.is_featured),
        "is_published": cint(doc.is_published),
        "display_order": _to_int(doc.display_order),
        "variants": variants,
        "variant_attributes": _product_variant_attributes(doc) if cint(doc.has_variants) else [],
        "seo_title": doc.seo_title,
        "seo_description": doc.seo_description,
    }


def _group_names_for_slug(slug: str | None) -> list[str]:
    category_slug = (slug or "").strip()
    if not category_slug:
        return []

    group_name = frappe.db.get_value(CATEGORY_DOCTYPE, {"slug": category_slug}, "name")
    if not group_name:
        return []

    bounds = frappe.db.get_value(CATEGORY_DOCTYPE, group_name, ["lft", "rgt"])
    if not bounds:
        return [group_name]

    lft, rgt = bounds
    rows = frappe.get_all(
        CATEGORY_DOCTYPE,
        filters={
            "is_active": 1,
            "lft": [">=", lft],
            "rgt": ["<=", rgt],
        },
        pluck="name",
    )
    return rows or [group_name]


def _build_filter_conditions(filters: dict[str, Any]) -> dict[str, Any]:
    conditions: dict[str, Any] = {"is_published": 1}
    if filters.get("category"):
        conditions["item_group"] = filters.get("category")
    if filters.get("category_slug"):
        names = _group_names_for_slug(filters.get("category_slug"))
        conditions["item_group"] = ["in", names] if names else "__missing__"
    if filters.get("in_stock"):
        conditions["stock_qty"] = [">", 0]
    if filters.get("featured"):
        conditions["is_featured"] = 1
    if filters.get("slug"):
        conditions["slug"] = filters.get("slug")
    return conditions


@frappe.whitelist(allow_guest=True)
def list_products(filters: str | dict[str, Any] | None = None, sort: str | None = None, page: int | str = 1):
    payload_filters = _parse_json_payload(filters)
    page_no = max(_to_int(page, 1), 1)
    page_size = _to_int(payload_filters.get("page_size"), 24) if payload_filters.get("page_size") else 24
    page_size = max(min(page_size, 100), 1)
    start = (page_no - 1) * page_size

    order_by = "display_order asc, creation desc"
    if sort == "price_asc":
        order_by = "price_toman asc"
    elif sort == "price_desc":
        order_by = "price_toman desc"
    elif sort == "newest":
        order_by = "creation desc"

    conditions = _build_filter_conditions(payload_filters)
    docs = frappe.get_all(
        PRODUCT_DOCTYPE,
        filters=conditions,
        fields=[
            "name",
            "item_name",
            "slug",
            "item_group",
            "short_description",
            "price_toman",
            "discount_toman",
            "stock_qty",
            "has_variants",
            "image",
            "display_order",
            "is_featured",
            "is_published",
        ],
        order_by=order_by,
        limit_start=start,
        limit=page_size,
    )

    total = frappe.db.count(PRODUCT_DOCTYPE, filters=conditions)
    out = []
    for row in docs:
        price = _to_int(row.price_toman)
        discount = max(0, _to_int(row.discount_toman))
        out.append(
            {
                "name": row.name,
                "title": row.item_name,
                "slug": row.slug,
                "category": row.item_group,
                "category_title": _category_title(row.item_group),
                "short_description": row.short_description,
                "price_toman": price,
                "discount_toman": discount,
                "effective_price_toman": _effective_price(price, discount),
                "stock_qty": _to_int(row.stock_qty),
                "has_variants": cint(row.has_variants),
                "image": row.image,
            }
        )

    return {
        "items": out,
        "page": page_no,
        "page_size": page_size,
        "total": total,
        "has_next": (start + page_size) < total,
    }


@frappe.whitelist(allow_guest=True)
def get_product(slug: str):
    if not slug:
        frappe.throw(_("Product slug is required"))

    name = frappe.db.get_value(PRODUCT_DOCTYPE, {"slug": slug, "is_published": 1}, "name")
    if not name:
        frappe.throw(_("Product not found"), frappe.DoesNotExistError)

    doc = frappe.get_doc(PRODUCT_DOCTYPE, name)
    return _safe_product_payload(doc)


@frappe.whitelist(allow_guest=True)
def list_product_variants(product: str | None = None, slug: str | None = None):
    product_name = product
    if slug:
        product_name = frappe.db.get_value(PRODUCT_DOCTYPE, {"slug": slug, "is_published": 1}, "name")
    if not product_name:
        frappe.throw(_("Product is required"))
    return _get_variants(product_name)


@frappe.whitelist(allow_guest=True)
def list_attributes():
    attrs = frappe.get_all(
        ATTRIBUTE_DOCTYPE,
        filters={"is_active": 1, "disabled": 0},
        fields=["name", "title", "slug", "display_order", "is_filterable", "numeric_values"],
        order_by="display_order asc, creation asc",
    )
    for attr in attrs:
        doc = frappe.get_doc(ATTRIBUTE_DOCTYPE, attr.name)
        if cint(getattr(doc, "numeric_values", 0)):
            attr["options"] = []
            attr["numeric_range"] = {
                "from_range": doc.from_range,
                "to_range": doc.to_range,
                "increment": doc.increment,
            }
            continue

        attr["options"] = [
            {
                "name": value.name,
                "title": value.attribute_value,
                "slug": _slugify(value.attribute_value),
                "abbr": value.abbr,
                "display_order": value.idx,
            }
            for value in (doc.attribute_values or [])
        ]

        if not attr["options"] and frappe.db.table_exists(ATTRIBUTE_OPTION_DOCTYPE):
            attr["options"] = frappe.get_all(
                ATTRIBUTE_OPTION_DOCTYPE,
                filters={"attribute": attr.name, "is_active": 1},
                fields=["name", "title", "slug", "display_order"],
                order_by="display_order asc, creation asc",
            )
    return attrs


def _resolve_order_item(raw_item: dict[str, Any]) -> dict[str, Any]:
    product_slug = _slugify(raw_item.get("product_slug") or raw_item.get("slug") or "")
    qty = max(_to_int(raw_item.get("qty"), 1), 1)
    variant_id = (raw_item.get("variant_id") or raw_item.get("variant") or "").strip()

    product_name = frappe.db.get_value(PRODUCT_DOCTYPE, {"slug": product_slug, "is_published": 1}, "name")
    if not product_name:
        frappe.throw(_("Product {0} not found").format(product_slug))

    product = frappe.get_doc(PRODUCT_DOCTYPE, product_name)
    variant = None
    if cint(product.has_variants):
        if not variant_id:
            frappe.throw(_("Please select a variant for {0}").format(product.item_name))
        variant_name = frappe.db.get_value(
            VARIANT_DOCTYPE,
            {"name": variant_id, "product": product.name, "is_published": 1},
            "name",
        )
        if not variant_name:
            frappe.throw(_("Invalid variant for {0}").format(product.item_name))
        variant = frappe.get_doc(VARIANT_DOCTYPE, variant_name)
        if cint(variant.stock_qty) < qty:
            frappe.throw(_("Insufficient stock for {0}").format(variant.title))
        _price, _discount, unit_price = _variant_price(variant, product)
        variant_title = variant.title
    else:
        if cint(product.stock_qty) < qty:
            frappe.throw(_("Insufficient stock for {0}").format(product.item_name))
        unit_price = _effective_price(product.price_toman, product.discount_toman)
        variant_title = ""

    return {
        "product": product.name,
        "variant": variant.name if variant else None,
        "product_slug": product.slug,
        "product_title": product.item_name,
        "variant_title": variant_title,
        "qty": qty,
        "unit_price_toman": unit_price,
        "row_total_toman": unit_price * qty,
    }


@frappe.whitelist(allow_guest=True, methods=["POST"])
def create_order(payload: str | dict[str, Any] | None = None):
    data = _parse_json_payload(payload)

    customer_name = (data.get("customer_name") or "").strip()
    mobile = (data.get("mobile") or "").strip()
    notes = (data.get("notes") or "").strip()
    shipping_address = (data.get("shipping_address") or "").strip()
    items = data.get("items") or []

    if not customer_name:
        frappe.throw(_("Customer name is required"))
    if not mobile or len(mobile) < 10:
        frappe.throw(_("Valid mobile number is required"))
    if not isinstance(items, list) or not items:
        frappe.throw(_("At least one item is required"))

    settings = _get_settings()
    shipping_fee = max(0, _to_int(settings.shipping_fee_toman))

    order_items = [_resolve_order_item(raw_item) for raw_item in items]
    subtotal = sum(item["row_total_toman"] for item in order_items)
    total = subtotal + shipping_fee
    public_token = secrets.token_urlsafe(24)

    order_doc = frappe.get_doc(
        {
            "doctype": ORDER_DOCTYPE,
            "customer_name": customer_name,
            "mobile": mobile,
            "notes": notes,
            "shipping_address": shipping_address,
            "subtotal_toman": subtotal,
            "shipping_fee_toman": shipping_fee,
            "total_toman": total,
            "order_status": "Pending Payment",
            "payment_status": "Pending",
            "public_token": public_token,
            "items": order_items,
        }
    )
    order_doc.insert(ignore_permissions=True)

    return {
        "order_id": order_doc.name,
        "order_status": order_doc.order_status,
        "payment_status": order_doc.payment_status,
        "total_toman": total,
        "public_token": public_token,
    }


def _zarin_headers() -> dict[str, str]:
    return {"Content-Type": "application/json", "Accept": "application/json"}


def _make_payment_callback(order_id: str) -> str:
    return get_url(f"/payment/callback?order_id={order_id}")


@frappe.whitelist(allow_guest=True, methods=["POST"])
def start_payment(order_id: str, order_token: str | None = None):
    if not order_id:
        frappe.throw(_("Order ID is required"))

    order = frappe.get_doc(ORDER_DOCTYPE, order_id)
    if order_token and order.public_token and order_token != order.public_token:
        frappe.throw(_("Invalid order token"))

    if order.payment_status == "Paid":
        frappe.throw(_("Order already paid"))

    settings = _get_settings()
    merchant_id = (settings.zarinpal_merchant_id or "").strip()
    if not merchant_id:
        frappe.throw(_("Zarinpal merchant ID is not configured"))

    payload = {
        "merchant_id": merchant_id,
        "amount": _to_int(order.total_toman),
        "callback_url": _make_payment_callback(order.name),
        "description": f"Store Order {order.name}",
        "metadata": {"mobile": order.mobile},
    }

    response = requests.post(settings.zarinpal_request_url, json=payload, headers=_zarin_headers(), timeout=20)
    response.raise_for_status()
    body = response.json() or {}
    data = body.get("data") or {}
    errors = body.get("errors") or {}

    if data.get("code") not in (100, 101):
        frappe.throw(_("Payment request failed: {0}").format(errors or data))

    authority = data.get("authority")
    if not authority:
        frappe.throw(_("Payment authority not returned"))

    order.payment_authority = authority
    order.order_status = "Pending Payment"
    order.payment_status = "Pending"
    order.save(ignore_permissions=True)

    startpay = (settings.zarinpal_startpay_url or "https://sandbox.zarinpal.com/pg/StartPay/").rstrip("/")
    return {"order_id": order.name, "authority": authority, "payment_url": f"{startpay}/{authority}"}


@frappe.whitelist(allow_guest=True, methods=["POST"])
def verify_payment(order_id: str, authority: str | None = None, status: str | None = None):
    if not order_id:
        frappe.throw(_("Order ID is required"))

    order = frappe.get_doc(ORDER_DOCTYPE, order_id)
    incoming_authority = (authority or "").strip() or (frappe.form_dict.get("Authority") or "").strip()
    incoming_status = (status or "").strip() or (frappe.form_dict.get("Status") or "").strip()

    if not incoming_authority:
        order.payment_status = "Failed"
        order.order_status = "Payment Failed"
        order.save(ignore_permissions=True)
        return {"ok": False, "status": "Payment Failed", "message": "Missing authority"}

    if incoming_status and incoming_status.lower() != "ok":
        order.payment_status = "Failed"
        order.order_status = "Payment Failed"
        order.payment_authority = incoming_authority
        order.save(ignore_permissions=True)
        return {"ok": False, "status": "Payment Failed", "message": "Payment cancelled by user"}

    settings = _get_settings()
    merchant_id = (settings.zarinpal_merchant_id or "").strip()
    if not merchant_id:
        frappe.throw(_("Zarinpal merchant ID is not configured"))

    payload = {
        "merchant_id": merchant_id,
        "amount": _to_int(order.total_toman),
        "authority": incoming_authority,
    }
    response = requests.post(settings.zarinpal_verify_url, json=payload, headers=_zarin_headers(), timeout=20)
    response.raise_for_status()
    body = response.json() or {}
    data = body.get("data") or {}

    code = cint(data.get("code"))
    if code not in (100, 101):
        order.payment_status = "Failed"
        order.order_status = "Payment Failed"
        order.payment_authority = incoming_authority
        order.payment_response_json = frappe.as_json(body)
        order.save(ignore_permissions=True)
        return {"ok": False, "status": "Payment Failed", "message": "Verification failed", "code": code}

    order.payment_status = "Paid"
    order.order_status = "Paid"
    order.payment_authority = incoming_authority
    order.payment_ref_id = str(data.get("ref_id") or "")
    order.payment_response_json = frappe.as_json(body)
    order.save(ignore_permissions=True)

    _apply_stock_deduction(order)
    return {"ok": True, "status": "Paid", "order_id": order.name, "ref_id": order.payment_ref_id}


def _apply_stock_deduction(order: frappe.model.document.Document):
    for item in order.items or []:
        if cint(item.qty) <= 0:
            continue
        if item.variant:
            frappe.db.sql(
                """
                UPDATE `tabProduct Variant`
                SET stock_qty = GREATEST(COALESCE(stock_qty, 0) - %(qty)s, 0)
                WHERE name = %(name)s
                """,
                {"qty": cint(item.qty), "name": item.variant},
            )
        elif item.product:
            frappe.db.sql(
                """
                UPDATE `tabProduct`
                SET stock_qty = GREATEST(COALESCE(stock_qty, 0) - %(qty)s, 0)
                WHERE name = %(name)s
                """,
                {"qty": cint(item.qty), "name": item.product},
            )


@frappe.whitelist(allow_guest=True)
def list_categories():
    rows = frappe.get_all(
        CATEGORY_DOCTYPE,
        filters={"is_active": 1, "is_group": 0},
        fields=["name", "item_group_name", "slug", "image", "description", "display_order", "parent_item_group"],
        order_by="display_order asc, creation asc",
    )
    return [
        {
            "name": row.name,
            "title": row.item_group_name,
            "slug": row.slug,
            "image": row.image,
            "description": row.description,
            "display_order": row.display_order,
            "parent_item_group": row.parent_item_group,
        }
        for row in rows
    ]


@frappe.whitelist(allow_guest=True)
def get_site_page(slug: str = "home"):
    name = frappe.db.get_value("Site Page", {"slug": slug, "is_published": 1}, "name")
    if not name:
        frappe.throw(_("Page not found"), frappe.DoesNotExistError)
    doc = frappe.get_doc("Site Page", name)
    return {
        "name": doc.name,
        "title": doc.title,
        "slug": doc.slug,
        "page_type": doc.page_type,
        "hero_title": doc.hero_title,
        "hero_subtitle": doc.hero_subtitle,
        "hero_image": doc.hero_image,
        "body_html": doc.body_html,
        "featured_category": doc.featured_category,
        "seo_title": doc.seo_title,
        "seo_description": doc.seo_description,
    }


@frappe.whitelist(allow_guest=True)
def list_blog_posts(page: int | str = 1, page_size: int | str = 12):
    page_no = max(_to_int(page, 1), 1)
    size = max(min(_to_int(page_size, 12), 50), 1)
    start = (page_no - 1) * size
    filters = {"is_published": 1}
    rows = frappe.get_all(
        "Blog Post",
        filters=filters,
        fields=["name", "title", "slug", "cover_image", "excerpt", "published_on", "display_order"],
        order_by="display_order asc, published_on desc, creation desc",
        limit_start=start,
        limit=size,
    )
    total = frappe.db.count("Blog Post", filters=filters)
    return {"items": rows, "page": page_no, "page_size": size, "total": total, "has_next": start + size < total}


@frappe.whitelist(allow_guest=True)
def get_blog_post(slug: str):
    name = frappe.db.get_value("Blog Post", {"slug": slug, "is_published": 1}, "name")
    if not name:
        frappe.throw(_("Blog post not found"), frappe.DoesNotExistError)
    doc = frappe.get_doc("Blog Post", name)
    return {
        "name": doc.name,
        "title": doc.title,
        "slug": doc.slug,
        "cover_image": doc.cover_image,
        "excerpt": doc.excerpt,
        "content": doc.content,
        "published_on": doc.published_on,
        "seo_title": doc.seo_title,
        "seo_description": doc.seo_description,
    }


@frappe.whitelist(allow_guest=True)
def get_navigation():
    rows = frappe.get_all(
        "Navigation Link",
        filters={"is_active": 1},
        fields=["label", "route", "placement", "display_order"],
        order_by="display_order asc, creation asc",
    )
    out = {"header": [], "footer": [], "mobile": []}
    for row in rows:
        key = (row.placement or "").lower()
        if key in out:
            out[key].append({"label": row.label, "to": row.route})
    return out


def before_request_api():
    """Registered as a before_request hook.
    Strips the Authorization header for /_api/ routes so Frappe's validate_auth()
    doesn't raise an HTML 401 error page for our custom Bearer tokens.
    The token is saved to frappe.local._custom_api_token for later use
    by _resolve_user_from_token() in api_router.py.
    """
    path = getattr(frappe.local, "request", None)
    if path is None:
        return
    if not frappe.local.request.path.startswith("/_api/"):
        return
    auth = frappe.get_request_header("Authorization", "")
    if auth.lower().startswith("bearer "):
        frappe.local._custom_api_token = auth[7:]
        frappe.request.environ.pop("HTTP_AUTHORIZATION", None)


from frappe.website.page_renderers.base_renderer import BaseRenderer
from werkzeug.wrappers import Response as WerkzeugResponse


class ApiRenderer(BaseRenderer):
    """Custom page renderer for the 'api_handler' endpoint.
    Registered via the page_renderer hook.
    """

    def can_render(self):
        return self.path == "api_handler"

    def render(self):
        from coffeeyar.api_router import handle_request

        result = handle_request()
        status_code = getattr(frappe.local.response, "http_status_code", 200)
        return WerkzeugResponse(
            frappe.as_json(result),
            status=status_code,
            content_type="application/json; charset=utf-8",
        )
