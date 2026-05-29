from __future__ import annotations

import re

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class ProductAttributeIncrementError(frappe.ValidationError):
    pass


class ProductAttribute(Document):
    def validate(self):
        self.slug = self._clean_slug(self.slug or self.title)
        self.validate_numeric()
        self.validate_duplication()

    def on_update(self):
        self.validate_existing_variants()
        self.set_disabled_in_variants()

    def _clean_slug(self, value: str | None) -> str:
        slug = (value or "").strip().lower()
        slug = re.sub(r"[^a-z0-9\u0600-\u06FF-]+", "-", slug)
        return re.sub(r"-+", "-", slug).strip("-")

    def validate_numeric(self):
        if self.numeric_values:
            self.set("attribute_values", [])
            if self.from_range is None or self.to_range is None:
                frappe.throw(_("Please specify from/to range"))
            if flt(self.from_range) >= flt(self.to_range):
                frappe.throw(_("From Range has to be less than To Range"))
            if not flt(self.increment):
                frappe.throw(_("Increment cannot be 0"), ProductAttributeIncrementError)
        else:
            self.from_range = 0
            self.to_range = 0
            self.increment = 0

    def validate_duplication(self):
        values: list[str] = []
        abbrs: list[str] = []
        for row in self.attribute_values or []:
            value = (row.attribute_value or "").strip()
            abbr = (row.abbr or "").strip()
            row.attribute_value = value
            row.abbr = abbr

            if value.lower() in values:
                frappe.throw(_("Attribute value: {0} must appear only once").format(value))
            values.append(value.lower())

            if abbr.lower() in abbrs:
                frappe.throw(_("Abbreviation: {0} must appear only once").format(abbr))
            abbrs.append(abbr.lower())

    def validate_existing_variants(self):
        if not frappe.db.table_exists("Product Variant Attribute"):
            return

        rows = frappe.get_all(
            "Product Variant Attribute",
            filters={"attribute": self.name, "parenttype": "Product Variant"},
            fields=["parent", "attribute_value"],
        )
        if not rows:
            return

        if self.numeric_values:
            from coffeeyar.variant import validate_is_incremental

            for row in rows:
                if row.attribute_value:
                    validate_is_incremental(self, self.name, row.attribute_value, row.parent)
            return

        allowed = {(row.attribute_value or "").strip() for row in self.attribute_values or []}
        from coffeeyar.variant import validate_product_attribute_value

        for row in rows:
            if row.attribute_value:
                validate_product_attribute_value(allowed, self.name, row.attribute_value, row.parent, from_variant=False)

    def set_disabled_in_variants(self):
        before = self.get_doc_before_save()
        if before and before.disabled == self.disabled:
            return
        if not frappe.db.table_exists("Product Variant Attribute"):
            return

        frappe.db.sql(
            """
            update `tabProduct Variant Attribute`
            set disabled = %(disabled)s
            where attribute = %(attribute)s
            """,
            {"disabled": 1 if self.disabled else 0, "attribute": self.name},
        )
