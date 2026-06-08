app_name = "coffeeyar"
app_title = "Coffeeyar"
app_publisher = "Sepehr"
app_description = "Minimal coffee storefront for Peakjoy"
app_email = "sepehr.sariaslani@gmail.com"
app_license = "mit"

home_page = "coffee"

website_route_rules = [
    {"from_route": "/shop/<path:app_path>", "to_route": "api_handler"},
    {"from_route": "/<path:app_path>", "to_route": "coffee"},
    {"from_route": "/", "to_route": "coffee"},
]

after_install = "coffeeyar.install.after_install"
