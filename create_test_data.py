import frappe

def create_test_data():
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

    frappe.db.commit()
    print("✅ Categories created!")

    def create_product(name, slug, category, price, stock=100, discount=0, short_desc="", description="", image="", has_variants=False, is_featured=False, origin="", roast="", notes=None):
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
            "image": image,
            "has_variants": has_variants,
            "is_featured": is_featured,
            "is_published": 1,
            "display_order": 0,
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"  ✅ {name}")

    # Coffee products
    create_product("قهوه اسپرسو برزیلی", "brazilian-espresso", espresso.name, 450000, 200, 50000, "اسپرسو غنی با طعم شکلات و گردو", "قهوه اسپرسو برزیلی با برشته‌کاری متوسط، طعم شکلات تلخ و گردو. مناسب برای اسپرسوسازهای خانگی و حرفه‌ای.", is_featured=True, origin="برزیل", roast="متوسط")
    create_product("قهوه اتیوپی یيرگاچف", "ethiopia-yirgacheffe", filter_coffee.name, 520000, 150, 0, "قهوه فیلتر با طعم میوه‌ای و گلی", "یکی از بهترین قهوه‌های جهان از منطقه یيرگاچف اتیوپی. با نت‌های میوه‌ای، گل یاس و چای سیاه. برشته‌کاری سبک.", is_featured=True, origin="اتیوپی", roast="سبک")
    create_product("قهوه کلمبیا سوپریمو", "colombia-supremo", beans.name, 380000, 300, 30000, "دانه قهوه کلمبیایی با طعم آجیل و کارامل", "دانه قهوه سوپریمو کلمبیا با کیفیت عالی. طعم آجیل، کارامل و کاکائو. مناسب برای تمام روش‌های دم‌آوری.", origin="کلمبیا", roast="متوسط-تیره")
    create_product("قهوه گواتمالا آنتیگوا", "guatemala-antigua", espresso.name, 490000, 120, 0, "اسپرسو با طعم دودی و شکلات", "قهوه آنتیگوا گواتمالا با طعم دودی، شکلات تلخ و ادویه. برشته‌کاری تیره. مناسب برای اسپرسو و موکاپات.", origin="گواتمالا", roast="تیره")
    create_product("قهوه کنیا AA", "kenya-aa", filter_coffee.name, 580000, 80, 0, "قهوه کنیایی با اسیدیته بالا و طعم میوه‌ای", "قهوه کنیا AA با اسیدیته براق، طتم کشمش سیاه، گوجه و گل. یکی از پرفروش‌ترین قهوه‌های تخصصی.", is_featured=True, origin="کنیا", roast="متوسط")
    create_product("قهوه هندونس فوری", "instant-honduras", instant.name, 180000, 500, 20000, "قهوه فوری با طعم ملایم و آجیلی", "قهوه فوری ساخته شده از دانه‌های عربیکا هندوراس. طعم ملایم، آجیلی و کمی شیرین. مناسب برای مصرف سریع.", origin="هندوراس", roast="متوسط")
    create_product("قهوه پاناما گیشا", "panama-geisha", filter_coffee.name, 1200000, 30, 0, "گیشا افسانه‌ای با طعم گل و چای", "یکی از گران‌ترین و نایاب‌ترین قهوه‌های جهان. گیشا پاناما با طعم گل یاس، چای سیاه، هلو و برگاموت. برشته‌کاری بسیار سبک.", is_featured=True, origin="پاناما", roast="بسیار سبک")
    create_product("قهوه اندونزی سوماترا", "indonesia-sumatra", beans.name, 420000, 180, 0, "دانه قهوه سوماترا با طعم زمینی و ادویه", "قهوه سوماترا با طعم زمینی، ادویه، چوب و کاکائو. برشتهکاری تیره. بدنه سنگین و کرم غلیظ.", origin="اندونزی", roast="تیره")

    # Accessories
    create_product("ماگ سرامیکی نوار", "navar-ceramic-mug", mugs.name, 280000, 200, 0, "ماگ سرامیکی دست‌ساز با طراحی مینیمال", "ماگ سرامیکی دست‌ساز با ظرفیت 350ml. طراحی مینیمال و شیک. مناسب برای اسپرسو و کاپوچینو.", origin="ایران")
    create_product("آسیاب دستی هاریو", "hario-hand-grinder", grinders.name, 1800000, 50, 200000, "آسیاب دستی هاریو اسکلتون با دنده سرامیکی", "آسیاب دستی هاریو اسکلتون با دنده سرامیکی. قابلیت تنظیم درجه آسیاب. مناسب برای قهوه فیلتر و اسپرسو.", origin="ژاپن")
    create_product("کیف چرمی قهوه", "coffee-leather-bag", accessories.name, 650000, 75, 50000, "کیف چرمی طبیعی برای حمل قهوه و اکسسوری", "کیف چرمی طبیعی برای حمل آسیاب، فیلتر و لوازم قهوه. با جیب‌های متعدد و بند قابل تنظیم.", origin="ایران")

    print("\n🎉 All test products created!")

create_test_data()
