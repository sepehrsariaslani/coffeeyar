from frappe.model.document import Document


class Order(Document):
    def validate(self):
        subtotal = 0
        for row in self.items or []:
            qty = int(row.qty or 0)
            unit = int(row.unit_price_toman or 0)
            row.row_total_toman = max(qty * unit, 0)
            subtotal += row.row_total_toman

        self.subtotal_toman = max(int(self.subtotal_toman or subtotal), 0)
        self.shipping_fee_toman = max(int(self.shipping_fee_toman or 0), 0)
        self.total_toman = self.subtotal_toman + self.shipping_fee_toman
