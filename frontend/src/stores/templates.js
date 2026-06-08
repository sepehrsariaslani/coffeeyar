import { defineStore } from "pinia";
import { ref } from "vue";

const STORAGE_KEY = "navar_templates";

export const defaultTemplates = [
  {
    id: "specialty-single-origin",
    name: "تک‌خاستگاه اسپشیالتی",
    description: "قالب پایه برای قهوه‌های تک‌خاستگاه با گزینه‌های دم‌آوری دستی",
    weights: [
      { label: "۲۵۰ گرم", multiplier: 1 },
      { label: "۵۰۰ گرم", multiplier: 1.9 },
      { label: "۱ کیلوگرم", multiplier: 3.5 },
    ],
    grinds: ["دانه کامل", "V60", "فرنچ پرس", "کمکس", "ایروپرس"],
    attributes: [
      {
        id: "altitude",
        name: "ارتفاع کشت",
        options: [
          { value: "۱۲۰۰–۱۵۰۰ متر" },
          { value: "۱۵۰۰–۱۸۰۰ متر" },
          { value: "۱۸۰۰–۲۲۰۰ متر" },
        ],
      },
      {
        id: "variety",
        name: "گونه",
        options: [{ value: "عربیکا" }, { value: "روبوستا" }, { value: "لیبریکا" }],
      },
      {
        id: "certification",
        name: "گواهینامه",
        options: [
          { value: "ندارد" },
          { value: "ارگانیک" },
          { value: "Rainforest Alliance" },
          { value: "Fair Trade" },
        ],
      },
    ],
    defaultRoast: "روشن",
    defaultProcess: "شسته",
    createdAt: "۱۴۰۳/۰۳/۰۱",
  },
  {
    id: "espresso-blend",
    name: "بلند اسپرسو",
    description: "قالب برای قهوه‌های مناسب اسپرسو و دستگاه‌های برقی",
    weights: [
      { label: "۲۵۰ گرم", multiplier: 1 },
      { label: "۵۰۰ گرم", multiplier: 1.85 },
      { label: "۱ کیلوگرم", multiplier: 3.4 },
      { label: "۲ کیلوگرم", multiplier: 6.5 },
    ],
    grinds: ["دانه کامل", "اسپرسو", "موکاپات"],
    attributes: [
      {
        id: "strength",
        name: "قدرت",
        options: [
          { value: "ملایم" },
          { value: "متوسط" },
          { value: "قوی" },
          { value: "خیلی قوی" },
        ],
      },
      {
        id: "variety",
        name: "گونه",
        options: [
          { value: "عربیکا" },
          { value: "روبوستا" },
          { value: "ترکیب عربیکا/روبوستا" },
        ],
      },
    ],
    defaultRoast: "تیره",
    defaultProcess: "نچرال",
    createdAt: "۱۴۰۳/۰۳/۰۱",
  },
];

function loadTemplates() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {}
  return defaultTemplates;
}

export const useTemplatesStore = defineStore("templates", () => {
  const templates = ref(loadTemplates());

  function save() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(templates.value));
  }

  function add(tpl) {
    const newTpl = {
      ...tpl,
      id: Date.now().toString(),
      createdAt: new Date().toLocaleDateString("fa-IR"),
    };
    templates.value.push(newTpl);
    save();
    return newTpl;
  }

  function update(tpl) {
    const idx = templates.value.findIndex((t) => t.id === tpl.id);
    if (idx !== -1) templates.value[idx] = tpl;
    save();
  }

  function remove(id) {
    templates.value = templates.value.filter((t) => t.id !== id);
    save();
  }

  return { templates, add, update, remove };
});
