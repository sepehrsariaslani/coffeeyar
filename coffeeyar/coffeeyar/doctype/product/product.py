from __future__ import annotations

import re

from frappe.model.document import Document


class Product(Document):
    def validate(self):
        slug = (self.slug or "").strip().lower()
        if not slug and self.item_name:
            slug = str(self.item_name).strip().lower()
        slug = re.sub(r"[^a-z0-9\u0600-\u06FF-]+", "-", slug)
        slug = re.sub(r"-+", "-", slug).strip("-")
        self.slug = slug

        self.price_toman = max(int(self.price_toman or 0), 0)
        self.discount_toman = max(int(self.discount_toman or 0), 0)
        self.stock_qty = max(int(self.stock_qty or 0), 0)
        self.has_variants = 1 if self.has_variants else 0
        if self.has_variants and not self.variant_based_on:
            self.variant_based_on = "Product Attribute"

        from coffeeyar.variant import validate_template_attributes

        validate_template_attributes(self)
