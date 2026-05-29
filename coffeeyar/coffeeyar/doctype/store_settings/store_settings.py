from frappe.model.document import Document


class StoreSettings(Document):
    def validate(self):
        self.shipping_fee_toman = max(int(self.shipping_fee_toman or 0), 0)
