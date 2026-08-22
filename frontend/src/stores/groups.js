import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/lib/api";
import { isDemoMode } from "@/lib/demo.js";

const STORAGE_KEY = "navar_groups_v1";

const defaultGroups = [
  {
    id: "coffee-single-origin",
    name: "قهوه تک‌خاستگاه",
    type: "coffee",
    description: "دانه‌های قهوه از یک مزرعه یا منطقه مشخص",
    attributes: [
      { id: "origin", name: "کشور خاستگاه", required: true, options: ["اتیوپی", "کلمبیا", "برزیل", "کنیا", "گواتمالا", "یمن"] },
      { id: "process", name: "روش فرآوری", required: true, options: ["شسته", "نچرال", "هانی", "شسته دوگانه"] },
      { id: "roast", name: "درجه برشته", required: true, options: ["روشن", "متوسط", "تیره"] },
      { id: "altitude", name: "ارتفاع کشت", required: false, options: ["۱۲۰۰–۱۵۰۰ متر", "۱۵۰۰–۱۸۰۰ متر", "۱۸۰۰–۲۲۰۰ متر"] },
      { id: "variety", name: "گونه", required: false, options: ["عربیکا", "روبوستا", "لیبریکا"] },
    ],
    weights: [
      { label: "۲۵۰ گرم", multiplier: 1 },
      { label: "۵۰۰ گرم", multiplier: 1.9 },
      { label: "۱ کیلوگرم", multiplier: 3.5 },
    ],
    grinds: ["دانه کامل", "اسپرسو", "موکاپات", "فرنچ پرس", "V60"],
    createdAt: "۱۴۰۳/۰۳/۰۱",
  },
  {
    id: "coffee-blend",
    name: "بلند قهوه",
    type: "coffee",
    description: "ترکیب دانه‌های قهوه از خاستگاه‌های مختلف",
    attributes: [
      { id: "strength", name: "قدرت", required: true, options: ["ملایم", "متوسط", "قوی", "خیلی قوی"] },
      { id: "roast", name: "درجه برشته", required: true, options: ["روشن", "متوسط", "تیره"] },
    ],
    weights: [
      { label: "۲۵۰ گرم", multiplier: 1 },
      { label: "۵۰۰ گرم", multiplier: 1.85 },
      { label: "۱ کیلوگرم", multiplier: 3.4 },
    ],
    grinds: ["دانه کامل", "اسپرسو", "موکاپات"],
    createdAt: "۱۴۰۳/۰۳/۰۱",
  },
  {
    id: "accessories-brewing",
    name: "وسایل دم‌آوری",
    type: "accessory",
    description: "ابزارهای دم‌آوری دستی قهوه",
    attributes: [
      { id: "capacity", name: "ظرفیت", required: true, options: ["۱–۲ فنجان", "۲–۴ فنجان", "۴–۶ فنجان", "۶+ فنجان"] },
      { id: "material", name: "جنس بدنه", required: true, options: ["شیشه بروسیلیکات", "سرامیک", "استیل ضدزنگ", "پلاستیک", "مس"] },
      { id: "brand", name: "برند", required: false, options: ["Hario", "Chemex", "Bodum", "Fellow", "Bialetti", "1Zpresso"] },
    ],
    weights: [],
    grinds: [],
    createdAt: "۱۴۰۳/۰۳/۰۱",
  },
  {
    id: "accessories-grinder",
    name: "آسیاب قهوه",
    type: "accessory",
    description: "آسیاب‌های دستی و برقی",
    attributes: [
      { id: "type", name: "نوع", required: true, options: ["دستی", "برقی"] },
      { id: "burr", name: "نوع آسیاب", required: true, options: ["برش فولادی مخروطی", "برش فولادی تخت", "پرانه‌ای"] },
      { id: "capacity", name: "ظرفیت هاپر", required: false, options: ["تا ۳۰ گرم", "۳۰–۶۰ گرم", "۶۰+ گرم"] },
    ],
    weights: [],
    grinds: [],
    createdAt: "۱۴۰۳/۰۳/۰۱",
  },
];

export const useGroupsStore = defineStore("groups", () => {
  const groups = ref([]);
  const loading = ref(false);

  async function fetchGroups() {
    loading.value = true;
    if (isDemoMode) {
      groups.value = loadGroups();
      loading.value = false;
      return;
    }
    try {
      const data = await api.admin.groups.get();
      if (Array.isArray(data) && data.length > 0) {
        groups.value = data;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      } else {
        throw new Error("empty");
      }
    } catch {
      const cached = loadGroups();
      groups.value = cached;
    }
    loading.value = false;
  }

  function loadGroups() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) return JSON.parse(raw);
    } catch {}
    return defaultGroups;
  }

  async function saveToServer() {
    if (isDemoMode) return;
    try {
      await api.admin.groups.update(groups.value);
    } catch {
      // silent
    }
  }

  function save() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(groups.value));
    saveToServer();
  }

  function create(data) {
    const g = { ...data, id: Date.now().toString(), createdAt: new Date().toLocaleDateString("fa-IR") };
    groups.value.push(g);
    save();
    return g;
  }

  function update(g) {
    const idx = groups.value.findIndex((x) => x.id === g.id);
    if (idx !== -1) groups.value[idx] = g;
    save();
  }

  function remove(id) {
    if (confirm("این گروه حذف شود؟")) {
      groups.value = groups.value.filter((g) => g.id !== id);
      save();
    }
  }

  fetchGroups();

  return { groups, loading, create, update, remove };
});
