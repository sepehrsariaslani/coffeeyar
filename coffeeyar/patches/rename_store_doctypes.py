from __future__ import annotations

import frappe
from frappe import _


RENAMES = [
    ("Kala Item Group", "Product Category"),
    ("Kala Item", "Product"),
    ("Coffee Order Item", "Order Item"),
    ("Coffee Order", "Order"),
    ("Coffee Settings", "Store Settings"),
]


def execute():
    for old, new in RENAMES:
        old_exists = frappe.db.exists("DocType", old)
        new_exists = frappe.db.exists("DocType", new)
        if old_exists and new_exists:
            frappe.throw(
                _("Cannot rename {0} to {1}: both DocTypes already exist. Resolve the duplicate first.").format(
                    old, new
                )
            )
        if old_exists and not new_exists:
            frappe.rename_doc("DocType", old, new, force=True)
