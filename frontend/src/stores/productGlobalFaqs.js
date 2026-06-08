import { defineStore } from "pinia";
import { ref } from "vue";

const DEFAULT_FAQS = [
  {
    id: "shipping",
    title: "ارسال و بازگشت",
    content: "ارسال به سراسر ایران در ۲۴ تا ۴۸ ساعت کاری.\nبرای سفارش‌های بالای ۵۰۰ هزار تومان ارسال رایگان است.\nبازگشت کالا تا ۷ روز پس از تحویل با حفظ بسته‌بندی ممکن است.",
    applyTo: "all",
    enabled: true,
    order: 0,
  },
  {
    id: "warranty",
    title: "گارانتی و خدمات",
    content: "تمام اکسسوری‌های نوار با ۶ ماه گارانتی اصالت کالا ارائه می‌شوند.\nدر صورت بروز هر گونه اشکال، با تیم پشتیبانی ما تماس بگیرید.",
    applyTo: "accessory",
    enabled: true,
    order: 1,
  },
  {
    id: "brew",
    title: "راهنمای دم‌آوری",
    content: "برای بهترین تجربه، نسبت ۱:۱۶ (یک گرم قهوه به ۱۶ گرم آب) را پیشنهاد می‌کنیم.\n· دمای آب: ۹۲ تا ۹۴ درجه\n· زمان عصاره‌گیری: ۲ دقیقه و ۳۰ ثانیه\n· نوع آسیاب: متوسط برای V60، درشت برای فرنچ پرس",
    applyTo: "coffee",
    enabled: true,
    order: 2,
  },
  {
    id: "freshness",
    title: "تازگی و نگهداری",
    content: "قهوه‌های نوار بعد از دریافت سفارش برشته می‌شوند.\nبرای حفظ تازگی، در ظرف دربسته و دور از نور و رطوبت نگه‌داری کنید.\nبهترین زمان مصرف: ۷ تا ۳۰ روز پس از تاریخ برشته شدن.",
    applyTo: "coffee",
    enabled: true,
    order: 3,
  },
  {
    id: "farm",
    title: "داستان مزرعه",
    content: "این دانه‌ها از مزارع کوچک کشاورزان خانواده‌محور تهیه شده‌اند.\nنوار با کشاورزان مستقیماً همکاری می‌کند تا قیمت منصفانه و کیفیت یکنواخت تضمین شود.",
    applyTo: "coffee",
    enabled: true,
    order: 4,
  },
];

export const useProductGlobalFaqsStore = defineStore("productGlobalFaqs", () => {
  const faqs = ref([]);

  function load() {
    try {
      const saved = localStorage.getItem("productGlobalFaqs");
      if (saved) faqs.value = JSON.parse(saved);
      else faqs.value = DEFAULT_FAQS.map((f) => ({ ...f }));
    } catch {
      faqs.value = DEFAULT_FAQS.map((f) => ({ ...f }));
    }
  }

  function save() {
    localStorage.setItem("productGlobalFaqs", JSON.stringify(faqs.value));
  }

  function add() {
    faqs.value.push({
      id: "faq-" + Date.now(),
      title: "",
      content: "",
      applyTo: "all",
      enabled: true,
      order: faqs.value.length,
    });
    save();
  }

  function remove(id) {
    faqs.value = faqs.value.filter((f) => f.id !== id);
    save();
  }

  function moveUp(idx) {
    if (idx === 0) return;
    [faqs.value[idx - 1], faqs.value[idx]] = [faqs.value[idx], faqs.value[idx - 1]];
    save();
  }

  function moveDown(idx) {
    if (idx >= faqs.value.length - 1) return;
    [faqs.value[idx], faqs.value[idx + 1]] = [faqs.value[idx + 1], faqs.value[idx]];
    save();
  }

  function getFaqsForType(type) {
    return [...faqs.value]
      .filter((f) => f.enabled && (f.applyTo === "all" || f.applyTo === type))
      .sort((a, b) => a.order - b.order);
  }

  load();

  return { faqs, save, add, remove, moveUp, moveDown, getFaqsForType };
});
