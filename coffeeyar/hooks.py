app_name = "coffeeyar"
app_title = "Coffeeyar"
app_publisher = "Sepehr"
app_description = "Minimal coffee storefront for Peakjoy"
app_email = "sepehr.sariaslani@gmail.com"
app_license = "mit"

home_page = "coffee"

website_route_rules = [
    {"from_route": "/api/<path:app_path>", "to_route": "api_handler"},
    {"from_route": "/<path:app_path>", "to_route": "coffee"},
    {"from_route": "/", "to_route": "coffee"},
]

before_request = ["coffeeyar.api_router.before_request_api"]

after_install = "coffeeyar.install.after_install"
