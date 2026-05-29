frappe.ui.form.on("Product Attribute", {
  refresh(frm) {
    frm.trigger("toggle_numeric_fields");
  },
  numeric_values(frm) {
    frm.trigger("toggle_numeric_fields");
    if (frm.doc.numeric_values) {
      frm.clear_table("attribute_values");
      frm.refresh_field("attribute_values");
    }
  },
  toggle_numeric_fields(frm) {
    frm.toggle_display("attribute_values", !frm.doc.numeric_values);
    frm.toggle_display(["from_range", "to_range", "increment"], Boolean(frm.doc.numeric_values));
  },
});
