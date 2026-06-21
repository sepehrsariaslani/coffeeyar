import frappe
import json


ROOT_GROUP = {"item_group_name": "محصولات", "slug": "products", "is_group": 1, "display_order": 1}

DEFAULT_GROUPS = [
    {"item_group_name": "محصولات منتخب", "slug": "featured", "display_order": 10},
    {"item_group_name": "کالاهای فیزیکی", "slug": "physical-products", "display_order": 20},
    {"item_group_name": "کالاهای دیجیتال", "slug": "digital-products", "display_order": 30},
    {"item_group_name": "لوازم جانبی", "slug": "accessory", "display_order": 40},
]


def after_install():
    _ensure_settings()
    _ensure_default_categories()
    _ensure_default_pages()
    _ensure_default_navigation()
    _ensure_default_attributes()
    _ensure_default_faqs()
    _ensure_default_policies()
    _ensure_default_page_content()
    _ensure_default_product_global_faqs()
    _ensure_default_brands()
    _ensure_default_theme_config()


def _ensure_settings():
    settings = frappe.get_single("Store Settings")
    if not settings.store_name:
        settings.store_name = "فروشگاه"
    if not settings.home_page:
        settings.home_page = "home"
    if settings.get("shipping_fee_toman") in (None, 0):
        settings.shipping_fee_toman = 120000
    if not settings.zarinpal_request_url:
        settings.zarinpal_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    if not settings.zarinpal_verify_url:
        settings.zarinpal_verify_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    if not settings.zarinpal_startpay_url:
        settings.zarinpal_startpay_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    if settings.use_sandbox is None:
        settings.use_sandbox = 1
    if not settings.get("shipping_standard_price"):
        settings.shipping_standard_price = 45000
    if not settings.get("shipping_standard_free_threshold"):
        settings.shipping_standard_free_threshold = 500000
    if not settings.get("shipping_express_price"):
        settings.shipping_express_price = 90000
    if settings.get("payment_online") is None:
        settings.payment_online = 1
    if settings.get("payment_cod") is None:
        settings.payment_cod = 1
    settings.save(ignore_permissions=True)


def _find_category_by_slug(slug: str) -> str | None:
    return frappe.db.get_value("Product Category", {"slug": slug}, "name")


def _ensure_default_categories():
    root_name = _find_category_by_slug(ROOT_GROUP["slug"])
    if not root_name:
        doc = frappe.get_doc(
            {
                "doctype": "Product Category",
                "item_group_name": ROOT_GROUP["item_group_name"],
                "slug": ROOT_GROUP["slug"],
                "is_group": ROOT_GROUP["is_group"],
                "display_order": ROOT_GROUP["display_order"],
                "is_active": 1,
            }
        )
        doc.insert(ignore_permissions=True)
        root_name = doc.name

    for row in DEFAULT_GROUPS:
        if _find_category_by_slug(row["slug"]):
            continue
        doc = frappe.get_doc(
            {
                "doctype": "Product Category",
                "item_group_name": row["item_group_name"],
                "slug": row["slug"],
                "parent_item_group": root_name,
                "is_group": 0,
                "display_order": row["display_order"],
                "is_active": 1,
            }
        )
        doc.insert(ignore_permissions=True)


def _ensure_default_pages():
    for page in [
        {
            "title": "خانه",
            "slug": "home",
            "page_type": "Home",
            "hero_title": "فروشگاه مینیمال",
            "hero_subtitle": "محصولات منتخب، خرید ساده و پرداخت آنلاین",
            "body_html": "<p>این محتوا از پنل مدیریت قابل ویرایش است.</p>",
        },
        {
            "title": "درباره ما",
            "slug": "about-us",
            "page_type": "Content",
            "hero_title": "درباره ما",
            "body_html": "<p>درباره فروشگاه خود را از پنل مدیریت ویرایش کنید.</p>",
        },
        {
            "title": "شوروم",
            "slug": "showroom",
            "page_type": "Content",
            "hero_title": "شوروم",
            "body_html": "<p>اطلاعات بازدید حضوری را از پنل مدیریت وارد کنید.</p>",
        },
    ]:
        if frappe.db.exists("Site Page", {"slug": page["slug"]}):
            continue
        page["doctype"] = "Site Page"
        page["is_published"] = 1
        frappe.get_doc(page).insert(ignore_permissions=True)


def _ensure_default_navigation():
    links = [
        ("Header", "همه محصولات", "/all-products", 10),
        ("Header", "بلاگ", "/blog", 20),
        ("Header", "درباره ما", "/about-us", 30),
        ("Header", "شوروم", "/showroom", 40),
        ("Mobile", "خانه", "/", 10),
        ("Mobile", "محصولات", "/all-products", 20),
        ("Mobile", "بلاگ", "/blog", 30),
        ("Mobile", "تسویه", "/checkout", 40),
    ]
    for placement, label, route, display_order in links:
        if frappe.db.exists("Navigation Link", {"placement": placement, "route": route}):
            continue
        frappe.get_doc(
            {
                "doctype": "Navigation Link",
                "placement": placement,
                "label": label,
                "route": route,
                "display_order": display_order,
                "is_active": 1,
            }
        ).insert(ignore_permissions=True)


def _ensure_default_attributes():
    for title, slug, options in [
        ("رنگ", "color", [("سفید", "white"), ("مشکی", "black")]),
        ("اندازه", "size", [("کوچک", "small"), ("متوسط", "medium"), ("بزرگ", "large")]),
        ("وزن", "weight", [("250 گرم", "250g"), ("500 گرم", "500g"), ("1 کیلوگرم", "1kg")]),
    ]:
        attr = frappe.db.get_value("Product Attribute", {"slug": slug}, "name")
        if not attr:
            attr = frappe.get_doc(
                {
                    "doctype": "Product Attribute",
                    "title": title,
                    "slug": slug,
                    "display_order": 0,
                    "is_filterable": 1,
                    "is_active": 1,
                }
            ).insert(ignore_permissions=True).name
        attr_doc = frappe.get_doc("Product Attribute", attr)
        existing_values = {(row.attribute_value or "").strip() for row in attr_doc.attribute_values or []}
        changed = False
        for idx, (option, option_slug) in enumerate(options, start=1):
            if option not in existing_values:
                attr_doc.append("attribute_values", {"attribute_value": option, "abbr": option_slug})
                existing_values.add(option)
                changed = True

            if frappe.db.exists("Product Attribute Option", {"attribute": attr, "slug": option_slug}):
                continue
            frappe.get_doc(
                {
                    "doctype": "Product Attribute Option",
                    "attribute": attr,
                    "title": option,
                    "slug": option_slug,
                    "display_order": idx,
                    "is_active": 1,
                }
            ).insert(ignore_permissions=True)
        if changed:
            attr_doc.save(ignore_permissions=True)


def _ensure_default_faqs():
    faqs = [
        {"question": "چگونه می‌توانم سفارش خود را پیگیری کنم؟", "answer": "پس از ثبت سفارش، کد رهگیری برای شما ارسال می‌شود و می‌توانید از طریق صفحه پیگیری سفارش، وضعیت آن را مشاهده کنید.", "display_order": 10},
        {"question": "روش‌های پرداخت چیست؟", "answer": "پرداخت آنلاین از طریق درگاه زرین‌پال و پرداخت در محل برای برخی مناطق قابل انجام است.", "display_order": 20},
        {"question": "چقدر زمان می‌برد تا سفارش به دستم برسد؟", "answer": "ارسال عادی ۲ تا ۴ روز کاری و ارسال اکسپرس ۲۴ ساعته می‌باشد.", "display_order": 30},
        {"question": "آیا می‌توانم سفارش خود را مرجوع کنم؟", "answer": "بله، تا ۷ روز پس از دریافت سفارش می‌توانید درخواست مرجوعی ثبت کنید.", "display_order": 40},
    ]
    for faq in faqs:
        if frappe.db.exists("FAQ", {"question": faq["question"]}):
            continue
        faq["doctype"] = "FAQ"
        faq["is_active"] = 1
        frappe.get_doc(faq).insert(ignore_permissions=True)


def _ensure_default_policies():
    """Seed default policies into Site Policy doctype."""
    if frappe.db.exists("Site Policy", "Site Policy"):
        return

    default_policies = {
        "terms": {
            "title": "شرایط و ضوابط استفاده",
            "content": """با استفاده از این وب‌سایت، شما موافقت خود را با شرایط زیر اعلام می‌کنید.

**۱. استفاده از سایت**
این وب‌سایت صرفاً برای خریداری محصولات ارائه‌شده طراحی شده است. هرگونه استفاده غیرقانونی یا مغایر با این شرایط ممنوع است.

**۲. ثبت‌نام و حساب کاربری**
اطلاعات وارد‌شده در هنگام ثبت‌نام باید دقیق و صحیح باشد. مسئولیت حفظ امنیت رمز عبور به عهده‌ی کاربر است.

**۳. سفارش‌گذاری**
ثبت سفارش به منزله‌ی قبول قیمت و شرایط تحویل درج‌شده است. پس از تأیید سفارش، امکان تغییر وجود ندارد.

**۴. قیمت‌گذاری**
قیمت‌ها به تومان نمایش داده می‌شوند و ممکن است بدون اطلاع قبلی تغییر کنند. قیمت نهایی در زمان تکمیل سفارش ملاک است.

**۵. مالکیت معنوی**
تمامی محتوا، تصاویر، متن‌ها و طراحی این سایت متعلق به فروشگاه است و هرگونه کپی‌برداری بدون اجازه ممنوع است.""",
        },
        "return": {
            "title": "قوانین بازگشت و مرجوعی کالا",
            "content": """**بازگشت کالا در شرایط زیر پذیرفته می‌شود:**

**۱. مهلت مرجوعی**
مشتری تا ۷ روز پس از دریافت کالا می‌تواند درخواست مرجوعی ثبت کند.

**۲. شرایط کالا**
- کالا باید سالم و در بسته‌بندی اصلی باشد.
- کالا نباید استفاده یا باز شده باشد.
- برچسب و کارتن اصلی باید موجود باشد.

**۳. کالاهای غیرقابل مرجوعی**
- مواد غذایی و محصولات فاسدشدنی
- کالاهایی که به درخواست مشتری سفارشی‌سازی شده‌اند
- محصولاتی که بسته‌بندی‌شان باز شده است

**۴. روش بازگشت وجه**
پس از دریافت و تأیید کالا، وجه به همان روش پرداخت (یا کیف‌پول) ظرف ۳ تا ۵ روز کاری عودت داده می‌شود.

**۵. هزینه ارسال مرجوعی**
در صورتی که کالا معیوب یا اشتباه ارسال شده باشد، هزینه ارسال به عهده فروشگاه است. در غیر این صورت هزینه برعهده مشتری است.""",
        },
        "privacy": {
            "title": "سیاست حفظ حریم خصوصی",
            "content": """ما به حریم خصوصی شما احترام می‌گذاریم.

**اطلاعاتی که جمع‌آوری می‌کنیم:**
- نام، شماره تماس و ایمیل برای مدیریت سفارش
- آدرس ارسال برای تحویل کالا
- تاریخچه سفارش برای ارائه‌ی خدمات بهتر

**نحوه استفاده از اطلاعات:**
- پردازش و ارسال سفارش‌ها
- اطلاع‌رسانی درباره وضعیت سفارش
- بهبود تجربه خرید

**اشتراک‌گذاری اطلاعات:**
اطلاعات شخصی شما با هیچ شخص ثالثی بدون اجازه شما به اشتراک گذاشته نمی‌شود، مگر برای انجام سفارش (مثل شرکت پیک).

**امنیت داده:**
اطلاعات شما با استفاده از پروتکل SSL رمزگذاری می‌شود.

**حذف حساب:**
برای حذف اطلاعات خود می‌توانید با پشتیبانی تماس بگیرید.""",
        },
        "shipping": {
            "title": "شرایط ارسال",
            "content": """**ارسال عادی (پست پیشتاز)**
- زمان تحویل: ۲ تا ۴ روز کاری
- هزینه ارسال: ۴۵,۰۰۰ تومان
- ارسال رایگان برای خریدهای بالای ۵۰۰,۰۰۰ تومان

**ارسال اکسپرس (تیپاکس / پیشرو)**
- زمان تحویل: ۲۴ ساعته (مناطق تهران)
- هزینه ارسال: ۹۰,۰۰۰ تومان

**نکات مهم:**
- ارسال به سراسر ایران امکان‌پذیر است.
- سفارش‌های ثبت‌شده تا ساعت ۱۴ روز جاری، همان روز آماده ارسال می‌شوند.
- پس از ارسال، کد رهگیری از طریق SMS ارسال می‌شود.
- برای مناطق دورافتاده ممکن است زمان بیشتری طول بکشد.""",
        },
    }

    frappe.get_doc({
        "doctype": "Site Policy",
        "policies_json": json.dumps(default_policies, ensure_ascii=False),
    }).insert(ignore_permissions=True)


def _ensure_default_page_content():
    """Seed default page content into Page Content doctype."""
    if frappe.db.exists("Page Content", "Page Content"):
        return

    home_content = {
        "heroTag": "مجموعه ۱۴۰۳",
        "heroTitle": "قهوه‌ای که\nمی‌خواستی.",
        "heroSubtitle": "ما دانه‌های تک‌خاستگاه را از مزارع شناخته‌شده تهیه می‌کنیم و در کارگاه کوچک خود تازه برشته می‌کنیم.",
        "heroCtaPrimary": "مشاهده محصولات",
        "heroCtaSecondary": "داستان ما",
        "featuredTag": "منتخب",
        "featuredTitle": "بهترین‌های این فصل",
        "featuredSubtitle": "هر فنجان روایت یک سفر است — از مزرعه تا فنجان شما.",
    }

    about_content = {
        "heroTag": "درباره ما",
        "heroTitle": "قهوه را همان‌طور که هست، دوست داریم.",
        "storyTitle": "داستان ما",
        "storyParagraphs": [
            "نوار سال ۱۴۰۰ در یک کارگاه کوچک متولد شد. باوری ساده داشتیم: قهوه‌ی خوب نباید پیچیده باشد. باید تازه، شفاف و قابل ردیابی باشد.",
            "ما با کشاورزانی همکاری می‌کنیم که با عشق به خاکشان کار می‌کنند، و در کارگاه خودمان دانه‌ها را در دفعات کوچک برشته می‌کنیم تا هر فنجان دقیق‌ترین نسخه‌ی خودش باشد.",
            "امروز هزاران فنجان از نوار در سراسر ایران دم می‌شود — و این تازه آغاز است.",
        ],
        "stats": [
            {"value": "۲۰۰+", "label": "مشتری دائمی"},
            {"value": "۱۲", "label": "خاستگاه فعال"},
            {"value": "۴۸ ساعت", "label": "تازگی تضمینی"},
        ],
        "timeline": [
            {"year": "۱۴۰۰", "title": "آغاز ماجرا", "description": "نوار در یک کارگاه کوچک در تهران با یک رستر ۵ کیلویی و باور به شفافیت زنجیره‌ی قهوه شروع کرد."},
            {"year": "۱۴۰۱", "title": "اولین خاستگاه‌ها", "description": "قراردادهای مستقیم با ۳ مزرعه از اتیوپی و کلمبیا — اول در ایران که قهوه‌ی تک‌خاستگاه با منشأ مشخص عرضه می‌کرد."},
            {"year": "۱۴۰۲", "title": "گسترش کارگاه", "description": "رستر جدید با ظرفیت ۱۵ کیلو، تیم ۶ نفره، و راه‌اندازی فروشگاه آنلاین با ارسال به سراسر ایران."},
            {"year": "۱۴۰۳", "title": "نوار امروز", "description": "بیش از ۲۰۰ مشتری دائمی، ۱۲ خاستگاه فعال، و تضمین تازگی ۴۸ ساعته از لحظه‌ی برشتن تا درِ خانه‌ی شما."},
        ],
        "mission": "ماموریت ما ساده است: قهوه‌ای باکیفیت، شفاف و قابل ردیابی به دست هر کسی که ارزش یک فنجان خوب را می‌داند برسانیم.",
        "vision": "ایران را در نقشه‌ی دنیای قهوه‌ی اسپشیالتی قرار دهیم — نه به‌عنوان مصرف‌کننده، بلکه به‌عنوان بازیگری آگاه و با ذوق.",
        "values": [
            {"title": "شفافیت", "description": "از مزرعه تا فنجان، همه چیز قابل ردیابی است. ما پنهان نمی‌کنیم."},
            {"title": "کیفیت بی‌تعارف", "description": "هیچ دسته‌ای از دانه بدون تأیید تیم ما رست نمی‌شود."},
            {"title": "احترام به کشاورز", "description": "قیمت عادلانه، رابطه‌ی بلندمدت، و دیده‌شدن کسانی که قهوه را می‌رویانند."},
            {"title": "تازگی همیشه", "description": "رست در دفعات کوچک، ارسال سریع، تضمین ۴۸ ساعته."},
        ],
    }

    contact_content = {
        "heroTag": "تماس با ما",
        "heroTitle": "همیشه پاسخگوییم.",
        "address": "تهران، خیابان ولیعصر، کوچه بهار، پلاک ۱۲",
        "phone": "۰۲۱-۸۸۱۲۳۴۵۶",
        "email": "hello@navar.coffee",
        "workingHours": "شنبه تا پنجشنبه، ۹ صبح تا ۶ عصر",
        "mapLat": 35.7219,
        "mapLng": 51.3347,
    }

    frappe.get_doc({
        "doctype": "Page Content",
        "home_hero_json": json.dumps(home_content, ensure_ascii=False),
        "about_json": json.dumps(about_content, ensure_ascii=False),
        "contact_json": json.dumps(contact_content, ensure_ascii=False),
    }).insert(ignore_permissions=True)


def _ensure_default_product_global_faqs():
    """Seed default product global FAQs."""
    if frappe.db.exists("Product Global FAQ Setting", "Product Global FAQ Setting"):
        return

    default_faqs = [
        {
            "id": "shipping",
            "title": "ارسال و بازگشت",
            "content": "ارسال به سراسر ایران در ۲۴ تا ۴۸ ساعت کاری.\nبرای سفارش‌های بالای ۵۰۰ هزار تومان ارسال رایگان است.\nبازگشت کالا تا ۷ روز پس از تحویل با حفظ بسته‌بندی ممکن است.",
            "apply_to": "all",
            "enabled": True,
            "order": 0,
        },
        {
            "id": "warranty",
            "title": "گارانتی و خدمات",
            "content": "تمام اکسسوری‌های نوار با ۶ ماه گارانتی اصالت کالا ارائه می‌شوند.\nدر صورت بروز هر گونه اشکال، با تیم پشتیبانی ما تماس بگیرید.",
            "apply_to": "accessory",
            "enabled": True,
            "order": 1,
        },
        {
            "id": "brew",
            "title": "راهنمای دم‌آوری",
            "content": "برای بهترین تجربه، نسبت ۱:۱۶ (یک گرم قهوه به ۱۶ گرم آب) را پیشنهاد می‌کنیم.\n· دمای آب: ۹۲ تا ۹۴ درجه\n· زمان عصاره‌گیری: ۲ دقیقه و ۳۰ ثانیه\n· نوع آسیاب: متوسط برای V60، درشت برای فرنچ پرس",
            "apply_to": "coffee",
            "enabled": True,
            "order": 2,
        },
        {
            "id": "freshness",
            "title": "تازگی و نگهداری",
            "content": "قهوه‌های نوار بعد از دریافت سفارش برشته می‌شوند.\nبرای حفظ تازگی، در ظرف دربسته و دور از نور و رطوبت نگه‌داری کنید.\nبهترین زمان مصرف: ۷ تا ۳۰ روز پس از تاریخ برشته شدن.",
            "apply_to": "coffee",
            "enabled": True,
            "order": 3,
        },
        {
            "id": "farm",
            "title": "داستان مزرعه",
            "content": "این دانه‌ها از مزارع کوچک کشاورزان خانواده‌محور تهیه شده‌اند.\nنوار با کشاورزان مستقیماً همکاری می‌کند تا قیمت منصفانه و کیفیت یکنواخت تضمین شود.",
            "apply_to": "coffee",
            "enabled": True,
            "order": 4,
        },
    ]

    frappe.get_doc({
        "doctype": "Product Global FAQ Setting",
        "faqs_json": json.dumps(default_faqs, ensure_ascii=False),
    }).insert(ignore_permissions=True)


def _ensure_default_brands():
    """Seed default brands for the marquee."""
    default_brands = [
        {"brand_name": "Tim Wendelboe", "country": "نروژ", "display_order": 1},
        {"brand_name": "Square Mile", "country": "انگلستان", "display_order": 2},
        {"brand_name": "Onyx Coffee Lab", "country": "آمریکا", "display_order": 3},
        {"brand_name": "Intelligentsia", "country": "آمریکا", "display_order": 4},
        {"brand_name": "کافه کتاب", "country": "تهران", "display_order": 5},
        {"brand_name": "Counter Culture", "country": "آمریکا", "display_order": 6},
        {"brand_name": "قهوه آریا", "country": "تهران", "display_order": 7},
        {"brand_name": "Koppi Roasters", "country": "سوئد", "display_order": 8},
        {"brand_name": "قهوه سپید", "country": "اصفهان", "display_order": 9},
        {"brand_name": "Heart Coffee", "country": "پورتلند", "display_order": 10},
        {"brand_name": "کافه نگار", "country": "مشهد", "display_order": 11},
        {"brand_name": "Fuglen Coffee", "country": "اسلو", "display_order": 12},
    ]
    for b in default_brands:
        if frappe.db.exists("Coffee Brand", b["brand_name"]):
            continue
        frappe.get_doc({
            "doctype": "Coffee Brand",
            "brand_name": b["brand_name"],
            "country": b["country"],
            "display_order": b["display_order"],
            "is_active": 1,
        }).insert(ignore_permissions=True)


def _ensure_default_theme_config():
    """Seed default theme config."""
    if frappe.db.exists("Theme Config", "Theme Config"):
        return

    default_theme = {
        "accentHue": 22,
        "accentChroma": 0.09,
        "accentLightness": 0.42,
        "bgLightness": 0.982,
        "bgChroma": 0.006,
        "bgHue": 75,
        "themeClass": "",
    }

    default_layout = {
        "themeName": "minimal",
        "headerVariant": 1,
        "footerVariant": 1,
        "heroVariant": 1,
        "cardVariant": "standard",
        "buttonStyle": "sharp",
        "accentColor": "default",
        "pageDesigns": {},
    }

    frappe.get_doc({
        "doctype": "Theme Config",
        "theme_json": json.dumps(default_theme, ensure_ascii=False),
        "layout_json": json.dumps(default_layout, ensure_ascii=False),
    }).insert(ignore_permissions=True)


def seed_test_data():
    """Seed test coffee products and categories. Can be run multiple times."""
    from frappe.utils import now_datetime

    def create_cat(name, slug, parent=None, icon="☕", color="#8B4513"):
        existing = frappe.db.get_value("Product Category", {"slug": slug})
        if existing:
            return frappe.get_doc("Product Category", existing)
        doc = frappe.get_doc({
            "doctype": "Product Category",
            "item_group_name": name,
            "slug": slug,
            "parent_item_group": parent or "",
            "is_active": 1,
            "icon": icon,
            "color": color,
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return doc

    def create_product(name, slug, category, price, stock=100, discount=0, short_desc="", description="", is_featured=False, origin="", roast=""):
        existing = frappe.db.get_value("Product", {"slug": slug})
        if existing:
            print(f"  ⚠️  {name} already exists, skipping")
            return
        doc = frappe.get_doc({
            "doctype": "Product",
            "item_name": name,
            "slug": slug,
            "item_group": category,
            "price_toman": price,
            "discount_toman": discount,
            "stock_qty": stock,
            "short_description": short_desc,
            "description": description or short_desc,
            "has_variants": 0,
            "is_featured": is_featured,
            "is_published": 1,
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"  ✅ {name}")

    # Root categories
    coffee = create_cat("قهوه", "coffee", icon="☕", color="#8B4513")
    accessories = create_cat("اکسسوری", "accessories", icon="🫖", color="#4A90D9")

    # Sub-categories
    espresso = create_cat("اسپرسو", "espresso", parent=coffee.name)
    filter_coffee = create_cat("قهوه فیلتر", "filter-coffee", parent=coffee.name)
    beans = create_cat("دانه قهوه", "beans", parent=coffee.name)
    instant = create_cat("قهوه فوری", "instant", parent=coffee.name)
    mugs = create_cat("ماگ", "mugs", parent=accessories.name)
    grinders = create_cat("آسیاب", "grinders", parent=accessories.name)

    print("✅ Categories created!")

    # Coffee products
    create_product("قهوه اسپرسو برزیلی", "brazilian-espresso", espresso.name, 450000, 200, 50000, "اسپرسو غنی با طعم شکلات و گردو", "قهوه اسپرسو برزیلی با برشته‌کاری متوسط، طعم شکلات تلخ و گردو. مناسب برای اسپرسوسازهای خانگی و حرفه‌ای.", True, "برزیل", "متوسط")
    create_product("قهوه اتیوپی یيرگاچف", "ethiopia-yirgacheffe", filter_coffee.name, 520000, 150, 0, "قهوه فیلتر با طعم میوه‌ای و گلی", "یکی از بهترین قهوه‌های جهان از منطقه یيرگاچف اتیوپی. با نت‌های میوه‌ای، گل یاس و چای سیاه. برشته‌کاری سبک.", True, "اتیوپی", "سبک")
    create_product("قهوه کلمبیا سوپریمو", "colombia-supremo", beans.name, 380000, 300, 30000, "دانه قهوه کلمبیایی با طعم آجیل و کارامل", "دانه قهوه سوپریمو کلمبیا با کیفیت عالی. طعم آجیل، کارامل و کاکائو. مناسب برای تمام روش‌های دم‌آوری.", False, "کلمبیا", "متوسط-تیره")
    create_product("قهوه گواتمالا آنتیگوا", "guatemala-antigua", espresso.name, 490000, 120, 0, "اسپرسو با طعم دودی و شکلات", "قهوه آنتیگوا گواتمالا با طعم دودی، شکلات تلخ و ادویه. برشته‌کاری تیره. مناسب برای اسپرسو و موکاپات.", False, "گواتمالا", "تیره")
    create_product("قهوه کنیا AA", "kenya-aa", filter_coffee.name, 580000, 80, 0, "قهوه کنیایی با اسیدیته بالا و طعم میوه‌ای", "قهوه کنیا AA با اسیدیته براق، طتم کشمش سیاه، گوجه و گل. یکی از پرفروش‌ترین قهوه‌های تخصصی.", True, "کنیا", "متوسط")
    create_product("قهوه هندونس فوری", "instant-honduras", instant.name, 180000, 500, 20000, "قهوه فوری با طعم ملایم و آجیلی", "قهوه فوری ساخته شده از دانه‌های عربیکا هندوراس. طعم ملایم، آجیلی و کمی شیرین. مناسب برای مصرف سریع.", False, "هندوراس", "متوسط")
    create_product("قهوه پاناما گیشا", "panama-geisha", filter_coffee.name, 1200000, 30, 0, "گیشا افسانه‌ای با طعم گل و چای", "یکی از گران‌ترین و نایاب‌ترین قهوه‌های جهان. گیشا پاناما با طعم گل یاس، چای سیاه، هلو و برگاموت. برشته‌کاری بسیار سبک.", True, "پاناما", "بسیار سبک")
    create_product("قهوه اندونزی سوماترا", "indonesia-sumatra", beans.name, 420000, 180, 0, "دانه قهوه سوماترا با طعم زمینی و ادویه", "قهوه سوماترا با طعم زمینی، ادویه، چوب و کاکائو. برشتهکاری تیره. بدنه سنگین و کرم غلیظ.", False, "اندونزی", "تیره")

    # Accessories
    create_product("ماگ سرامیکی نوار", "navar-ceramic-mug", mugs.name, 280000, 200, 0, "ماگ سرامیکی دست‌ساز با طراحی مینیمال", "ماگ سرامیکی دست‌ساز با ظرفیت 350ml. طراحی مینیمال و شیک. مناسب برای اسپرسو و کاپوچینو.", False, "ایران")
    create_product("آسیاب دستی هاریو", "hario-hand-grinder", grinders.name, 1800000, 50, 200000, "آسیاب دستی هاریو اسکلتون با دنده سرامیکی", "آسیاب دستی هاریو اسکلتون با دنده سرامیکی. قابلیت تنظیم درجه آسیاب. مناسب برای قهوه فیلتر و اسپرسو.", False, "ژاپن")
    create_product("کیف چرمی قهوه", "coffee-leather-bag", accessories.name, 650000, 75, 50000, "کیف چرمی طبیعی برای حمل قهوه و اکسسوری", "کیف چرمی طبیعی برای حمل آسیاب، فیلتر و لوازم قهوه. با جیب‌های متعدد و بند قابل تنظیم.", False, "ایران")

    print("🎉 All test products created!")
