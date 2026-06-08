from __future__ import annotations

import json
import re
from typing import Any

import frappe
from frappe import _

from coffeeyar.api import (
    _category_title,
    _effective_price,
    _get_settings,
    _parse_json_payload,
    _slugify,
    _to_int,
    _variant_price,
    CATEGORY_DOCTYPE,
)


def handle_request():
    path = frappe.local.request.path
    method = frappe.request.method
    body = frappe.request.data or "{}"
    payload = _parse_json_payload(body)

    route = path.rstrip("/")
    route = re.sub(r"^/api/", "", route)
    segments = route.split("/") if route else []
    segment_count = len(segments)

    try:
        if not segments:
            return _json({"error": "Not found"}, 404)

        resource = segments[0]

        # ── Auth ──
        if resource == "auth" and method == "POST":
            if segment_count >= 2 and segments[1] == "register":
                return _handle_auth_register(payload)
            if segment_count >= 2 and segments[1] == "login":
                return _handle_auth_login(payload)
        if resource == "auth" and method == "GET" and segment_count >= 2 and segments[1] == "me":
            return _handle_auth_me()
        if resource == "auth" and method == "PUT" and segment_count >= 2 and segments[1] == "me":
            return _handle_auth_update(payload)

        # ── Categories ──
        if resource == "categories" and method == "GET":
            return _handle_list_categories()

        # ── Products ──
        if resource == "products" and method == "GET":
            if segment_count >= 2:
                slug = segments[1]
                if segment_count >= 3 and segments[2] == "faqs":
                    return _handle_product_faqs(slug)
                return _handle_get_product(slug)
            return _handle_list_products(frappe.request.args)

        # ── Reviews ──
        if resource == "reviews":
            if method == "GET" and segment_count >= 2:
                return _handle_list_reviews(segments[1])
            if method == "POST":
                return _handle_create_review(payload)

        # ── Wishlist ──
        if resource == "wishlist" and method == "POST" and segment_count >= 2:
            return _handle_wishlist_toggle(segments[1])
        if resource == "wishlist" and method == "GET":
            if segment_count >= 2 and segments[1] == "ids":
                return _handle_wishlist_ids()
            return _handle_wishlist_list()

        # ── Coupons ──
        if resource == "coupons" and method == "POST" and segment_count >= 2 and segments[1] == "validate":
            return _handle_coupon_validate(payload)

        # ── Orders ──
        if resource == "orders" and method == "POST":
            return _handle_create_order(payload)
        if resource == "orders" and method == "GET":
            if segment_count >= 2:
                return _handle_get_order(segments[1])
            return _handle_list_orders()

        # ── Returns ──
        if resource == "returns":
            if method == "POST":
                return _handle_create_return(payload)
            if method == "GET":
                return _handle_list_returns()

        # ── FAQ ──
        if resource == "faq" and method == "GET":
            return _handle_list_faq()

        # ── Blog ──
        if resource == "blog" and method == "GET":
            if segment_count >= 2:
                return _handle_get_blog_post(segments[1])
            return _handle_list_blog_posts(frappe.request.args)

        # ── Public content / policies / theme ──
        if resource == "content" and method == "GET":
            return _handle_public_content()
        if resource == "policies" and method == "GET":
            return _handle_public_policies()
        if resource == "product-global-faqs" and method == "GET":
            return _handle_public_product_global_faqs()

        # ── Site ──
        if resource == "site-settings" and method == "GET":
            return _handle_site_settings()
        if resource == "navigation" and method == "GET":
            return _handle_navigation()

        # ── Addresses ──
        if resource == "addresses":
            if method == "GET":
                return _handle_list_addresses()
            if method == "POST":
                return _handle_create_address(payload)
            if method == "DELETE" and segment_count >= 2:
                return _handle_delete_address(segments[1])

        # ── Admin ──
        if resource == "admin" and segment_count >= 2:
            return _handle_admin(segments[1:], method, payload, frappe.request.args)

        return _json({"error": "Not found"}, 404)

    except frappe.DoesNotExistError as e:
        return _json({"error": str(e) or "Not found"}, 404)
    except frappe.ValidationError as e:
        return _json({"error": str(e)}, 422)
    except Exception as e:
        frappe.log_error(f"API Router Error: {e}")
        return _json({"error": "Internal server error"}, 500)


def _json(data: Any, status: int = 200):
    frappe.local.response.http_status_code = status
    frappe.local.response.content_type = "application/json"
    return data


def _require_auth():
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Not authenticated"), frappe.AuthenticationError)


def _require_admin():
    _require_auth()
    if not frappe.db.get_value("User", frappe.session.user, "user_type") in ("System User",):
        if "System Manager" not in frappe.get_roles():
            frappe.throw(_("Not authorized"), frappe.PermissionError)


# ── Auth ──


def _handle_auth_register(payload: dict):
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    phone = (payload.get("phone") or "").strip()
    password = (payload.get("password") or "").strip()

    if not name or not email or not password:
        frappe.throw(_("Name, email and password are required"))

    if frappe.db.exists("User", email):
        frappe.throw(_("User already exists"))

    user = frappe.get_doc(
        {
            "doctype": "User",
            "email": email,
            "first_name": name,
            "mobile_no": phone,
            "send_welcome_email": 0,
            "user_type": "Website User",
        }
    )
    user.insert(ignore_permissions=True)
    user.new_password = password

    profile = frappe.db.exists("Customer Profile", {"user": user.name})
    if not profile:
        frappe.get_doc(
            {
                "doctype": "Customer Profile",
                "user": user.name,
                "full_name": name,
                "email": email,
                "mobile": phone,
            }
        ).insert(ignore_permissions=True)

    frappe.login(user=user.name)
    token = _generate_token(user.name)

    return _json(
        {
            "token": token,
            "user": {
                "name": user.first_name,
                "email": user.email,
                "phone": user.mobile_no,
                "is_admin": "System Manager" in frappe.get_roles(),
            },
        }
    )


def _handle_auth_login(payload: dict):
    email = (payload.get("email") or "").strip().lower()
    password = (payload.get("password") or "").strip()

    if not email or not password:
        frappe.throw(_("Email and password are required"))

    try:
        frappe.login(user=email, password=password)
    except frappe.AuthenticationError:
        frappe.throw(_("Invalid email or password"))

    user = frappe.get_doc("User", email)
    token = _generate_token(email)

    return _json(
        {
            "token": token,
            "user": {
                "name": user.first_name,
                "email": user.email,
                "phone": user.mobile_no,
                "is_admin": "System Manager" in frappe.get_roles(),
            },
        }
    )


def _generate_token(user: str) -> str:
    import secrets

    token = secrets.token_urlsafe(32)
    frappe.cache().set(f"api_token:{token}", user, expires_in_sec=86400 * 30)
    return token


def _resolve_user_from_token() -> str | None:
    auth = frappe.request.headers.get("Authorization") or ""
    if auth.startswith("Bearer "):
        token = auth[7:]
        return frappe.cache().get(f"api_token:{token}")
    return None


def _handle_auth_me():
    user_email = _resolve_user_from_token()
    if not user_email:
        _require_auth()
        user_email = frappe.session.user
    user = frappe.get_doc("User", user_email)
    profile = frappe.db.get_value("Customer Profile", {"user": user_email}, ["name", "full_name", "mobile", "email"], as_dict=True)
    return _json(
        {
            "name": user.first_name,
            "email": user.email,
            "phone": user.mobile_no,
            "is_admin": "System Manager" in frappe.get_roles(),
            "profile": profile or {},
        }
    )


def _handle_auth_update(payload: dict):
    user_email = _resolve_user_from_token()
    if not user_email:
        _require_auth()
        user_email = frappe.session.user
    user = frappe.get_doc("User", user_email)
    if payload.get("name"):
        user.first_name = payload["name"]
    if payload.get("phone"):
        user.mobile_no = payload["phone"]
    user.save(ignore_permissions=True)

    profile_name = frappe.db.get_value("Customer Profile", {"user": user_email}, "name")
    if profile_name:
        profile = frappe.get_doc("Customer Profile", profile_name)
        if payload.get("name"):
            profile.full_name = payload["name"]
        if payload.get("phone"):
            profile.mobile = payload["phone"]
        if payload.get("email"):
            profile.email = payload["email"]
        profile.save(ignore_permissions=True)

    return _json({"ok": True, "user": {"name": user.first_name, "email": user.email, "phone": user.mobile_no}})


# ── Categories ──


def _handle_list_categories():
    rows = frappe.get_all(
        CATEGORY_DOCTYPE,
        filters={"is_active": 1},
        fields=[
            "name", "item_group_name", "slug", "image", "description",
            "display_order", "parent_item_group", "icon", "color",
            "has_variants", "variant_label", "has_grinds",
            "default_variants_json", "default_grinds_json", "attributes_json",
        ],
        order_by="display_order asc, creation asc",
    )
    result = []
    for row in rows:
        result.append({
            "id": row.name,
            "name": row.item_group_name,
            "title": row.item_group_name,
            "slug": row.slug,
            "image": row.image,
            "description": row.description,
            "display_order": row.display_order,
            "parent_id": row.parent_item_group,
            "parent_item_group": row.parent_item_group,
            "icon": row.icon,
            "color": row.color,
            "has_variants": bool(row.has_variants) if hasattr(row, 'has_variants') else False,
            "variant_label": row.variant_label if hasattr(row, 'variant_label') else "",
            "has_grinds": bool(row.has_grinds) if hasattr(row, 'has_grinds') else False,
            "default_variants": _parse_json_field(row.default_variants_json),
            "default_grinds": _parse_json_field(row.default_grinds_json),
            "attributes": _parse_json_field(row.attributes_json),
        })
    return _json(result)


def _parse_json_field(value: str | None) -> Any:
    if not value:
        return []
    try:
        return frappe.parse_json(value)
    except Exception:
        return []


# ── Products ──


def _handle_list_products(args: dict):
    from coffeeyar.api import list_products as _list_products

    filters = {}
    sort = args.get("sort")
    page = args.get("page", 1)
    page_size = args.get("page_size", 24)

    if args.get("category_slug"):
        filters["category_slug"] = args["category_slug"]
    if args.get("featured"):
        filters["featured"] = 1
    if args.get("in_stock"):
        filters["in_stock"] = 1
    if args.get("slug"):
        filters["slug"] = args["slug"]

    result = _list_products(filters=frappe.as_json(filters) if filters else None, sort=sort, page=page)
    return _json(result)


def _handle_get_product(slug: str):
    from coffeeyar.api import get_product as _get_product

    result = _get_product(slug)
    return _json(result)


def _handle_product_faqs(slug: str):
    product_name = frappe.db.get_value("Product", {"slug": slug}, "name")
    if not product_name:
        frappe.throw(_("Product not found"), frappe.DoesNotExistError)
    rows = frappe.get_all(
        "Product FAQ",
        filters={"product": product_name, "is_active": 1},
        fields=["question", "answer"],
        order_by="display_order asc, creation asc",
    )
    return _json(rows)


# ── Reviews ──


def _handle_list_reviews(product_id: str):
    rows = frappe.get_all(
        "Product Review",
        filters={"product": product_id, "is_approved": 1},
        fields=["name", "user_name", "rating", "text", "creation"],
        order_by="creation desc",
    )
    for row in rows:
        row["id"] = row.name
    return _json(rows)


def _handle_create_review(payload: dict):
    product_id = payload.get("product_id") or ""
    user_name = payload.get("user_name") or payload.get("name") or "کاربر"
    rating = _to_int(payload.get("rating"), 0)
    text = payload.get("text") or ""

    if not product_id or not rating:
        frappe.throw(_("Product ID and rating are required"))

    doc = frappe.get_doc(
        {
            "doctype": "Product Review",
            "product": product_id,
            "user_name": user_name,
            "rating": rating,
            "text": text,
            "is_approved": 0,
        }
    )
    doc.insert(ignore_permissions=True)
    return _json({"id": doc.name, "user_name": user_name, "rating": rating, "text": text, "creation": doc.creation}, 201)


# ── Wishlist ──


def _handle_wishlist_toggle(product_id: str):
    user_email = _resolve_user_from_token()
    if not user_email:
        frappe.throw(_("Not authenticated"), frappe.AuthenticationError)

    key = f"wishlist:{user_email}"
    ids = frappe.cache().get(key) or []
    if isinstance(ids, str):
        ids = frappe.parse_json(ids)
    ids = list(ids) if ids else []

    wishlisted = product_id in ids
    if wishlisted:
        ids = [i for i in ids if i != product_id]
    else:
        ids.append(product_id)
    frappe.cache().set(key, ids, expires_in_sec=86400 * 365)

    return _json({"wishlisted": not wishlisted, "ids": ids})


def _handle_wishlist_ids():
    user_email = _resolve_user_from_token()
    if not user_email:
        return _json({"ids": []})
    key = f"wishlist:{user_email}"
    ids = frappe.cache().get(key) or []
    if isinstance(ids, str):
        ids = frappe.parse_json(ids)
    return _json({"ids": list(ids) if ids else []})


def _handle_wishlist_list():
    user_email = _resolve_user_from_token()
    if not user_email:
        return _json([])
    key = f"wishlist:{user_email}"
    ids = frappe.cache().get(key) or []
    if isinstance(ids, str):
        ids = frappe.parse_json(ids)
    ids = list(ids) if ids else []
    products = []
    for pid in ids:
        doc = frappe.db.get_value("Product", {"name": pid}, ["name", "item_name", "slug", "image", "price_toman", "discount_toman"], as_dict=True)
        if doc:
            products.append({
                "id": doc.name,
                "name": doc.item_name,
                "slug": doc.slug,
                "image": doc.image,
                "price_toman": _to_int(doc.price_toman),
                "discount_toman": _to_int(doc.discount_toman),
                "effective_price_toman": _effective_price(doc.price_toman, doc.discount_toman),
            })
    return _json(products)


# ── Coupons ──


def _handle_coupon_validate(payload: dict):
    code = (payload.get("code") or "").strip().upper()
    order_total = _to_int(payload.get("order_total"), 0)

    if not code:
        frappe.throw(_("Coupon code is required"))

    coupon_name = frappe.db.get_value("Coupon", {"code": code, "is_active": 1}, "name")
    if not coupon_name:
        frappe.throw(_("Invalid coupon code"))

    coupon = frappe.get_doc("Coupon", coupon_name)

    from frappe.utils import now_datetime

    now = now_datetime()
    if coupon.valid_from and coupon.valid_from > now:
        frappe.throw(_("Coupon is not yet valid"))
    if coupon.valid_until and coupon.valid_until < now:
        frappe.throw(_("Coupon has expired"))
    if coupon.max_uses > 0 and coupon.used_count >= coupon.max_uses:
        frappe.throw(_("Coupon usage limit reached"))
    if order_total < coupon.minimum_order_toman:
        frappe.throw(_("Minimum order amount not met"))

    discount = coupon.discount_amount
    if coupon.discount_type == "Percentage":
        discount = order_total * discount / 100

    return _json({
        "code": coupon.code,
        "discount": int(discount),
        "discount_type": coupon.discount_type,
        "description": coupon.description,
    })


# ── Orders ──


def _handle_create_order(payload: dict):
    from coffeeyar.api import create_order as _create_order

    result = _create_order(frappe.as_json(payload))
    return _json(result, 201)


def _handle_list_orders():
    user_email = _resolve_user_from_token()
    if not user_email:
        _require_auth()
        user_email = frappe.session.user

    orders = frappe.get_all(
        "Order",
        filters={"customer_user": user_email},
        fields=["name", "customer_name", "total_toman", "order_status", "payment_status", "tracking_code", "creation"],
        order_by="creation desc",
    )
    for o in orders:
        o["id"] = o.name
        o["totalPrice"] = _to_int(o.total_toman)
        o["date"] = str(o.creation)
        o["status"] = o.order_status
        o["trackingCode"] = o.tracking_code or ""
    return _json(orders)


def _handle_get_order(ref: str):
    order = frappe.get_doc("Order", ref)
    items = []
    for item in order.items or []:
        items.append({
            "productId": item.product_slug or item.product,
            "name": item.product_title,
            "image": "",
            "weight": item.variant_title or "",
            "grind": "",
            "unitPrice": _to_int(item.unit_price_toman),
            "qty": _to_int(item.qty),
        })

    return _json({
        "id": order.name,
        "date": str(order.creation),
        "status": order.order_status,
        "payment_status": order.payment_status,
        "items": items,
        "totalPrice": _to_int(order.total_toman),
        "address": order.shipping_address or "",
        "trackingCode": order.tracking_code or "",
        "customer_name": order.customer_name,
        "mobile": order.mobile,
    })


# ── Returns ──


def _handle_create_return(payload: dict):
    doc = frappe.get_doc(
        {
            "doctype": "Return Request",
            "order": payload.get("order_id") or "",
            "order_ref": payload.get("order_ref") or "",
            "reason": payload.get("reason") or "",
            "description": payload.get("description") or "",
            "total_amount_toman": _to_int(payload.get("total_amount"), 0),
            "customer_name": (payload.get("customer_name") or frappe.session.user).strip(),
        }
    )
    for item in payload.get("items") or []:
        doc.append("items", {
            "product": item.get("product_id") or item.get("product") or "",
            "product_title": item.get("name") or item.get("product_title") or "",
            "qty": _to_int(item.get("qty"), 1),
            "unit_price_toman": _to_int(item.get("unit_price") or item.get("unit_price_toman"), 0),
        })
    doc.insert(ignore_permissions=True)
    return _json({
        "id": doc.name,
        "status": doc.status,
        "created_at": str(doc.creation),
    }, 201)


def _handle_list_returns():
    user_email = _resolve_user_from_token()
    if not user_email:
        return _json([])
    rows = frappe.get_all(
        "Return Request",
        fields=["name", "order_ref", "reason", "description", "status", "admin_note", "creation"],
        order_by="creation desc",
    )
    for r in rows:
        r["id"] = r.name
    return _json(rows)


# ── FAQ ──


def _handle_list_faq():
    rows = frappe.get_all(
        "FAQ",
        filters={"is_active": 1},
        fields=["question", "answer"],
        order_by="display_order asc, creation asc",
    )
    return _json(rows)


# ── Blog ──


def _handle_list_blog_posts(args: dict):
    from coffeeyar.api import list_blog_posts as _list_blog_posts

    result = _list_blog_posts(page=args.get("page", 1), page_size=args.get("page_size", 12))
    return _json(result)


def _handle_get_blog_post(slug: str):
    from coffeeyar.api import get_blog_post as _get_blog_post

    result = _get_blog_post(slug)
    return _json(result)


# ── Site ──


def _handle_site_settings():
    settings = _get_settings()
    return _json({
        "shop_name": settings.store_name or "فروشگاه",
        "description": settings.get("description") or "",
        "phone": settings.get("phone") or "",
        "email": settings.get("email") or "",
        "address": settings.get("address") or "",
        "instagram": settings.get("instagram") or "",
        "telegram": settings.get("telegram") or "",
        "enamad_code": settings.get("enamad_code") or "",
        "payment_online": bool(settings.get("payment_online", 1)),
        "payment_cod": bool(settings.get("payment_cod", 1)),
        "shipping": {
            "standard": {
                "enabled": True,
                "label": "ارسال عادی",
                "days": "۲ تا ۴ روز کاری",
                "price": _to_int(settings.get("shipping_standard_price", 45000)),
                "free_threshold": _to_int(settings.get("shipping_standard_free_threshold", 500000)),
            },
            "express": {
                "enabled": True,
                "label": "ارسال اکسپرس",
                "days": "۲۴ ساعته",
                "price": _to_int(settings.get("shipping_express_price", 90000)),
                "free_threshold": 0,
            },
        },
        "shipping_fee_toman": _to_int(settings.shipping_fee_toman, 120000),
        "use_sandbox": bool(settings.use_sandbox),
    })


def _handle_navigation():
    from coffeeyar.api import get_navigation as _get_navigation

    return _json(_get_navigation())


# ── Addresses ──


def _handle_list_addresses():
    user_email = _resolve_user_from_token()
    if not user_email:
        _require_auth()
        user_email = frappe.session.user

    profile_name = frappe.db.get_value("Customer Profile", {"user": user_email}, "name")
    if not profile_name:
        return _json([])

    rows = frappe.get_all(
        "Customer Address",
        filters={"customer": profile_name},
        fields=["name", "title", "recipient_name", "mobile", "province", "city", "address_line", "postal_code", "is_default"],
        order_by="is_default desc, creation desc",
    )
    result = []
    for r in rows:
        result.append({
            "id": r.name,
            "label": r.title,
            "fullName": r.recipient_name,
            "phone": r.mobile,
            "province": r.province,
            "city": r.city,
            "street": r.address_line,
            "postalCode": r.postal_code,
            "isDefault": bool(r.is_default),
        })
    return _json(result)


def _handle_create_address(payload: dict):
    user_email = _resolve_user_from_token()
    if not user_email:
        _require_auth()
        user_email = frappe.session.user

    profile_name = frappe.db.get_value("Customer Profile", {"user": user_email}, "name")
    if not profile_name:
        frappe.throw(_("Customer profile not found"))

    doc = frappe.get_doc(
        {
            "doctype": "Customer Address",
            "customer": profile_name,
            "title": payload.get("label") or payload.get("title") or "خانه",
            "recipient_name": payload.get("fullName") or payload.get("recipient_name") or user_email,
            "mobile": payload.get("phone") or payload.get("mobile") or "",
            "province": payload.get("province") or "",
            "city": payload.get("city") or "",
            "address_line": payload.get("street") or payload.get("address_line") or payload.get("address") or "",
            "postal_code": payload.get("postalCode") or payload.get("postal_code") or "",
            "is_default": bool(payload.get("isDefault") or payload.get("is_default")),
        }
    )
    doc.insert(ignore_permissions=True)
    return _json({"id": doc.name, "ok": True}, 201)


def _handle_delete_address(address_id: str):
    frappe.delete_doc("Customer Address", address_id, ignore_permissions=True)
    return _json({"ok": True})


# ── Admin ──


def _handle_admin(segments: list[str], method: str, payload: dict, args: dict):
    _require_admin()

    if not segments:
        if method == "GET":
            return _handle_admin_dashboard()
        return _json({"error": "Not found"}, 404)

    resource = segments[0]

    if resource == "products":
        return _admin_products(segments[1:], method, payload)
    if resource == "categories":
        return _admin_categories(segments[1:], method, payload)
    if resource == "orders":
        return _admin_orders(segments[1:], method, payload)
    if resource == "customers" and method == "GET":
        return _admin_customers()
    if resource == "blog":
        return _admin_blog(segments[1:], method, payload)
    if resource == "faq":
        return _admin_faq(segments[1:], method, payload)
    if resource == "coupons":
        return _admin_coupons(segments[1:], method, payload)
    if resource == "navigation":
        return _admin_navigation(segments[1:], method, payload)
    if resource == "site-settings" and method == "PUT":
        return _admin_site_settings(payload)
    if resource == "returns":
        return _admin_returns(segments[1:], method, payload)
    if resource == "dashboard" and method == "GET":
        return _handle_admin_dashboard()
    if resource == "content":
        return _admin_content(method, payload)
    if resource == "policies":
        return _admin_policies(method, payload)
    if resource == "groups":
        return _admin_groups(method, payload)
    if resource == "templates":
        return _admin_templates(method, payload)
    if resource == "profiles":
        return _admin_profiles(method, payload)
    if resource == "product-faqs":
        return _admin_product_faqs(method, payload)
    if resource == "theme":
        return _admin_theme(method, payload)

    return _json({"error": "Not found"}, 404)


def _handle_admin_dashboard():
    from frappe.utils import now_datetime, add_days

    today = now_datetime().date()
    week_ago = add_days(today, -7)

    total_orders = frappe.db.count("Order")
    total_revenue = frappe.db.sql("SELECT COALESCE(SUM(total_toman), 0) FROM `tabOrder` WHERE payment_status = 'Paid'")[0][0]
    total_products = frappe.db.count("Product", {"is_published": 1})
    total_customers = frappe.db.count("Customer Profile")
    recent_orders = frappe.db.count("Order", {"creation": [">=", str(week_ago)]})

    return _json({
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "total_products": total_products,
        "total_customers": total_customers,
        "recent_orders": recent_orders,
    })


def _admin_products(segments: list[str], method: str, payload: dict):
    if method == "GET":
        rows = frappe.get_all("Product", fields=["name", "item_name", "slug", "price_toman", "stock_qty", "is_published", "display_order"], order_by="display_order asc")
        for r in rows:
            r["id"] = r.name
        return _json(rows)
    if method == "POST":
        doc = frappe.get_doc({
            "doctype": "Product",
            "item_name": payload.get("item_name") or payload.get("name") or payload.get("title") or "",
            "slug": payload.get("slug") or _slugify(payload.get("item_name") or payload.get("name") or payload.get("title") or ""),
            "item_group": payload.get("item_group") or payload.get("category") or "",
            "price_toman": _to_int(payload.get("price_toman"), 0),
            "discount_toman": _to_int(payload.get("discount_toman"), 0),
            "stock_qty": _to_int(payload.get("stock_qty"), 0),
            "image": payload.get("image") or "",
            "short_description": payload.get("short_description") or "",
            "description": payload.get("description") or "",
            "is_published": bool(payload.get("is_published", 1)),
            "is_featured": bool(payload.get("is_featured")),
            "has_variants": bool(payload.get("has_variants")),
            "display_order": _to_int(payload.get("display_order"), 0),
        }).insert(ignore_permissions=True)
        return _json({"id": doc.name, "ok": True}, 201)
    if method == "PUT" and segments:
        doc = frappe.get_doc("Product", segments[0])
        for key in ["item_name", "slug", "item_group", "price_toman", "discount_toman", "stock_qty", "image", "short_description", "description", "sku", "display_order"]:
            if key in payload:
                doc.set(key, payload[key])
        for key in ["is_published", "is_featured", "has_variants"]:
            if key in payload:
                doc.set(key, bool(payload[key]))
        doc.save(ignore_permissions=True)
        return _json({"ok": True})
    if method == "DELETE" and segments:
        frappe.delete_doc("Product", segments[0], ignore_permissions=True)
        return _json({"ok": True})

    return _json({"error": "Not found"}, 404)


def _admin_categories(segments: list[str], method: str, payload: dict):
    if method == "GET":
        rows = frappe.get_all("Product Category", fields=["*"], order_by="display_order asc")
        for r in rows:
            r["id"] = r.name
        return _json(rows)
    if method == "POST":
        doc = frappe.get_doc({
            "doctype": "Product Category",
            "item_group_name": payload.get("name") or payload.get("item_group_name") or payload.get("title") or "",
            "slug": payload.get("slug") or _slugify(payload.get("name") or ""),
            "parent_item_group": payload.get("parent_id") or payload.get("parent_item_group") or None,
            "icon": payload.get("icon") or "",
            "color": payload.get("color") or "",
            "image": payload.get("image") or "",
            "description": payload.get("description") or "",
            "display_order": _to_int(payload.get("display_order") or payload.get("order"), 0),
            "has_variants": bool(payload.get("has_variants")),
            "variant_label": payload.get("variant_label") or "",
            "has_grinds": bool(payload.get("has_grinds")),
            "default_variants_json": payload.get("default_variants_json") or "",
            "default_grinds_json": payload.get("default_grinds_json") or "",
            "attributes_json": payload.get("attributes_json") or "",
            "is_active": bool(payload.get("is_active", 1)),
        }).insert(ignore_permissions=True)
        return _json({"id": doc.name, "ok": True}, 201)
    if method == "PUT" and segments:
        doc = frappe.get_doc("Product Category", segments[0])
        for key in payload:
            if key in ("name", "id"):
                continue
            doc.set(key, payload[key])
        doc.save(ignore_permissions=True)
        return _json({"ok": True})
    if method == "DELETE" and segments:
        frappe.delete_doc("Product Category", segments[0], ignore_permissions=True)
        return _json({"ok": True})
    return _json({"error": "Not found"}, 404)


def _admin_orders(segments: list[str], method: str, payload: dict):
    if method == "GET":
        rows = frappe.get_all("Order", fields=["name", "customer_name", "total_toman", "order_status", "payment_status", "creation"], order_by="creation desc")
        for r in rows:
            r["id"] = r.name
        return _json(rows)
    if len(segments) >= 2 and segments[1] == "status" and method == "PUT":
        doc = frappe.get_doc("Order", segments[0])
        if payload.get("order_status"):
            doc.order_status = payload["order_status"]
        if payload.get("payment_status"):
            doc.payment_status = payload["payment_status"]
        if payload.get("tracking_code"):
            doc.tracking_code = payload["tracking_code"]
        doc.save(ignore_permissions=True)
        return _json({"ok": True, "order_status": doc.order_status})
    return _json({"error": "Not found"}, 404)


def _admin_customers():
    rows = frappe.get_all("Customer Profile", fields=["name", "full_name", "email", "mobile", "creation"], order_by="creation desc")
    for r in rows:
        r["id"] = r.name
    return _json(rows)


def _admin_blog(segments: list[str], method: str, payload: dict):
    if method == "GET":
        rows = frappe.get_all("Blog Post", fields=["name", "title", "slug", "is_published", "published_on", "display_order"], order_by="display_order asc")
        for r in rows:
            r["id"] = r.name
        return _json(rows)
    if method == "POST":
        doc = frappe.get_doc({
            "doctype": "Blog Post",
            "title": payload.get("title") or "",
            "slug": payload.get("slug") or _slugify(payload.get("title") or ""),
            "content": payload.get("content") or "",
            "excerpt": payload.get("excerpt") or "",
            "cover_image": payload.get("cover_image") or "",
            "is_published": bool(payload.get("is_published", 1)),
            "published_on": payload.get("published_on") or None,
            "display_order": _to_int(payload.get("display_order"), 0),
        }).insert(ignore_permissions=True)
        return _json({"id": doc.name, "ok": True}, 201)
    if method == "PUT" and segments:
        doc = frappe.get_doc("Blog Post", segments[0])
        for key in ["title", "slug", "content", "excerpt", "cover_image", "published_on", "display_order"]:
            if key in payload:
                doc.set(key, payload[key])
        if "is_published" in payload:
            doc.set("is_published", bool(payload["is_published"]))
        doc.save(ignore_permissions=True)
        return _json({"ok": True})
    if method == "DELETE" and segments:
        frappe.delete_doc("Blog Post", segments[0], ignore_permissions=True)
        return _json({"ok": True})
    return _json({"error": "Not found"}, 404)


def _admin_faq(segments: list[str], method: str, payload: dict):
    if method == "GET":
        rows = frappe.get_all("FAQ", fields=["name", "question", "answer", "display_order", "is_active"], order_by="display_order asc")
        for r in rows:
            r["id"] = r.name
        return _json(rows)
    if method == "POST":
        doc = frappe.get_doc({
            "doctype": "FAQ",
            "question": payload.get("question") or "",
            "answer": payload.get("answer") or "",
            "display_order": _to_int(payload.get("display_order"), 0),
            "is_active": bool(payload.get("is_active", 1)),
        }).insert(ignore_permissions=True)
        return _json({"id": doc.name, "ok": True}, 201)
    if method == "PUT" and segments:
        doc = frappe.get_doc("FAQ", segments[0])
        for key in ["question", "answer", "display_order"]:
            if key in payload:
                doc.set(key, payload[key])
        if "is_active" in payload:
            doc.set("is_active", bool(payload["is_active"]))
        doc.save(ignore_permissions=True)
        return _json({"ok": True})
    if method == "DELETE" and segments:
        frappe.delete_doc("FAQ", segments[0], ignore_permissions=True)
        return _json({"ok": True})
    return _json({"error": "Not found"}, 404)


def _admin_coupons(segments: list[str], method: str, payload: dict):
    if method == "GET":
        rows = frappe.get_all("Coupon", fields=["name", "code", "description", "discount_type", "discount_amount", "minimum_order_toman", "max_uses", "used_count", "is_active"], order_by="creation desc")
        for r in rows:
            r["id"] = r.name
        return _json(rows)
    if method == "POST":
        doc = frappe.get_doc({
            "doctype": "Coupon",
            "code": (payload.get("code") or "").upper(),
            "description": payload.get("description") or "",
            "discount_type": payload.get("discount_type") or "Percentage",
            "discount_amount": _to_int(payload.get("discount_amount"), 0),
            "minimum_order_toman": _to_int(payload.get("minimum_order_toman"), 0),
            "max_uses": _to_int(payload.get("max_uses"), 0),
            "is_active": bool(payload.get("is_active", 1)),
        }).insert(ignore_permissions=True)
        return _json({"id": doc.name, "ok": True}, 201)
    if method == "DELETE" and segments:
        frappe.delete_doc("Coupon", segments[0], ignore_permissions=True)
        return _json({"ok": True})
    if method in ("PATCH", "PUT") and segments:
        doc = frappe.get_doc("Return Request", segments[0])
        if payload.get("status"):
            doc.status = payload["status"]
        if payload.get("admin_note") is not None:
            doc.admin_note = payload["admin_note"]
        doc.save(ignore_permissions=True)
        return _json({"ok": True, "status": doc.status})
    return _json({"error": "Not found"}, 404)


# ── Public: Content ──


def _handle_public_content():
    doc = _get_single_doctype("Page Content")
    return _json({
        "home": _parse_json_field(doc.home_hero_json if hasattr(doc, 'home_hero_json') else ""),
        "about": _parse_json_field(doc.about_json if hasattr(doc, 'about_json') else ""),
        "contact": _parse_json_field(doc.contact_json if hasattr(doc, 'contact_json') else ""),
    })


def _handle_public_policies():
    doc = _get_single_doctype("Site Policy")
    return _json(_parse_json_field(doc.policies_json if hasattr(doc, 'policies_json') else ""))


def _handle_public_product_global_faqs():
    doc = _get_single_doctype("Product Global FAQ Setting")
    return _json(_parse_json_field(doc.faqs_json if hasattr(doc, 'faqs_json') else ""))


# ── Admin: Content ──


def _admin_content(method: str, payload: dict):
    if method == "GET":
        doc = _get_single_doctype("Page Content")
        return _json({
            "home": _parse_json_field(doc.home_hero_json),
            "about": _parse_json_field(doc.about_json),
            "contact": _parse_json_field(doc.contact_json),
        })
    if method == "PUT":
        doc = _get_single_doctype("Page Content", create=True)
        if "home" in payload:
            doc.home_hero_json = frappe.as_json(payload["home"])
        if "about" in payload:
            doc.about_json = frappe.as_json(payload["about"])
        if "contact" in payload:
            doc.contact_json = frappe.as_json(payload["contact"])
        doc.save(ignore_permissions=True)
        return _json({"ok": True})
    return _json({"error": "Not found"}, 404)


# ── Admin: Policies ──


def _admin_policies(method: str, payload: dict):
    if method == "GET":
        doc = _get_single_doctype("Site Policy")
        return _json(_parse_json_field(doc.policies_json))
    if method == "PUT":
        doc = _get_single_doctype("Site Policy", create=True)
        doc.policies_json = frappe.as_json(payload if isinstance(payload, dict) else {})
        doc.save(ignore_permissions=True)
        return _json({"ok": True})
    return _json({"error": "Not found"}, 404)


# ── Admin: Groups ──


def _admin_groups(method: str, payload: dict):
    if method == "GET":
        doc = _get_single_doctype("Product Group Setting")
        return _json(_parse_json_field(doc.groups_json))
    if method == "PUT":
        doc = _get_single_doctype("Product Group Setting", create=True)
        doc.groups_json = frappe.as_json(payload if isinstance(payload, dict) else payload.get("groups", []))
        doc.save(ignore_permissions=True)
        return _json({"ok": True})
    return _json({"error": "Not found"}, 404)


# ── Admin: Templates ──


def _admin_templates(method: str, payload: dict):
    if method == "GET":
        doc = _get_single_doctype("Product Template Setting")
        return _json(_parse_json_field(doc.templates_json))
    if method == "PUT":
        doc = _get_single_doctype("Product Template Setting", create=True)
        doc.templates_json = frappe.as_json(payload if isinstance(payload, dict) else payload.get("templates", []))
        doc.save(ignore_permissions=True)
        return _json({"ok": True})
    return _json({"error": "Not found"}, 404)


# ── Admin: Taste Profiles ──


def _admin_profiles(method: str, payload: dict):
    if method == "GET":
        doc = _get_single_doctype("Taste Profile Setting")
        return _json({
            "profiles": _parse_json_field(doc.profiles_json),
            "assignments": _parse_json_field(doc.assignments_json),
        })
    if method == "PUT":
        doc = _get_single_doctype("Taste Profile Setting", create=True)
        if "profiles" in payload:
            doc.profiles_json = frappe.as_json(payload["profiles"])
        if "assignments" in payload:
            doc.assignments_json = frappe.as_json(payload["assignments"])
        doc.save(ignore_permissions=True)
        return _json({"ok": True})
    return _json({"error": "Not found"}, 404)


# ── Admin: Product Global FAQs ──


def _admin_product_faqs(method: str, payload: dict):
    if method == "GET":
        doc = _get_single_doctype("Product Global FAQ Setting")
        return _json(_parse_json_field(doc.faqs_json))
    if method == "PUT":
        doc = _get_single_doctype("Product Global FAQ Setting", create=True)
        doc.faqs_json = frappe.as_json(payload if isinstance(payload, dict) else payload.get("faqs", []))
        doc.save(ignore_permissions=True)
        return _json({"ok": True})
    return _json({"error": "Not found"}, 404)


# ── Admin: Theme ──


def _admin_theme(method: str, payload: dict):
    if method == "GET":
        doc = _get_single_doctype("Theme Config")
        return _json({
            "theme": _parse_json_field(doc.theme_json),
            "layout": _parse_json_field(doc.layout_json),
        })
    if method == "PUT":
        doc = _get_single_doctype("Theme Config", create=True)
        if "theme" in payload:
            doc.theme_json = frappe.as_json(payload["theme"])
        if "layout" in payload:
            doc.layout_json = frappe.as_json(payload["layout"])
        doc.save(ignore_permissions=True)
        return _json({"ok": True})
    return _json({"error": "Not found"}, 404)


# ── Helper ──


def _get_single_doctype(doctype: str, create: bool = False):
    name = frappe.db.get_single_value(doctype, "name")
    if name:
        return frappe.get_doc(doctype, name)
    if create:
        doc = frappe.get_doc({"doctype": doctype})
        doc.insert(ignore_permissions=True)
        return doc
    return frappe.get_doc({"doctype": doctype})


def _admin_navigation(segments: list[str], method: str, payload: dict):
    if method == "GET":
        rows = frappe.get_all("Navigation Link", fields=["name", "label", "route", "placement", "display_order", "is_active"], order_by="display_order asc")
        for r in rows:
            r["id"] = r.name
        return _json(rows)
    if method == "POST":
        doc = frappe.get_doc({
            "doctype": "Navigation Link",
            "label": payload.get("label") or "",
            "route": payload.get("route") or "/",
            "placement": payload.get("placement") or "Header",
            "display_order": _to_int(payload.get("display_order"), 0),
            "is_active": bool(payload.get("is_active", 1)),
        }).insert(ignore_permissions=True)
        return _json({"id": doc.name, "ok": True}, 201)
    if method == "PUT" and segments:
        doc = frappe.get_doc("Navigation Link", segments[0])
        for key in ["label", "route", "placement", "display_order"]:
            if key in payload:
                doc.set(key, payload[key])
        if "is_active" in payload:
            doc.set("is_active", bool(payload["is_active"]))
        doc.save(ignore_permissions=True)
        return _json({"ok": True})
    if method == "DELETE" and segments:
        frappe.delete_doc("Navigation Link", segments[0], ignore_permissions=True)
        return _json({"ok": True})
    return _json({"error": "Not found"}, 404)


def _admin_site_settings(payload: dict):
    settings = _get_settings()
    mapping = {
        "shop_name": "store_name",
        "description": "description",
        "phone": "phone",
        "email": "email",
        "address": "address",
        "instagram": "instagram",
        "telegram": "telegram",
        "enamad_code": "enamad_code",
        "shipping_standard_price": "shipping_standard_price",
        "shipping_standard_free_threshold": "shipping_standard_free_threshold",
        "shipping_express_price": "shipping_express_price",
    }
    for payload_key, doc_key in mapping.items():
        if payload_key in payload:
            settings.set(doc_key, payload[payload_key])
    if "payment_online" in payload:
        settings.set("payment_online", bool(payload["payment_online"]))
    if "payment_cod" in payload:
        settings.set("payment_cod", bool(payload["payment_cod"]))
    settings.save(ignore_permissions=True)
    return _json({"ok": True})


def _admin_returns(segments: list[str], method: str, payload: dict):
    if method == "GET":
        rows = frappe.get_all("Return Request", fields=["name", "order_ref", "reason", "status", "customer_name", "creation"], order_by="creation desc")
        for r in rows:
            r["id"] = r.name
        return _json(rows)
    if len(segments) >= 2 and segments[1] == "status" and method == "PUT":
        doc = frappe.get_doc("Return Request", segments[0])
        if payload.get("status"):
            doc.status = payload["status"]
        if payload.get("admin_note") is not None:
            doc.admin_note = payload["admin_note"]
        doc.save(ignore_permissions=True)
        return _json({"ok": True, "status": doc.status})
    return _json({"error": "Not found"}, 404)
