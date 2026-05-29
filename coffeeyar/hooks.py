app_name = "coffeeyar"
app_title = "Coffeeyar"
app_publisher = "Sepehr"
app_description = "Minimal coffee storefront for Peakjoy"
app_email = "sepehr.sariaslani@gmail.com"
app_license = "mit"

home_page = "coffee"

website_route_rules = [
    {"from_route": "/", "to_route": "coffee"},
    {"from_route": "/all-products", "to_route": "coffee"},
    {"from_route": "/category/<path:app_path>", "to_route": "coffee"},
    {"from_route": "/about-us", "to_route": "coffee"},
    {"from_route": "/showroom", "to_route": "coffee"},
    {"from_route": "/blog", "to_route": "coffee"},
    {"from_route": "/blog/<path:app_path>", "to_route": "coffee"},
    {"from_route": "/checkout", "to_route": "coffee"},
    {"from_route": "/payment/callback", "to_route": "coffee"},
    {"from_route": "/product/<path:app_path>", "to_route": "coffee"},
]

after_install = "coffeeyar.install.after_install"
