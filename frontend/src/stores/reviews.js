import { defineStore } from "pinia";
import { ref, computed } from "vue";

const KEY = "navar_reviews_v1";

const defaultReviews = {
  "ethiopia-yirgacheffe": [
    { id: "r1", name: "سارا احمدی", rating: 5, text: "بهترین قهوه‌ای که تا حالا خوردم. عطر یاسمن واقعاً حس می‌شه. برای V60 عالیه.", date: "۱۴۰۳/۰۲/۱۰" },
    { id: "r2", name: "علی رضایی", rating: 4, text: "اسیدیته‌ی روشن و تازه. برشته‌ش خوبه ولی دوست دارم کمی تاریک‌تر باشه.", date: "۱۴۰۳/۰۳/۰۱" },
  ],
  "colombia-huila": [
    { id: "r3", name: "مریم محمدی", rating: 5, text: "شیرینی کارامل واقعیه. برای صبح‌ها با موکاپات خیلی خوبه. حتماً دوباره می‌خرم.", date: "۱۴۰۳/۰۱/۲۵" },
  ],
  "kenya-aa": [
    { id: "r4", name: "کیوان نجفی", rating: 5, text: "این قهوه یه تجربه‌ی کاملاً متفاوته. اسیدیته‌ی شراب‌گون داره که برای Cold Brew فوق‌العاده‌ست.", date: "۱۴۰۳/۰۳/۱۵" },
    { id: "r5", name: "نازنین حسینی", rating: 4, text: "عطر میوه‌های قرمز توش واقعیه. ولی ممکنه برای همه مناسب نباشه.", date: "۱۴۰۳/۰۳/۱۸" },
  ],
};

function load() {
  try { const r = localStorage.getItem(KEY); return r ? JSON.parse(r) : defaultReviews; } catch { return defaultReviews; }
}

export const useReviewsStore = defineStore("reviews", () => {
  const all = ref(load());

  function save() { localStorage.setItem(KEY, JSON.stringify(all.value)); }

  function getReviews(productId) { return all.value[productId] || []; }

  function averageRating(productId) {
    const list = getReviews(productId);
    if (!list.length) return 0;
    return Math.round((list.reduce((s, r) => s + r.rating, 0) / list.length) * 10) / 10;
  }

  function addReview(productId, { name, rating, text }) {
    if (!all.value[productId]) all.value[productId] = [];
    all.value[productId].unshift({
      id: Date.now().toString(),
      name,
      rating,
      text,
      date: new Date().toLocaleDateString("fa-IR"),
    });
    save();
  }

  return { getReviews, averageRating, addReview };
});
