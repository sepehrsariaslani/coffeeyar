import frappe
from frappe.utils import now_datetime

# ── 1. Create categories ──
def create_cat(name, slug, parent=None, icon="☕", color="#8B4513"):
    if frappe.db.exists("Product Category", {"slug": slug}):
        return frappe.get_doc("Product Category", {"slug": slug})
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
    return doc

# Root categories
coffee = create_cat("قهوه", "coffee", icon="☕", color="#8B4513")
accessories = create_cat("اکسسوری", "accessories", icon="🫖", color="#4A90D9")
equipment = create_cat("تجهیزات", "equipment", icon="⚙️", color="#6B7280")

# Sub-categories for coffee
espresso = create_cat("اسپرسو", "espresso", parent=coffee.name, icon="☕", color="#8B4513")
filter_coffee = create_cat("قهوه فیلتر", "filter-coffee", parent=coffee.name, icon="☕", color="#A0522D")
beans = create_cat("دانه قهوه", "beans", parent=coffee.name, icon="🫘", color="#654321")
instant = create_cat("قهوه فوری", "instant", parent=coffee.name, icon="⚡", color="#D2691E")

# Sub-categories for accessories
mugs = create_cat("ماگ", "mugs", parent=accessories.name, icon="🍵", color="#4A90D9")
grinders = create_cat("آسیاب", "grinders", parent=accessories.name, icon="🔧", color="#6B7280")

print("✅ Categories created!")

# ── 2. Create products ──
def create_product(name, slug, category, price, stock=100, discount=0, short_desc="", description="", image="", has_variants=False, is_featured=False, origin="", roast="", notes=None):
    if frappe.db.exists("Product", {"slug": slug}):
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
        "image": image,
        "has_variants": has_variants,
        "is_featured": is_featured,
        "is_published": 1,
        "display_order": 0,
    })
    doc.insert(ignore_permissions=True)
    print(f"  ✅ {name}")

# Coffee products
create_product(
    "قهوه اسپرسو برزیلی", "brazilian-espresso", espresso.name,
    price=450000, stock=200, discount=50000,
    short_desc="اسپرسو غنی با طعم شکلات و گردو",
    description="قهوه اسپرسو برزیلی با برشته‌کاری متوسط، طعم شکلات تلخ و گردو. مناسب برای اسپرسوسازهای خانگی و حرفه‌ای.",
    is_featured=True, origin="برزیل", roast="متوسط",
    notes=["شکلات تلخ", "گردو", "کرم غلیظ"]
)

create_product(
    "قهوه اتیوپی یيرگاچف", "ethiopia-yirgacheffe", filter_coffee.name,
    price=520000, stock=150, discount=0,
    short_desc="قهوه فیلتر با طعم میوه‌ای و گلی",
    description="یکی از بهترین قهوه‌های جهان از منطقه یيرگاچف اتیوپی. با نت‌های میوه‌ای، گل یاس و چای سیاه. برشته‌کاری سبک.",
    is_featured=True, origin="اتیوپی", roast="سبک",
    notes=["گل یاس", "بلوبری", "چای سیاه"]
)

create_product(
    "قهوه کلمبیا سوپریمو", "colombia-supremo", beans.name,
    price=380000, stock=300, discount=30000,
    short_desc="دانه قهوه کلمبیایی با طعم آجیل و کارامل",
    description="دانه قهوه سوپریمو کلمبیا با کیفیت عالی. طعم آجیل، کارامل و کاکائو. مناسب برای تمام روش‌های دم‌آوری.",
    origin="کلمبیا", roast="متوسط-تیره",
    notes=["کارامل", "گردو", "کاکائو"]
)

create_product(
    "قهوه گواتمالا آنتیگوا", "guatemala-antigua", espresso.name,
    price=490000, stock=120, discount=0,
    short_desc="اسپرسو با طعم دودی و شکلات",
    description="قهوه آنتیگوا گواتمالا با طعم دودی، شکلات تلخ و ادویه. برشته‌کاری تیره. مناسب برای اسپرسو و موکاپات.",
    origin="گواتمالا", roast="تیره",
    notes=["دودی", "شکلات تلخ", "دارچین"]
)

create_product(
    "قهوه کنیا AA", "kenya-aa", filter_coffee.name,
    price=580000, stock=80, discount=0,
    short_desc="قهوه کنیایی با اسیدیته بالا و طعم میوه‌ای",
    description="قهوه کنیا AA با اسیدیته براق، طتم کشمش سیاه، گوجه و گل. یکی از پرفروش‌ترین قهوه‌های تخصصی.",
    is_featured=True, origin="کنیا", roast="متوسط",
    notes=["کشمش سیاه", "گوجه", "گل محمدی"]
)

create_product(
    "قهوه هندونس فوری", "instant-honduras", instant.name,
    price=180000, stock=500, discount=20000,
    short_desc="قهوه فوری با طعم ملایم و آجیلی",
    description="قهوه فوری ساخته شده از دانه‌های عربیکا هندوراس. طعم ملایم، آجیلی و کمی شیرین. مناسب برای مصرف سریع.",
    origin="هندوراس", roast="متوسط",
    notes=["بادام", "کارامل"]
)

create_product(
    "قهوه پاناما گیشا", "panama-geisha", filter_coffee.name,
    price=1200000, stock=30, discount=0,
    short_desc="گیشا افسانه‌ای با طعم گل و چای",
    description="یکی از گران‌ترین و نایاب‌ترین قهوه‌های جهان. گیشا پاناما با طعم گل یاس، چای سیاه، هلو و برگاموت. برشته‌کاری بسیار سبک.",
    is_featured=True, origin="پاناما", roast="بسیار سبک",
    notes=["گل یاس", "هلو", "برگاموت", "چای سیاه"]
)

create_product(
    "قهوه اندونزی سوماترا", "indonesia-sumatra", beans.name,
    price=420000, stock=180, discount=0,
    short_desc="دانه قهوه سوماترا با طعم زمینی و ادویه",
    description="قهوه سوماترا با طعم زمینی، ادویه، چوب و کاکائو. برشتهکاری تیره. بدنه سنگین و کرم غلیظ.",
    origin="اندونزی", roast="تیره",
    notes=["زمینی", "چوب صندل", "کاکائو", "فلفل"]
)

# Accessories
create_product(
    "ماگ سرامیکی نوار", "navar-ceramic-mug", mugs.name,
    price=280000, stock=200, discount=0,
    short_desc="ماگ سرامیکی دست‌ساز با طراحی مینیمال",
    description="ماگ سرامیکی دست‌ساز با ظرفیت 350ml. طراحی مینیمال و شیک. مناسب برای اسپرسو و کاپوچینو.",
    origin="ایران", notes=["سرامیک", "دست‌ساز", "350ml"]
)

create_product(
    "آسیاب دستی هاریو", "hario-hand-grinder", grinders.name,
    price=1800000, stock=50, discount=200000,
    short_desc="آسیاب دستی هاریو اسکلتون با دنده سرامیکی",
    description="آسیاب دستی هاریو اسکلتون با دنده سرامیکی. قابلیت تنظیم درجه آسیاب. مناسب برای قهوه فیلتر و اسپرسو.",
    origin="ژاپن", notes=["دنده سرامیکی", "قابل تنظیم", "ظرفیت 24g"]
)

create_product(
    "کیف چرمی قهوه", "coffee-leather-bag", accessories.name,
    price=650000, stock=75, discount=50000,
    short_desc="کیف چرمی طبیعی برای حمل قهوه و اکسسوری",
    description="کیف چرمی طبیعی برای حمل آسیاب، فیلتر و لوازم قهوه. با جیب‌های متعدد و بند قابل تنظیم.",
    origin="ایران", notes=["چرم طبیعی", "ضد آب"]
)

print("\n🎉 All test products created!")
