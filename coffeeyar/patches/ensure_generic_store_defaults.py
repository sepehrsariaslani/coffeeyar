from __future__ import annotations

import frappe


GENERIC_CATEGORIES = [
    {"item_group_name": "محصولات منتخب", "slug": "featured", "display_order": 10},
    {"item_group_name": "کالاهای فیزیکی", "slug": "physical-products", "display_order": 20},
    {"item_group_name": "کالاهای دیجیتال", "slug": "digital-products", "display_order": 30},
    {"item_group_name": "لوازم جانبی", "slug": "accessory", "display_order": 40},
]

LEGACY_EMPTY_CATEGORY_SLUGS = ["coffee-beans", "brew-gear", "drip-bags"]


def execute():
    root = _ensure_category("محصولات", "products", is_group=1)
    for row in GENERIC_CATEGORIES:
        if frappe.db.exists("Product Category", {"slug": row["slug"]}):
            continue
        doc = frappe.get_doc(
            {
                "doctype": "Product Category",
                "item_group_name": row["item_group_name"],
                "slug": row["slug"],
                "parent_item_group": root,
                "is_group": 0,
                "is_active": 1,
                "display_order": row["display_order"],
            }
        )
        doc.insert(ignore_permissions=True)

    for slug in LEGACY_EMPTY_CATEGORY_SLUGS:
        category = frappe.db.get_value("Product Category", {"slug": slug}, "name")
        if category and not frappe.db.count("Product", {"item_group": category}):
            frappe.db.set_value("Product Category", category, "is_active", 0, update_modified=False)


def _ensure_category(title: str, slug: str, is_group: int = 0) -> str:
    existing = frappe.db.get_value("Product Category", {"slug": slug}, "name")
    if existing:
        return existing
    doc = frappe.get_doc(
        {
            "doctype": "Product Category",
            "item_group_name": title,
            "slug": slug,
            "is_group": is_group,
            "is_active": 1,
            "display_order": 0,
        }
    )
    doc.insert(ignore_permissions=True)
    return doc.name

