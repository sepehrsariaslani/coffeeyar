from __future__ import annotations

import re

from frappe.model.document import Document


class ProductCategory(Document):
    def validate(self):
        slug = (self.slug or "").strip().lower()
        if not slug and self.item_group_name:
            slug = str(self.item_group_name).strip().lower()
        slug = re.sub(r"[^a-z0-9\u0600-\u06FF-]+", "-", slug)
        slug = re.sub(r"-+", "-", slug).strip("-")
        self.slug = slug
