import frappe


ROOT_GROUP = {"item_group_name": "محصولات", "slug": "products", "is_group": 1, "display_order": 1}

DEFAULT_GROUPS = [
    {"item_group_name": "محصولات منتخب", "slug": "featured", "display_order": 10},
    {"item_group_name": "کالاهای فیزیکی", "slug": "physical-products", "display_order": 20},
    {"item_group_name": "کالاهای دیجیتال", "slug": "digital-products", "display_order": 30},
    {"item_group_name": "لوازم جانبی", "slug": "accessory", "display_order": 40},
]


def after_install():
    _ensure_settings()
    _ensure_default_categories()
    _ensure_default_pages()
    _ensure_default_navigation()
    _ensure_default_attributes()


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


def _find_category_by_slug(slug: str) -> str | None:
    return frappe.db.get_value("Product Category", {"slug": slug}, "name")


def _ensure_default_categories():
    root_name = _find_category_by_slug(ROOT_GROUP["slug"])
    if not root_name:
        doc = frappe.get_doc(
            {
                "doctype": "Product Category",
                "item_group_name": ROOT_GROUP["item_group_name"],
                "slug": ROOT_GROUP["slug"],
                "is_group": ROOT_GROUP["is_group"],
                "display_order": ROOT_GROUP["display_order"],
                "is_active": 1,
            }
        )
        doc.insert(ignore_permissions=True)
        root_name = doc.name

    for row in DEFAULT_GROUPS:
        if _find_category_by_slug(row["slug"]):
            continue
        doc = frappe.get_doc(
            {
                "doctype": "Product Category",
                "item_group_name": row["item_group_name"],
                "slug": row["slug"],
                "parent_item_group": root_name,
                "is_group": 0,
                "display_order": row["display_order"],
                "is_active": 1,
            }
        )
        doc.insert(ignore_permissions=True)


def _ensure_default_pages():
    for page in [
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
    ]:
        if frappe.db.exists("Site Page", {"slug": page["slug"]}):
            continue
        page["doctype"] = "Site Page"
        page["is_published"] = 1
        frappe.get_doc(page).insert(ignore_permissions=True)


def _ensure_default_navigation():
    links = [
        ("Header", "همه محصولات", "/all-products", 10),
        ("Header", "بلاگ", "/blog", 20),
        ("Header", "درباره ما", "/about-us", 30),
        ("Header", "شوروم", "/showroom", 40),
        ("Mobile", "خانه", "/", 10),
        ("Mobile", "محصولات", "/all-products", 20),
        ("Mobile", "بلاگ", "/blog", 30),
        ("Mobile", "تسویه", "/checkout", 40),
    ]
    for placement, label, route, display_order in links:
        if frappe.db.exists("Navigation Link", {"placement": placement, "route": route}):
            continue
        frappe.get_doc(
            {
                "doctype": "Navigation Link",
                "placement": placement,
                "label": label,
                "route": route,
                "display_order": display_order,
                "is_active": 1,
            }
        ).insert(ignore_permissions=True)


def _ensure_default_attributes():
    for title, slug, options in [
        ("رنگ", "color", [("سفید", "white"), ("مشکی", "black")]),
        ("اندازه", "size", [("کوچک", "small"), ("متوسط", "medium"), ("بزرگ", "large")]),
        ("وزن", "weight", [("250 گرم", "250g"), ("500 گرم", "500g"), ("1 کیلوگرم", "1kg")]),
    ]:
        attr = frappe.db.get_value("Product Attribute", {"slug": slug}, "name")
        if not attr:
            attr = frappe.get_doc(
                {
                    "doctype": "Product Attribute",
                    "title": title,
                    "slug": slug,
                    "display_order": 0,
                    "is_filterable": 1,
                    "is_active": 1,
                }
            ).insert(ignore_permissions=True).name
        attr_doc = frappe.get_doc("Product Attribute", attr)
        existing_values = {(row.attribute_value or "").strip() for row in attr_doc.attribute_values or []}
        changed = False
        for idx, (option, option_slug) in enumerate(options, start=1):
            if option not in existing_values:
                attr_doc.append("attribute_values", {"attribute_value": option, "abbr": option_slug})
                existing_values.add(option)
                changed = True

            if frappe.db.exists("Product Attribute Option", {"attribute": attr, "slug": option_slug}):
                continue
            frappe.get_doc(
                {
                    "doctype": "Product Attribute Option",
                    "attribute": attr,
                    "title": option,
                    "slug": option_slug,
                    "display_order": idx,
                    "is_active": 1,
                }
            ).insert(ignore_permissions=True)
        if changed:
            attr_doc.save(ignore_permissions=True)
