import frappe
from frappe.utils import get_system_timezone


no_cache = 1


def get_context(context):
    csrf_token = frappe.sessions.get_csrf_token()
    frappe.db.commit()

    context.boot = get_boot()
    context.boot["csrf_token"] = csrf_token
    return context


@frappe.whitelist(methods=["GET"], allow_guest=True)
def get_context_for_dev():
    return get_boot()


def get_boot():
    from coffeeyar.api import _get_settings

    settings = _get_settings()
    return frappe._dict(
        {
            "site_name": frappe.local.site,
            "store_name": settings.store_name or "فروشگاه",
            "system_timezone": get_system_timezone(),
            "user": frappe.session.user,
            "shipping_fee_toman": int(settings.shipping_fee_toman or 120000),
            "use_sandbox": int(settings.use_sandbox or 0),
        }
    )
