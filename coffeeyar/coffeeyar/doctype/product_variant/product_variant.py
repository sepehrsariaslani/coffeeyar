import frappe
from frappe import _
from frappe.model.document import Document


class ProductVariant(Document):
    def before_naming(self):
        self.set_missing_identity()

    def before_insert(self):
        self.set_missing_identity()

    def validate(self):
        self.price_toman = max(int(self.price_toman or 0), 0)
        self.discount_toman = max(int(self.discount_toman or 0), 0)
        self.stock_qty = max(int(self.stock_qty or 0), 0)
        self.is_published = 1 if self.is_published else 0

        from coffeeyar.variant import (
            ProductVariantExistsError,
            find_variant,
            make_variant_identity,
            validate_product_variant_attributes,
        )

        validate_product_variant_attributes(self)
        template = frappe.get_doc("Product", self.product)
        make_variant_identity(template, self)

        duplicate = find_variant(self.product, {row.attribute: row.attribute_value for row in self.attributes}, self.name)
        if duplicate:
            frappe.throw(
                _("Product Variant {0} already exists with same attributes").format(duplicate),
                ProductVariantExistsError,
            )

    def set_missing_identity(self):
        if not self.product:
            return
        from coffeeyar.variant import make_variant_identity

        template = frappe.get_doc("Product", self.product)
        make_variant_identity(template, self)
