import product1 from "@/assets/product-1.jpg";
import product2 from "@/assets/product-2.jpg";
import product3 from "@/assets/product-3.jpg";
import product4 from "@/assets/product-4.jpg";

const defaultWeights = [
  { label: "۲۵۰ گرم", multiplier: 1 },
  { label: "۵۰۰ گرم", multiplier: 1.9 },
  { label: "۱ کیلوگرم", multiplier: 3.5 },
];

const defaultGrinds = ["دانه کامل", "اسپرسو", "موکاپات", "فرنچ پرس", "V60"];

export const products = [
  {
    id: "ethiopia-yirgacheffe",
    categoryId: "cat-coffee", subCategoryId: "sub-coffee-single",
    attrs: { origin: "اتیوپی", roast: "روشن", process: "شسته" },
    type: "coffee",
    name: "اتیوپی یرگاچف",
    origin: "اتیوپی",
    process: "شسته",
    roast: "روشن",
    price: 480000,
    stock: "in_stock",
    stockCount: 24,
    image: product1,
    gallery: [product1, product2, product3, product4],
    weights: defaultWeights,
    grinds: defaultGrinds,
    flavor: { bitterness: 3, acidity: 8, aroma: 9 },
    notes: ["یاسمن", "لیمو", "عسل"],
    description:
      "یک قهوه‌ی روشن و معطر از منطقه‌ی یرگاچف اتیوپی با اسیدیته‌ی روشن و عطر گل‌های سفید. مناسب برای دم‌آوری دستی.",
    specs: [
      { label: "خاستگاه", value: "اتیوپی — یرگاچف" },
      { label: "فرآوری", value: "شسته (Washed)" },
      { label: "رست", value: "روشن (Light)" },
      { label: "اسیدیته", value: "۸ / ۱۰" },
      { label: "تلخی", value: "۳ / ۱۰" },
      { label: "عطر", value: "۹ / ۱۰" },
      { label: "ارتفاع کشت", value: "۱۷۰۰ تا ۲۲۰۰ متر" },
      { label: "برداشت", value: "اکتبر تا ژانویه" },
      { label: "روش دم‌آوری", value: "V60، کمکس، ایروپرس" },
    ],
  },
  {
    id: "colombia-huila",
    categoryId: "cat-coffee", subCategoryId: "sub-coffee-single",
    attrs: { origin: "کلمبیا", roast: "متوسط", process: "شسته" },
    type: "coffee",
    name: "کلمبیا هویلا",
    origin: "کلمبیا",
    process: "شسته",
    roast: "متوسط",
    price: 420000,
    stock: "low_stock",
    stockCount: 5,
    image: product2,
    gallery: [product2, product1, product3, product4],
    weights: defaultWeights,
    grinds: defaultGrinds,
    flavor: { bitterness: 5, acidity: 6, aroma: 7 },
    notes: ["شکلات شیری", "کاراملی", "بادام"],
    description:
      "بدنه‌ی متعادل، شیرینی کارامل و پایان نرم شکلاتی. انتخابی بی‌نقص برای اسپرسوی روزانه.",
    specs: [
      { label: "خاستگاه", value: "کلمبیا — هویلا" },
      { label: "فرآوری", value: "شسته (Washed)" },
      { label: "رست", value: "متوسط (Medium)" },
      { label: "اسیدیته", value: "۶ / ۱۰" },
      { label: "تلخی", value: "۵ / ۱۰" },
      { label: "عطر", value: "۷ / ۱۰" },
      { label: "ارتفاع کشت", value: "۱۵۰۰ تا ۱۹۰۰ متر" },
      { label: "برداشت", value: "اکتبر تا فوریه" },
      { label: "روش دم‌آوری", value: "اسپرسو، موکاپات، فرنچ پرس" },
    ],
  },
  {
    id: "brazil-cerrado",
    categoryId: "cat-coffee", subCategoryId: "sub-coffee-single",
    attrs: { origin: "برزیل", roast: "تیره", process: "نچرال" },
    type: "coffee",
    name: "برزیل سرادو",
    origin: "برزیل",
    process: "نچرال",
    roast: "تیره",
    price: 380000,
    stock: "out_of_stock",
    stockCount: 0,
    image: product3,
    gallery: [product3, product2, product1, product4],
    weights: defaultWeights,
    grinds: defaultGrinds,
    flavor: { bitterness: 8, acidity: 3, aroma: 6 },
    notes: ["کاکائو", "فندق", "تنباکوی شیرین"],
    description:
      "بدنه‌ی سنگین و شکلاتی با اسیدیته‌ی پایین. ستون فقرات بلندهای کلاسیک اسپرسو.",
    specs: [
      { label: "خاستگاه", value: "برزیل — سرادو" },
      { label: "فرآوری", value: "نچرال (Natural)" },
      { label: "رست", value: "تیره (Dark)" },
      { label: "اسیدیته", value: "۳ / ۱۰" },
      { label: "تلخی", value: "۸ / ۱۰" },
      { label: "عطر", value: "۶ / ۱۰" },
      { label: "ارتفاع کشت", value: "۸۵۰ تا ۱۲۵۰ متر" },
      { label: "برداشت", value: "می تا سپتامبر" },
      { label: "روش دم‌آوری", value: "اسپرسو، موکاپات" },
    ],
  },
  {
    id: "kenya-aa",
    categoryId: "cat-coffee", subCategoryId: "sub-coffee-single",
    attrs: { origin: "کنیا", roast: "متوسط", process: "شسته دوگانه" },
    type: "coffee",
    name: "کنیا AA",
    origin: "کنیا",
    process: "شسته دوگانه",
    roast: "متوسط",
    price: 540000,
    stock: "in_stock",
    stockCount: 18,
    image: product4,
    gallery: [product4, product1, product2, product3],
    weights: defaultWeights,
    grinds: defaultGrinds,
    flavor: { bitterness: 4, acidity: 9, aroma: 8 },
    notes: ["انگور سیاه", "گریپ‌فروت", "شکر قهوه‌ای"],
    description:
      "اسیدیته‌ی شراب‌گونه، عطر میوه‌های قرمز و شیرینی عمیق. تجربه‌ای فراموش‌نشدنی برای دم‌آوری V60.",
    specs: [
      { label: "خاستگاه", value: "کنیا — نیری" },
      { label: "فرآوری", value: "شسته دوگانه (Double Washed)" },
      { label: "رست", value: "متوسط (Medium)" },
      { label: "اسیدیته", value: "۹ / ۱۰" },
      { label: "تلخی", value: "۴ / ۱۰" },
      { label: "عطر", value: "۸ / ۱۰" },
      { label: "ارتفاع کشت", value: "۱۸۰۰ تا ۲۱۰۰ متر" },
      { label: "برداشت", value: "اکتبر تا دسامبر" },
      { label: "روش دم‌آوری", value: "V60، کمکس، کلد برو" },
    ],
  },
  {
    id: "french-press-classic",
    categoryId: "cat-accessories", subCategoryId: "sub-acc-brewing",
    attrs: { brand: "Bodum", material: "شیشه بروسیلیکات" },
    type: "accessory",
    name: "فرنچ پرس کلاسیک",
    category: "فرنچ پرس",
    brand: "Bodum",
    price: 850000,
    stock: "in_stock",
    stockCount: 12,
    image: product1,
    gallery: [product1, product2],
    description:
      "فرنچ پرس کلاسیک با بدنه‌ی شیشه‌ی بروسیلیکات مقاوم در برابر حرارت و قاب استیل ضدزنگ. ظرفیت ۳۵۰ میلی‌لیتر، ایده‌آل برای ۱ تا ۲ فنجان قهوه‌ی پُربدنه.",
    specs: [
      { label: "ظرفیت", value: "۳۵۰ میلی‌لیتر" },
      { label: "جنس بدنه", value: "شیشه بروسیلیکات" },
      { label: "قاب", value: "استیل ضدزنگ" },
      { label: "فیلتر", value: "مش استیل دوجداره" },
      { label: "مناسب برای", value: "۱ تا ۲ فنجان" },
    ],
  },
  {
    id: "french-press-large",
    categoryId: "cat-accessories", subCategoryId: "sub-acc-brewing",
    attrs: { brand: "Bodum", material: "شیشه بروسیلیکات" },
    type: "accessory",
    name: "فرنچ پرس بزرگ",
    category: "فرنچ پرس",
    brand: "Bodum",
    price: 1100000,
    stock: "low_stock",
    stockCount: 3,
    image: product2,
    gallery: [product2, product1],
    description:
      "نسخه‌ی بزرگ فرنچ پرس کلاسیک با ظرفیت ۱ لیتر. عالی برای جمع‌های دوستانه یا دم‌آوری کلد برو.",
    specs: [
      { label: "ظرفیت", value: "۱ لیتر" },
      { label: "جنس بدنه", value: "شیشه بروسیلیکات" },
      { label: "قاب", value: "استیل ضدزنگ" },
      { label: "فیلتر", value: "مش استیل دوجداره" },
      { label: "مناسب برای", value: "۴ تا ۶ فنجان" },
    ],
  },
  {
    id: "moka-pot-3cup",
    categoryId: "cat-accessories", subCategoryId: "sub-acc-brewing",
    attrs: { brand: "Bialetti", material: "آلومینیوم" },
    type: "accessory",
    name: "موکاپات ۳ کاپ",
    category: "موکاپات",
    brand: "Bialetti",
    price: 950000,
    stock: "in_stock",
    stockCount: 9,
    image: product3,
    gallery: [product3, product4],
    description:
      "موکاپات اصلی بیالتی ساخت ایتالیا. قهوه‌ای قوی و پُربدنه شبیه به اسپرسو با فشار بخار آب. دسته‌ی ارگونومیک مقاوم در برابر حرارت.",
    specs: [
      { label: "ظرفیت", value: "۳ فنجان اسپرسو" },
      { label: "جنس", value: "آلومینیوم آنودایز‌شده" },
      { label: "دسته", value: "پلاستیک مقاوم حرارت" },
      { label: "مناسب برای", value: "گاز و سرامیک" },
      { label: "کشور سازنده", value: "ایتالیا" },
    ],
  },
  {
    id: "v60-ceramic",
    categoryId: "cat-accessories", subCategoryId: "sub-acc-brewing",
    attrs: { brand: "Hario", material: "سرامیک" },
    type: "accessory",
    name: "درپر V60 سرامیکی",
    category: "V60",
    brand: "Hario",
    price: 720000,
    stock: "in_stock",
    stockCount: 15,
    image: product4,
    gallery: [product4, product1],
    description:
      "درپر V60 مدل ۰۲ هاریو ساخت ژاپن از سرامیک با کیفیت. حفظ دمای بهتر نسبت به مدل پلاستیکی. شیارهای مارپیچ منحصربه‌فرد برای جریان ایده‌آل قهوه.",
    specs: [
      { label: "سایز", value: "۰۲ (۱ تا ۴ فنجان)" },
      { label: "جنس", value: "سرامیک ژاپنی" },
      { label: "زاویه‌ی شیار", value: "۶۰ درجه" },
      { label: "فیلتر", value: "فیلتر کاغذی V60-02" },
      { label: "کشور سازنده", value: "ژاپن" },
    ],
  },
  {
    id: "chemex-6cup",
    categoryId: "cat-accessories", subCategoryId: "sub-acc-brewing",
    attrs: { brand: "Chemex", material: "شیشه بروسیلیکات" },
    type: "accessory",
    name: "کمکس ۶ کاپ",
    category: "کمکس",
    brand: "Chemex",
    price: 1350000,
    stock: "in_stock",
    stockCount: 7,
    image: product1,
    gallery: [product1, product3],
    description:
      "کمکس اصلی آمریکایی با طراحی کلاسیک دهه ۱۹۴۰. فیلتر ضخیم کمکس چربی قهوه را می‌گیرد و قهوه‌ای شفاف و ظریف تولید می‌کند. اثر هنری که روی میزتان می‌درخشد.",
    specs: [
      { label: "ظرفیت", value: "۶ فنجان" },
      { label: "جنس", value: "شیشه بروسیلیکات" },
      { label: "دسته", value: "چوب و چرم" },
      { label: "فیلتر", value: "کاغذ ضخیم کمکس" },
      { label: "کشور سازنده", value: "آمریکا" },
    ],
  },
  {
    id: "gooseneck-kettle",
    categoryId: "cat-accessories", subCategoryId: "sub-acc-brewing",
    attrs: { brand: "Fellow", material: "استیل" },
    type: "accessory",
    name: "کتری ماهیچه‌ای برقی",
    category: "کتری",
    brand: "Fellow",
    price: 2800000,
    stock: "low_stock",
    stockCount: 2,
    image: product2,
    gallery: [product2, product4],
    description:
      "کتری برقی Fellow Stagg EKG با کنترل دقیق دما (±۱ درجه) و نازل ماهیچه‌ای برای ریختن کنترل‌شده‌ی آب. ضروری برای دم‌آوری دستی با V60 یا کمکس.",
    specs: [
      { label: "ظرفیت", value: "۰.۹ لیتر" },
      { label: "کنترل دما", value: "۴۰ تا ۱۰۰ درجه (±۱ درجه)" },
      { label: "توان", value: "۱۲۰۰ وات" },
      { label: "نگه‌داری دما", value: "۶۰ دقیقه" },
      { label: "کشور سازنده", value: "آمریکا" },
    ],
  },
  {
    id: "hand-grinder-1zpresso",
    categoryId: "cat-accessories", subCategoryId: "sub-acc-grinder",
    attrs: { brand: "1Zpresso", material: "آلومینیوم" },
    type: "accessory",
    name: "آسیاب دستی 1Zpresso",
    category: "آسیاب",
    brand: "1Zpresso",
    price: 3200000,
    stock: "in_stock",
    stockCount: 6,
    image: product3,
    gallery: [product3, product2],
    description:
      "آسیاب دستی حرفه‌ای 1Zpresso JX با ۴۸ برش فولادی. تنظیم دقیق درجه آسیاب با ۹۰ کلیک در هر چرخش. مناسب برای تمام روش‌های دم‌آوری از اسپرسو تا فرنچ پرس.",
    specs: [
      { label: "برش‌ها", value: "۴۸ برش فولادی" },
      { label: "تنظیم", value: "۹۰ کلیک/چرخش" },
      { label: "ظرفیت هاپر", value: "۳۵ گرم" },
      { label: "جنس بدنه", value: "آلومینیوم CNC" },
      { label: "وزن", value: "۴۰۰ گرم" },
    ],
  },
];

export const posts = [
  {
    slug: "art-of-pour-over",
    title: "هنر دم‌آوری دستی",
    excerpt: "چگونه یک فنجان قهوه‌ی بی‌نقص دم کنیم؟ از انتخاب دانه تا کنترل دما.",
    date: "۱۴۰۳/۰۲/۱۵",
    readTime: "۶ دقیقه",
    category: "عمومی",
    body: "دم‌آوری دستی هنری است که نیازمند صبر و دقت است. در این مقاله از انتخاب دانه‌ی مناسب تا کنترل دمای آب و زمان عصاره‌گیری را با هم مرور می‌کنیم...",
  },
  {
    slug: "single-origin-vs-blend",
    title: "تک‌خاستگاه یا بلند؟",
    excerpt: "تفاوت میان قهوه‌های تک‌خاستگاه و بلندها و این که کدام برای شما مناسب است.",
    date: "۱۴۰۳/۰۱/۲۸",
    readTime: "۴ دقیقه",
    category: "عمومی",
    body: "قهوه‌های تک‌خاستگاه شخصیت منحصربه‌فرد یک منطقه را به فنجان شما می‌آورند، در حالی که بلندها تعادلی هوشمندانه هستند...",
  },
  {
    slug: "espresso-at-home",
    title: "اسپرسو در خانه",
    excerpt: "راهنمای کامل ساخت اسپرسوی کافه‌ای در آشپزخانه‌ی شما.",
    date: "۱۴۰۳/۰۱/۱۰",
    readTime: "۸ دقیقه",
    category: "عمومی",
    body: "ساخت اسپرسوی خوب در خانه ممکن است. آسیاب درست، فشار مناسب و دانه‌ی تازه سه ضلع این مثلث هستند...",
  },
  {
    slug: "brew-french-press",
    title: "راهنمای دم‌آوری با فرنچ پرس",
    excerpt: "فرنچ پرس ساده‌ترین راه برای رسیدن به یک فنجان غنی و پُربدنه است. همه چیز را اینجا یاد بگیرید.",
    date: "۱۴۰۳/۰۳/۰۵",
    readTime: "۵ دقیقه",
    category: "روش دم‌آوری",
    body: `فرنچ پرس یکی از محبوب‌ترین روش‌های دم‌آوری قهوه است که بدون نیاز به تجهیزات پیچیده، فنجانی پُربدنه و معطر تحویل می‌دهد.

**مواد لازم:**
- ۳۰ گرم قهوه با آسیاب درشت
- ۵۰۰ میلی‌لیتر آب در دمای ۹۳ درجه
- فرنچ پرس ۵۰۰ میلی‌لیتری

**مراحل:**
۱. فرنچ پرس را با آب گرم پیش‌گرم کنید.
۲. قهوه‌ی آسیاب‌شده را داخل ظرف بریزید.
۳. آب را به آرامی روی قهوه بریزید و ۳۰ ثانیه صبر کنید (مرحله‌ی بلوم).
۴. بقیه‌ی آب را اضافه کنید و هم بزنید.
۵. درب فرنچ پرس را بگذارید و ۴ دقیقه صبر کنید.
۶. پیستون را به آرامی فشار دهید و بلافاصله قهوه را بریزید.

**نکته:** آسیاب درشت مانع تلخی بیش از حد می‌شود. از دانه‌های با رست متوسط تا تیره بهترین نتیجه را می‌گیرید.`,
  },
  {
    slug: "brew-v60",
    title: "دم‌آوری با V60 — گام به گام",
    excerpt: "V60 قهوه‌ای شفاف و ظریف با اسیدیته‌ی روشن تولید می‌کند. اگر طرفدار قهوه‌های تک‌خاستگاه هستید، این روش برای شماست.",
    date: "۱۴۰۳/۰۳/۱۲",
    readTime: "۷ دقیقه",
    category: "روش دم‌آوری",
    body: `V60 یکی از دقیق‌ترین روش‌های دم‌آوری است که کنترل کامل روی طعم نهایی را به شما می‌دهد.

**مواد لازم:**
- ۱۵ گرم قهوه با آسیاب متوسط
- ۲۵۰ میلی‌لیتر آب در دمای ۹۲–۹۴ درجه
- فیلتر کاغذی V60 شماره ۰۲

**مراحل:**
۱. فیلتر را آب بکشید تا طعم کاغذ از بین برود.
۲. قهوه را داخل فیلتر بریزید و سطح آن را صاف کنید.
۳. با ۳۰ گرم آب شروع کنید و ۴۵ ثانیه صبر کنید.
۴. به آرامی آب را در حرکت دورانی اضافه کنید.
۵. کل فرآیند باید بین ۲:۳۰ تا ۳:۰۰ دقیقه طول بکشد.

**نکته:** قهوه‌های روشن مثل اتیوپی یرگاچف در V60 می‌درخشند.`,
  },
  {
    slug: "brew-moka-pot",
    title: "موکاپات — اسپرسوی ایتالیایی در خانه",
    excerpt: "موکاپات با فشار بخار قهوه‌ای قوی و پُربدنه درست می‌کند. روشی کلاسیک که هیچ‌وقت از مد نمی‌افتد.",
    date: "۱۴۰۳/۰۳/۲۰",
    readTime: "۴ دقیقه",
    category: "روش دم‌آوری",
    body: `موکاپات یا کافه‌تیره ایتالیایی یکی از نمادین‌ترین وسایل دم‌آوری قهوه است.

**مواد لازم:**
- قهوه با آسیاب ریز تا متوسط
- آب گرم (نه جوش) در مخزن پایینی
- منبع حرارت ملایم

**مراحل:**
۱. آب را تا زیر سوپاپ ایمنی مخزن پایین پر کنید.
۲. قهوه را داخل سبد فیلتر بریزید و فشار ندهید.
۳. قسمت‌ها را محکم ببندید و روی حرارت ملایم بگذارید.
۴. وقتی صدای خرخر شنیدید، شعله را خاموش کنید.
۵. موکاپات را زیر آب سرد بگیرید تا استخراج متوقف شود.

**نکته:** از رست تیره برای بدنه‌ی بیشتر و از رست متوسط برای طعم متعادل‌تر استفاده کنید.`,
  },
  {
    slug: "brew-cold-brew",
    title: "کلد برو — قهوه‌ی سرد بدون تلخی",
    excerpt: "کلد برو با خیساندن طولانی‌مدت قهوه در آب سرد، نوشیدنی‌ای ملایم و طبیعتاً شیرین می‌سازد.",
    date: "۱۴۰۳/۰۴/۰۱",
    readTime: "۶ دقیقه",
    category: "روش دم‌آوری",
    body: `کلد برو با وجود سادگی، یکی از خوش‌طعم‌ترین روش‌های آماده‌سازی قهوه‌ی سرد است.

**مواد لازم:**
- ۱۰۰ گرم قهوه با آسیاب خیلی درشت
- ۱ لیتر آب سرد
- یک جار شیشه‌ای یا پارچ بزرگ
- فیلتر قهوه یا پارچه‌ی نازک

**مراحل:**
۱. قهوه و آب سرد را در ظرف مخلوط کنید.
۲. بهم بزنید تا همه‌ی قهوه خیس شود.
۳. درب ظرف را ببندید و ۱۲ تا ۲۴ ساعت در یخچال بگذارید.
۴. از فیلتر دو بار رد کنید تا کاملاً صاف شود.
۵. تا ۲ هفته در یخچال نگه‌داری کنید.

**سرو:** با یخ سرو کنید یا برای قهوه‌ی قوی‌تر، مستقیم بنوشید.`,
  },
];

export const customers = [
  {
    id: "C001",
    name: "علی محمدی",
    email: "ali.mohammadi@email.com",
    phone: "۰۹۱۲۱۲۳۴۵۶۷",
    city: "تهران",
    address: "خیابان ولیعصر، کوچه بهار، پلاک ۱۲",
    postalCode: "۱۴۳۵۸۷۶۵۴۳",
    totalOrders: 5,
    totalSpent: 3840000,
    joinDate: "۱۴۰۲/۱۰/۰۵",
    lastOrder: "۱۴۰۳/۰۳/۰۴",
  },
  {
    id: "C002",
    name: "سارا رضایی",
    email: "sara.rezaei@email.com",
    phone: "۰۹۳۵۹۸۷۶۵۴۳",
    city: "اصفهان",
    address: "خیابان چهارباغ، بلوار آزادی، پلاک ۴۵",
    postalCode: "۸۱۵۴۳۲۱۰۹۸",
    totalOrders: 3,
    totalSpent: 1560000,
    joinDate: "۱۴۰۲/۱۱/۱۸",
    lastOrder: "۱۴۰۳/۰۳/۰۳",
  },
  {
    id: "C003",
    name: "محمد کریمی",
    email: "m.karimi@email.com",
    phone: "۰۹۱۸۴۵۶۷۸۹۰",
    city: "مشهد",
    address: "بلوار وکیل‌آباد، خیابان گلشن، پلاک ۷",
    postalCode: "۹۱۸۷۶۵۴۳۲۱",
    totalOrders: 7,
    totalSpent: 5460000,
    joinDate: "۱۴۰۲/۰۸/۲۲",
    lastOrder: "۱۴۰۳/۰۳/۰۲",
  },
  {
    id: "C004",
    name: "نگار حسینی",
    email: "negar.hosseini@email.com",
    phone: "۰۹۳۳۱۲۳۴۵۶۷",
    city: "شیراز",
    address: "خیابان زند، کوچه ارم، پلاک ۳",
    postalCode: "۷۱۳۴۵۶۷۸۹۰",
    totalOrders: 2,
    totalSpent: 900000,
    joinDate: "۱۴۰۳/۰۱/۰۸",
    lastOrder: "۱۴۰۳/۰۳/۰۱",
  },
  {
    id: "C005",
    name: "رضا احمدی",
    email: "reza.ahmadi@email.com",
    phone: "۰۹۱۵۶۷۸۹۰۱۲",
    city: "تبریز",
    address: "خیابان راستا، بلوار ملت، پلاک ۱۸",
    postalCode: "۵۱۵۴۸۷۶۵۴۳",
    totalOrders: 4,
    totalSpent: 2280000,
    joinDate: "۱۴۰۲/۰۹/۱۵",
    lastOrder: "۱۴۰۳/۰۲/۲۵",
  },
  {
    id: "C006",
    name: "مریم صادقی",
    email: "maryam.sadeghi@email.com",
    phone: "۰۹۱۰۹۸۷۶۵۴۳",
    city: "تهران",
    address: "خیابان شریعتی، کوچه نیلوفر، پلاک ۹",
    postalCode: "۱۵۴۸۷۶۵۴۳۲",
    totalOrders: 6,
    totalSpent: 4020000,
    joinDate: "۱۴۰۲/۰۷/۰۳",
    lastOrder: "۱۴۰۳/۰۲/۱۸",
  },
];

export const formatPrice = (n) =>
  new Intl.NumberFormat("fa-IR").format(n) + " تومان";
