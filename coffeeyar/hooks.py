app_name = "coffeeyar"
app_title = "Coffeeyar"
app_publisher = "Sepehr"
app_description = "Minimal coffee storefront for Peakjoy"
app_email = "sepehr.sariaslani@gmail.com"
app_license = "mit"

home_page = "coffee"

website_route_rules = [
    {"from_route": "/_api/<path:app_path>", "to_route": "api_handler"},
    {"from_route": "/desk", "to_route": "desk"},
    {"from_route": "/desk/<path:app_path>", "to_route": "desk"},
    {"from_route": "/login", "to_route": "login"},
    {"from_route": "/login/<path:app_path>", "to_route": "login"},
    {"from_route": "/password-update", "to_route": "password-update"},
    {"from_route": "/me", "to_route": "me"},
    {"from_route": "/print", "to_route": "print"},
    {"from_route": "/", "to_route": "coffee"},
    {"from_route": "/<path:app_path>", "to_route": "coffee"},
]

before_request = ["coffeeyar.api.before_request_api"]
page_renderer = ["coffeeyar.api.ApiRenderer"]

after_install = "coffeeyar.install.after_install"
