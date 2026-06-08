from frappe.model.document import Document


class StoreSettings(Document):
    def validate(self):
        self.shipping_fee_toman = max(int(self.shipping_fee_toman or 0), 0)
        self.shipping_standard_price = max(int(getattr(self, 'shipping_standard_price', 0) or 0), 0)
        self.shipping_standard_free_threshold = max(int(getattr(self, 'shipping_standard_free_threshold', 0) or 0), 0)
        self.shipping_express_price = max(int(getattr(self, 'shipping_express_price', 0) or 0), 0)
