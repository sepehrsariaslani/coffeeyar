from __future__ import annotations

import frappe
from frappe.utils.nestedset import rebuild_tree


def execute():
    root = frappe.db.get_value("Product Category", {"slug": "products"}, "name")
    if not root:
        return

    for slug in ["featured", "physical-products", "digital-products", "accessory"]:
        category = frappe.db.get_value("Product Category", {"slug": slug}, "name")
        if category and category != root:
            frappe.db.set_value(
                "Product Category",
                category,
                {"parent_item_group": root, "is_group": 0, "is_active": 1},
                update_modified=False,
            )

    rebuild_tree("Product Category")
