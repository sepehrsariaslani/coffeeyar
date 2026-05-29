frappe.ui.form.on("Product Variant", {
  refresh(frm) {
    frm.set_query("product", () => ({ filters: { has_variants: 1 } }));
  },

  product(frm) {
    if (!frm.doc.product) return;
    if (!frm.doc.attributes?.length) {
      frappe.call({
        method: "coffeeyar.variant.get_attribute_values_for_product",
        args: { product: frm.doc.product },
        callback(r) {
          const attrs = r.message || [];
          frm.clear_table("attributes");
          attrs.forEach((attr) => {
            const row = frm.add_child("attributes");
            row.variant_of = frm.doc.product;
            row.attribute = attr.attribute;
            row.attribute_title = attr.title;
            row.numeric_values = attr.numeric_values;
            row.from_range = attr.from_range;
            row.to_range = attr.to_range;
            row.increment = attr.increment;
          });
          frm.refresh_field("attributes");
        },
      });
    }
  },
});
