from __future__ import annotations

import frappe

no_cache = 1


def get_context(context):
    from coffeeyar.api_router import handle_request

    # Rewrite /shop/ prefix back to /api/ so the router logic is unchanged
    try:
        path = frappe.local.request.path
        if path.startswith("/shop/"):
            frappe.local.request.path = "/api/" + path[6:]
    except Exception:
        pass

    result = handle_request()
    status_code = getattr(frappe.local.response, "http_status_code", 200)
    frappe.local.response.update({
        "type": "json",
        "data": result,
        "content_type": "application/json",
        "http_status_code": status_code,
    })
    return {}
