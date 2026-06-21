from __future__ import annotations

import re

import frappe


def execute():
    if not frappe.db.table_exists("Product Attribute"):
        return

    migrate_attribute_options()
    migrate_variant_attribute_values()


def _abbr(value: str, used: set[str]) -> str:
    base = (value or "").strip()
    base = re.sub(r"\s+", "-", base)
    base = re.sub(r"[^a-zA-Z0-9\u0600-\u06FF-]+", "-", base).strip("-")
    base = (base or "VAL")[:20]
    candidate = base
    index = 2
    while candidate.lower() in used:
        suffix = f"-{index}"
        candidate = f"{base[:20 - len(suffix)]}{suffix}"
        index += 1
    used.add(candidate.lower())
    return candidate


def migrate_attribute_options():
    if not frappe.db.table_exists("Product Attribute Option"):
        return

    options = frappe.get_all(
        "Product Attribute Option",
        fields=["name", "attribute", "title", "slug", "display_order"],
        order_by="attribute asc, display_order asc, creation asc",
    )
    by_attribute: dict[str, list] = {}
    for option in options:
        by_attribute.setdefault(option.attribute, []).append(option)

    for attribute, rows in by_attribute.items():
        if not frappe.db.exists("Product Attribute", attribute):
            continue
        doc = frappe.get_doc("Product Attribute", attribute)
        existing_values = {(row.attribute_value or "").strip().lower() for row in doc.attribute_values or []}
        used_abbrs = {(row.abbr or "").strip().lower() for row in doc.attribute_values or []}
        changed = False

        for option in rows:
            value = (option.title or option.slug or option.name or "").strip()
            if not value or value.lower() in existing_values:
                continue
            doc.append(
                "attribute_values",
                {
                    "attribute_value": value,
                    "abbr": _abbr(option.slug or value, used_abbrs),
                },
            )
            existing_values.add(value.lower())
            changed = True

        if changed:
            doc.save(ignore_permissions=True)


def migrate_variant_attribute_values():
    if not frappe.db.table_exists("Product Variant Attribute"):
        return

    rows = frappe.get_all(
        "Product Variant Attribute",
        filters={"attribute_value": ["in", ["", None]]},
        fields=["name", "option", "option_title", "attribute"],
    )
    for row in rows:
        value = row.option_title
        if not value and row.option and frappe.db.table_exists("Product Attribute Option"):
            value = frappe.db.get_value("Product Attribute Option", row.option, "title")
        if not value:
            continue
        frappe.db.set_value("Product Variant Attribute", row.name, "attribute_value", value, update_modified=False)

    # Backfill fetched metadata for both product-template rows and variant rows.
    rows = frappe.get_all(
        "Product Variant Attribute",
        fields=["name", "attribute"],
    )
    for row in rows:
        if not row.attribute:
            continue
        values = frappe.db.get_value(
            "Product Attribute",
            row.attribute,
            ["title", "numeric_values", "from_range", "to_range", "increment", "disabled"],
            as_dict=True,
        )
        if not values:
            continue
        frappe.db.set_value(
            "Product Variant Attribute",
            row.name,
            {
                "attribute_title": values.title,
                "numeric_values": values.numeric_values,
                "from_range": values.from_range,
                "to_range": values.to_range,
                "increment": values.increment,
                "disabled": values.disabled,
            },
            update_modified=False,
        )
