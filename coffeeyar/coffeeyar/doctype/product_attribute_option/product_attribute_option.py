from __future__ import annotations

import re

from frappe.model.document import Document


class ProductAttributeOption(Document):
    def validate(self):
        slug = (self.slug or "").strip().lower()
        if not slug and self.title:
            slug = str(self.title).strip().lower()
        slug = re.sub(r"[^a-z0-9\u0600-\u06FF-]+", "-", slug)
        slug = re.sub(r"-+", "-", slug).strip("-")
        self.slug = slug
