import frappe
from frappe.utils import get_system_timezone

no_cache = 1

def get_context(context):
    # Don't serve the SPA shell for static asset paths — let Frappe's
    # built-in static file server handle them. Without this guard the
    # catch-all route rule in hooks.py would intercept every
    # /assets/coffeeyar/frontend/assets/*.js request and return HTML,
    # causing MIME-type errors in the browser.
    path = getattr(frappe.local.request, "path", "")
    if path.startswith(("/assets/", "/_", "/files/", "/private/")):
        frappe.throw(frappe._("Not Found"), frappe.DoesNotExistError)

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
