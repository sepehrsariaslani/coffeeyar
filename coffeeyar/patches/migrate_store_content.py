from __future__ import annotations

import frappe
from frappe.utils import today


def execute():
    _merge_legacy_categories()
    _merge_legacy_products()
    _ensure_settings()
    _ensure_default_pages()
    _ensure_default_navigation()
    _ensure_default_attributes()


def _table_exists(table: str) -> bool:
    return table in frappe.db.get_tables(cached=False)


def _get_value(doctype: str, filters, fieldname: str):
    try:
        return frappe.db.get_value(doctype, filters, fieldname)
    except Exception:
        return None


def _find_category(slug: str | None) -> str | None:
    if not slug:
        return None
    return _get_value("Product Category", {"slug": slug}, "name")


def _insert_doc(data: dict):
    doc = frappe.get_doc(data)
    doc.insert(ignore_permissions=True)
    return doc


def _merge_legacy_categories():
    if not _table_exists("tabCoffee Category"):
        return

    root = _ensure_category("محصولات", "products", is_group=1)
    rows = frappe.db.sql(
        """
        SELECT title, slug, image, display_order, is_active
        FROM `tabCoffee Category`
        ORDER BY COALESCE(display_order, 0), creation
        """,
        as_dict=True,
    )
    for row in rows:
        if _find_category(row.slug):
            continue
        _insert_doc(
            {
                "doctype": "Product Category",
                "item_group_name": row.title,
                "slug": row.slug,
                "parent_item_group": root,
                "is_group": 0,
                "is_active": 1 if row.is_active is None else row.is_active,
                "image": row.image,
                "display_order": row.display_order or 0,
            }
        )


def _merge_legacy_products():
    if not _table_exists("tabCoffee Product"):
        return

    fallback_category = _ensure_category("محصولات", "products", is_group=1)
    rows = frappe.db.sql(
        """
        SELECT title, slug, category, image, gallery_json, short_description, description,
               price_toman, discount_toman, stock_qty, display_order, is_published
        FROM `tabCoffee Product`
        ORDER BY creation
        """,
        as_dict=True,
    )
    for row in rows:
        if _get_value("Product", {"slug": row.slug}, "name"):
            continue

        category = fallback_category
        if row.category and _table_exists("tabCoffee Category"):
            category_slug = frappe.db.sql(
                "SELECT slug FROM `tabCoffee Category` WHERE name=%s",
                (row.category,),
            )
            if category_slug:
                category = _find_category(category_slug[0][0]) or fallback_category

        _insert_doc(
            {
                "doctype": "Product",
                "item_name": row.title,
                "slug": row.slug,
                "item_group": category,
                "image": row.image,
                "gallery_json": row.gallery_json,
                "short_description": row.short_description,
                "description": row.description,
                "price_toman": row.price_toman or 0,
                "discount_toman": row.discount_toman or 0,
                "stock_qty": row.stock_qty or 0,
                "display_order": row.display_order or 0,
                "is_published": 1 if row.is_published is None else row.is_published,
            }
        )


def _ensure_category(title: str, slug: str, is_group: int = 0) -> str:
    existing = _find_category(slug)
    if existing:
        return existing
    doc = _insert_doc(
        {
            "doctype": "Product Category",
            "item_group_name": title,
            "slug": slug,
            "is_group": is_group,
            "is_active": 1,
            "display_order": 0,
        }
    )
    return doc.name


def _ensure_settings():
    settings = frappe.get_single("Store Settings")
    if not settings.store_name:
        settings.store_name = "فروشگاه"
    if not settings.home_page:
        settings.home_page = "home"
    if settings.shipping_fee_toman in (None, 0):
        settings.shipping_fee_toman = 120000
    if not settings.zarinpal_request_url:
        settings.zarinpal_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    if not settings.zarinpal_verify_url:
        settings.zarinpal_verify_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    if not settings.zarinpal_startpay_url:
        settings.zarinpal_startpay_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    if settings.use_sandbox is None:
        settings.use_sandbox = 1
    settings.save(ignore_permissions=True)


def _ensure_default_pages():
    pages = [
        {
            "title": "خانه",
            "slug": "home",
            "page_type": "Home",
            "hero_title": "فروشگاه مینیمال",
            "hero_subtitle": "محصولات منتخب، خرید ساده و پرداخت آنلاین",
            "body_html": "<p>این محتوا از پنل مدیریت قابل ویرایش است.</p>",
        },
        {
            "title": "درباره ما",
            "slug": "about-us",
            "page_type": "Content",
            "hero_title": "درباره ما",
            "body_html": "<p>درباره فروشگاه خود را از پنل مدیریت ویرایش کنید.</p>",
        },
        {
            "title": "شوروم",
            "slug": "showroom",
            "page_type": "Content",
            "hero_title": "شوروم",
            "body_html": "<p>اطلاعات بازدید حضوری را از پنل مدیریت وارد کنید.</p>",
        },
    ]
    for page in pages:
        if _get_value("Site Page", {"slug": page["slug"]}, "name"):
            continue
        page["doctype"] = "Site Page"
        page["is_published"] = 1
        _insert_doc(page)


def _ensure_default_navigation():
    links = [
        ("Header", "همه محصولات", "/all-products", 10),
        ("Header", "دسته‌ها", "/all-products", 20),
        ("Header", "بلاگ", "/blog", 30),
        ("Header", "درباره ما", "/about-us", 40),
        ("Header", "شوروم", "/showroom", 50),
        ("Mobile", "خانه", "/", 10),
        ("Mobile", "محصولات", "/all-products", 20),
        ("Mobile", "بلاگ", "/blog", 30),
        ("Mobile", "تسویه", "/checkout", 40),
    ]
    for placement, label, route, display_order in links:
        if _get_value("Navigation Link", {"placement": placement, "route": route}, "name"):
            continue
        _insert_doc(
            {
                "doctype": "Navigation Link",
                "placement": placement,
                "label": label,
                "route": route,
                "display_order": display_order,
                "is_active": 1,
            }
        )


def _ensure_default_attributes():
    for title, slug, options in [
        ("رنگ", "color", [("سفید", "white"), ("مشکی", "black")]),
        ("اندازه", "size", [("کوچک", "small"), ("متوسط", "medium"), ("بزرگ", "large")]),
        ("وزن", "weight", [("250 گرم", "250g"), ("500 گرم", "500g"), ("1 کیلوگرم", "1kg")]),
    ]:
        attr = _get_value("Product Attribute", {"slug": slug}, "name")
        if not attr:
            attr = _insert_doc(
                {
                    "doctype": "Product Attribute",
                    "title": title,
                    "slug": slug,
                    "display_order": 0,
                    "is_filterable": 1,
                    "is_active": 1,
                }
            ).name
        attr_doc = frappe.get_doc("Product Attribute", attr)
        existing_values = {(row.attribute_value or "").strip() for row in attr_doc.attribute_values or []}
        changed = False
        for idx, (option, option_slug) in enumerate(options, start=1):
            if option not in existing_values:
                attr_doc.append("attribute_values", {"attribute_value": option, "abbr": option_slug})
                existing_values.add(option)
                changed = True

            if _get_value("Product Attribute Option", {"attribute": attr, "slug": option_slug}, "name"):
                continue
            _insert_doc(
                {
                    "doctype": "Product Attribute Option",
                    "attribute": attr,
                    "title": option,
                    "slug": option_slug,
                    "display_order": idx,
                    "is_active": 1,
                }
            )
        if changed:
            attr_doc.save(ignore_permissions=True)

    if not _get_value("Blog Post", {"slug": "welcome"}, "name"):
        _insert_doc(
            {
                "doctype": "Blog Post",
                "title": "اولین نوشته",
                "slug": "welcome",
                "excerpt": "این نوشته نمونه از پنل مدیریت قابل ویرایش است.",
                "content": "<p>از این بخش برای انتشار مقاله‌ها و خبرهای فروشگاه استفاده کنید.</p>",
                "published_on": today(),
                "is_published": 1,
            }
        )
