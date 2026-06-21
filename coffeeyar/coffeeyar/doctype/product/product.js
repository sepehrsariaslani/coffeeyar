frappe.ui.form.on("Product", {
  refresh(frm) {
    frm.trigger("toggle_variant_fields");
    if (!frm.is_new() && frm.doc.has_variants) {
      frm.add_custom_button(__("ساخت یک تنوع"), () => show_single_variant_dialog(frm), __("تنوع‌ها"));
      frm.add_custom_button(__("ساخت چند تنوع"), () => show_multiple_variants_dialog(frm), __("تنوع‌ها"));
      frm.add_custom_button(__("مشاهده تنوع‌ها"), () => {
        frappe.set_route("List", "Product Variant", { product: frm.doc.name });
      }, __("تنوع‌ها"));
    }
  },

  has_variants(frm) {
    frm.trigger("toggle_variant_fields");
  },

  variant_based_on(frm) {
    frm.trigger("toggle_variant_fields");
  },

  toggle_variant_fields(frm) {
    const show = Boolean(frm.doc.has_variants && frm.doc.variant_based_on === "Product Attribute");
    frm.toggle_display("attributes", show);
    if (!frm.doc.variant_based_on) {
      frm.set_value("variant_based_on", "Product Attribute");
    }
  },
});

frappe.ui.form.on("Product Variant Attribute", {
  attribute(frm, cdt, cdn) {
    const row = locals[cdt][cdn];
    if (!row.attribute) return;

    frappe.db.get_value(
      "Product Attribute",
      row.attribute,
      ["title", "numeric_values", "from_range", "to_range", "increment", "disabled"],
    ).then((r) => {
      const value = r.message || {};
      frappe.model.set_value(cdt, cdn, "attribute_title", value.title || row.attribute);
      frappe.model.set_value(cdt, cdn, "numeric_values", value.numeric_values || 0);
      frappe.model.set_value(cdt, cdn, "from_range", value.from_range || 0);
      frappe.model.set_value(cdt, cdn, "to_range", value.to_range || 0);
      frappe.model.set_value(cdt, cdn, "increment", value.increment || 0);
      frappe.model.set_value(cdt, cdn, "disabled", value.disabled || 0);
      if (frm.doc.doctype === "Product") {
        frappe.model.set_value(cdt, cdn, "variant_of", frm.doc.name);
      }
    });
  },
});

function get_product_attributes(frm) {
  return frappe.call({
    method: "coffeeyar.variant.get_attribute_values_for_product",
    args: { product: frm.doc.name },
  }).then((r) => r.message || []);
}

async function show_single_variant_dialog(frm) {
  const attributes = await get_product_attributes(frm);
  if (!attributes.length) {
    frappe.msgprint(__("ابتدا ویژگی‌های تنوع را در جدول محصول تعریف کنید."));
    return;
  }

  const fields = attributes.map((attr) => {
    if (attr.numeric_values) {
      return {
        fieldname: attr.attribute,
        fieldtype: "Float",
        label: `${attr.title} (${attr.from_range} تا ${attr.to_range})`,
        reqd: 1,
        description: attr.increment ? `${__("گام")}: ${attr.increment}` : "",
      };
    }

    return {
      fieldname: attr.attribute,
      fieldtype: "Select",
      label: attr.title,
      options: (attr.values || []).map((row) => row.value).join("\n"),
      reqd: 1,
    };
  });

  fields.push({ fieldname: "use_template_image", fieldtype: "Check", label: __("استفاده از تصویر محصول قالب"), default: 1 });

  const dialog = new frappe.ui.Dialog({
    title: __("ساخت یک تنوع"),
    fields,
    primary_action_label: __("ساخت تنوع"),
    primary_action(values) {
      const args = {};
      attributes.forEach((attr) => {
        args[attr.attribute] = values[attr.attribute];
      });
      frappe.call({
        method: "coffeeyar.variant.create_variant",
        args: {
          product: frm.doc.name,
          args,
          use_template_image: values.use_template_image ? 1 : 0,
        },
        freeze: true,
        callback(r) {
          const result = r.message || {};
          dialog.hide();
          if (result.name) {
            frappe.set_route("Form", "Product Variant", result.name);
          }
        },
      });
    },
  });

  dialog.show();
}

async function show_multiple_variants_dialog(frm) {
  const attributes = await get_product_attributes(frm);
  const selectable = attributes.filter((attr) => !attr.numeric_values);
  const skipped = attributes.filter((attr) => attr.numeric_values);

  if (!selectable.length) {
    frappe.msgprint(__("ساخت گروهی برای ویژگی‌های عددی پشتیبانی نمی‌شود. از ساخت یک تنوع استفاده کنید."));
    return;
  }

  const fields = [];
  if (skipped.length) {
    fields.push({
      fieldname: "numeric_note",
      fieldtype: "HTML",
      options: `<p class="text-muted">${__("ویژگی‌های عددی در ساخت گروهی نادیده گرفته می‌شوند؛ برای آن‌ها تنوع تکی بسازید.")}</p>`,
    });
  }

  selectable.forEach((attr) => {
    fields.push({
      fieldname: attr.attribute,
      fieldtype: "MultiCheck",
      label: attr.title,
      columns: 2,
      options: (attr.values || []).map((row) => ({ label: row.value, value: row.value })),
    });
  });
  fields.push({ fieldname: "use_template_image", fieldtype: "Check", label: __("استفاده از تصویر محصول قالب"), default: 1 });

  const dialog = new frappe.ui.Dialog({
    title: __("ساخت چند تنوع"),
    fields,
    primary_action_label: __("ساخت تنوع‌ها"),
    primary_action(values) {
      const args = {};
      let total = 1;
      selectable.forEach((attr) => {
        const selected = values[attr.attribute] || [];
        args[attr.attribute] = selected;
        total *= selected.length || 0;
      });

      if (!total) {
        frappe.msgprint(__("از هر ویژگی حداقل یک مقدار انتخاب کنید."));
        return;
      }
      if (total > 500) {
        frappe.msgprint(__("بیشتر از ۵۰۰ تنوع را یک‌جا نسازید."));
        return;
      }

      frappe.call({
        method: "coffeeyar.variant.create_multiple_variants",
        args: {
          product: frm.doc.name,
          args,
          use_template_image: values.use_template_image ? 1 : 0,
        },
        freeze: true,
        callback(r) {
          const result = r.message || {};
          dialog.hide();
          frappe.msgprint(__("{0} تنوع ساخته شد. {1} تنوع از قبل وجود داشت.", [result.created || 0, result.existing || 0]));
          frappe.set_route("List", "Product Variant", { product: frm.doc.name });
        },
      });
    },
  });

  dialog.show();
}
