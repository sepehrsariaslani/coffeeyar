from __future__ import annotations

import copy
import json
import re
from itertools import product as cartesian_product
from typing import Any

import frappe
from frappe import _
from frappe.utils import cint, cstr, flt


class ProductVariantExistsError(frappe.ValidationError):
    pass


class InvalidProductAttributeValueError(frappe.ValidationError):
    pass


class ProductAttributeIncrementError(frappe.ValidationError):
    pass


def _parse_args(args: str | dict[str, Any] | None) -> dict[str, Any]:
    if isinstance(args, str):
        args = json.loads(args) if args.strip() else {}
    args = args or {}
    return {cstr(k): v for k, v in args.items() if k != "use_template_image"}


def _normalize_value(value: Any) -> str:
    return cstr(value).strip()


def _slug_part(value: str) -> str:
    value = _normalize_value(value).lower().replace("_", "-")
    value = re.sub(r"[^a-z0-9\u0600-\u06FF-]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")


def _get_template(product: str | frappe.model.document.Document) -> frappe.model.document.Document:
    template = frappe.get_doc("Product", product) if isinstance(product, str) else product
    if not cint(template.has_variants):
        frappe.throw(_("Product {0} is not marked as a variant template").format(template.name))
    return template


def _template_attribute_names(template: frappe.model.document.Document) -> list[str]:
    names = []
    for row in template.attributes or []:
        if row.attribute and row.attribute not in names:
            names.append(row.attribute)
    return names


def _attribute_doc(attribute: str) -> frappe.model.document.Document:
    return frappe.get_doc("Product Attribute", attribute)


def _attribute_title(attribute: str) -> str:
    return frappe.db.get_value("Product Attribute", attribute, "title") or attribute


def _attribute_allowed_values(attribute_doc: frappe.model.document.Document) -> set[str]:
    return {_normalize_value(row.attribute_value) for row in attribute_doc.attribute_values or []}


def _attribute_abbreviation(attribute: str, value: str) -> str:
    attr = _attribute_doc(attribute)
    if cint(attr.numeric_values):
        return _slug_part(value) or value

    for row in attr.attribute_values or []:
        if _normalize_value(row.attribute_value) == _normalize_value(value):
            return _normalize_value(row.abbr) or _slug_part(value) or value
    return _slug_part(value) or value


def validate_is_incremental(numeric_attribute, attribute: str, value: Any, item: str):
    from_range = flt(numeric_attribute.from_range)
    to_range = flt(numeric_attribute.to_range)
    increment = flt(numeric_attribute.increment)
    numeric_value = flt(value)

    if not increment:
        frappe.throw(_("Increment for Attribute {0} cannot be 0").format(attribute), ProductAttributeIncrementError)

    is_in_range = from_range <= numeric_value <= to_range
    precision = max(len(cstr(v).split(".")[-1].rstrip("0")) for v in (numeric_value, increment))
    remainder = flt((numeric_value - from_range) % increment, precision)
    is_incremental = remainder == 0 or remainder == increment

    if not (is_in_range and is_incremental):
        frappe.throw(
            _(
                "Value for Attribute {0} must be within the range of {1} to {2} in the increments of {3} for Product {4}"
            ).format(attribute, from_range, to_range, increment, item),
            InvalidProductAttributeValueError,
            title=_("Invalid Attribute"),
        )


def validate_product_attribute_value(
    allowed_values, attribute: str, attribute_value: Any, item: str, from_variant: bool = True
):
    normalized_value = _normalize_value(attribute_value)
    allowed = {_normalize_value(value) for value in allowed_values}
    if normalized_value in allowed:
        return

    if from_variant:
        frappe.throw(
            _("{0} is not a valid Value for Attribute {1} of Product {2}.").format(
                frappe.bold(normalized_value), frappe.bold(attribute), frappe.bold(item)
            ),
            InvalidProductAttributeValueError,
            title=_("Invalid Value"),
        )

    frappe.throw(
        _("The value {0} is already assigned to an existing Product Variant {1}.").format(
            frappe.bold(normalized_value), frappe.bold(item)
        ),
        InvalidProductAttributeValueError,
        title=_("Edit Not Allowed"),
    )


def _validate_template_attribute_rows(template: frappe.model.document.Document):
    seen = set()
    for row in template.attributes or []:
        if not row.attribute:
            continue
        if row.attribute in seen:
            frappe.throw(_("Each attribute can be selected only once per product template"))
        seen.add(row.attribute)

        attr = _attribute_doc(row.attribute)
        if cint(attr.disabled):
            frappe.throw(_("Attribute {0} is disabled").format(attr.title or attr.name))
        row.variant_of = template.name
        row.attribute_title = attr.title
        row.numeric_values = cint(attr.numeric_values)
        row.from_range = flt(attr.from_range)
        row.to_range = flt(attr.to_range)
        row.increment = flt(attr.increment)
        row.disabled = cint(attr.disabled)

    if cint(template.has_variants) and not seen:
        frappe.throw(_("Please specify at least one attribute in the Variant Attributes table"))


def validate_template_attributes(template: frappe.model.document.Document):
    if not cint(template.has_variants):
        return
    _validate_template_attribute_rows(template)


def validate_product_variant_attributes(item, args: str | dict[str, Any] | None = None):
    variant = frappe.get_doc("Product Variant", item) if isinstance(item, str) else item
    template = _get_template(variant.product)
    _validate_template_attribute_rows(template)

    template_attributes = _template_attribute_names(template)
    if args is None:
        args = {row.attribute: row.attribute_value or row.option_title for row in variant.attributes or []}
    else:
        args = _parse_args(args)

    normalized_args = {attribute: _normalize_value(value) for attribute, value in args.items() if _normalize_value(value)}
    extra = [attribute for attribute in normalized_args if attribute not in template_attributes]
    if extra:
        frappe.throw(_("Attributes {0} are not part of Product Template {1}").format(", ".join(extra), template.name))

    missing = [attribute for attribute in template_attributes if not normalized_args.get(attribute)]
    if missing:
        frappe.throw(_("Please specify values for attributes: {0}").format(", ".join(missing)))

    rows = []
    for attribute in template_attributes:
        value = normalized_args[attribute]
        attr = _attribute_doc(attribute)
        if cint(attr.disabled):
            frappe.throw(_("Attribute {0} is disabled").format(attr.title or attr.name))

        if cint(attr.numeric_values):
            validate_is_incremental(attr, attribute, value, variant.name or template.name)
        else:
            validate_product_attribute_value(
                _attribute_allowed_values(attr), attribute, value, variant.name or template.name, from_variant=True
            )

        rows.append(
            {
                "variant_of": template.name,
                "attribute": attribute,
                "attribute_value": value,
                "attribute_title": attr.title,
                "option_title": value,
                "numeric_values": cint(attr.numeric_values),
                "from_range": flt(attr.from_range),
                "to_range": flt(attr.to_range),
                "increment": flt(attr.increment),
                "disabled": cint(attr.disabled),
            }
        )

    variant.set("attributes", rows)


def find_variant(product: str, args: str | dict[str, Any], variant: str | None = None) -> str | None:
    template = _get_template(product)
    normalized_args = {key: _normalize_value(value) for key, value in _parse_args(args).items() if _normalize_value(value)}
    if not normalized_args:
        return None

    candidates = frappe.get_all("Product Variant", filters={"product": template.name}, pluck="name")
    for candidate_name in candidates:
        if variant and candidate_name == variant:
            continue
        candidate = frappe.get_doc("Product Variant", candidate_name)
        candidate_args = {
            row.attribute: _normalize_value(row.attribute_value or row.option_title)
            for row in candidate.attributes or []
            if row.attribute
        }
        if candidate_args == normalized_args:
            return candidate.name
    return None


def make_variant_identity(template: frappe.model.document.Document, variant: frappe.model.document.Document):
    parts = []
    values = []
    for row in variant.attributes or []:
        value = _normalize_value(row.attribute_value or row.option_title)
        if not value:
            continue
        parts.append(_attribute_abbreviation(row.attribute, value))
        values.append(value)

    if not variant.title:
        suffix = " / ".join(values)
        variant.title = f"{template.item_name} - {suffix}" if suffix else template.item_name

    if not variant.sku:
        base = _normalize_value(template.sku) or _normalize_value(template.slug) or _normalize_value(template.name)
        suffix = "-".join(_slug_part(part) for part in parts if _slug_part(part))
        variant.sku = f"{base}-{suffix}" if suffix else base


def copy_template_to_variant(
    template: frappe.model.document.Document, variant: frappe.model.document.Document, use_template_image: bool = False
):
    variant.product = template.name
    if use_template_image and template.image:
        variant.image = template.image
    if variant.price_toman in (None, ""):
        variant.price_toman = 0
    if variant.discount_toman in (None, ""):
        variant.discount_toman = 0
    if variant.stock_qty in (None, ""):
        variant.stock_qty = 0
    if not variant.is_published:
        variant.is_published = 1


def generate_keyed_value_combinations(args: str | dict[str, list[Any]]) -> list[dict[str, Any]]:
    parsed = _parse_args(args)
    keys = [key for key, values in parsed.items() if values]
    if not keys:
        return []

    values_matrix = []
    for key in keys:
        values = parsed[key]
        if not isinstance(values, list):
            values = [values]
        values_matrix.append(values)

    return [dict(zip(keys, values)) for values in cartesian_product(*values_matrix)]


@frappe.whitelist()
def get_variant(product: str, args: str | dict[str, Any] | None = None, variant: str | None = None):
    args = _parse_args(args)
    if not args:
        frappe.throw(_("Please specify at least one attribute in the Attributes table"))
    return find_variant(product, args, variant)


@frappe.whitelist()
def create_variant(product: str, args: str | dict[str, Any], use_template_image: bool | str = False):
    template = _get_template(product)
    args = _parse_args(args)
    use_template_image = bool(cint(use_template_image))

    existing = find_variant(template.name, args)
    if existing:
        return {"name": existing, "existing": 1}

    variant = frappe.new_doc("Product Variant")
    copy_template_to_variant(template, variant, use_template_image=use_template_image)
    validate_product_variant_attributes(variant, args)
    make_variant_identity(template, variant)
    variant.insert()
    return {"name": variant.name, "existing": 0}


@frappe.whitelist()
def create_multiple_variants(product: str, args: str | dict[str, list[Any]], use_template_image: bool | str = False):
    template = _get_template(product)
    combinations = generate_keyed_value_combinations(args)
    total = len(combinations)
    if not total:
        frappe.throw(_("Select at least one value from each attribute."))
    if total > 500:
        frappe.throw(_("Please do not create more than 500 variants at a time"))

    use_template_image = bool(cint(use_template_image))
    created = 0
    existing = 0
    for combination in combinations:
        if find_variant(template.name, combination):
            existing += 1
            continue
        variant = frappe.new_doc("Product Variant")
        copy_template_to_variant(template, variant, use_template_image=use_template_image)
        validate_product_variant_attributes(variant, copy.deepcopy(combination))
        make_variant_identity(template, variant)
        variant.insert()
        created += 1

    return {"created": created, "existing": existing, "total": total}


@frappe.whitelist()
def get_attribute_values_for_product(product: str):
    template = _get_template(product)
    out = []
    for row in template.attributes or []:
        if not row.attribute:
            continue
        attr = _attribute_doc(row.attribute)
        item = {
            "attribute": attr.name,
            "title": attr.title,
            "numeric_values": cint(attr.numeric_values),
            "from_range": flt(attr.from_range),
            "to_range": flt(attr.to_range),
            "increment": flt(attr.increment),
            "values": [],
        }
        if not cint(attr.numeric_values):
            item["values"] = [
                {"value": _normalize_value(value.attribute_value), "abbr": _normalize_value(value.abbr)}
                for value in attr.attribute_values or []
            ]
        out.append(item)
    return out
