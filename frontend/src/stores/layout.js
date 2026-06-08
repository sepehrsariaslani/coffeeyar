import { defineStore } from "pinia";
import { ref, watch } from "vue";

export const DESIGN_THEMES = {
  minimal: {
    label: "مینیمال",
    desc: "فضای سفید، تیز، کلاسیک",
    class: "",
    preview: { bg: "#F9F6F1", text: "#111111", accent: "#111111", border: "#E5E5E5" },
  },
  bento: {
    label: "بنتو",
    desc: "گرید نامتقارن، باکس‌های متمایز",
    class: "theme-bento",
    preview: { bg: "#F0EFEC", text: "#111111", accent: "#333333", border: "#DEDEDE" },
  },
  modern: {
    label: "مدرن",
    desc: "گوشه‌دار، سایه، پویا",
    class: "theme-modern",
    preview: { bg: "#FFFFFF", text: "#0A0F1E", accent: "#3B5BDB", border: "#E2E8F0" },
  },
  dark: {
    label: "تاریک",
    desc: "شب‌گرد، نرم‌چشم",
    class: "theme-dark",
    preview: { bg: "#161412", text: "#F5F0EA", accent: "#D4956A", border: "#2E2A26" },
  },
  earthy: {
    label: "طبیعی",
    desc: "ارگانیک، گرد، زمینی",
    class: "theme-earthy",
    preview: { bg: "#F4F7F2", text: "#1A2A18", accent: "#3A7D44", border: "#C8D8C4" },
  },
  scandinavian: {
    label: "اسکاندیناوی",
    desc: "گرم، طبیعی، آرام",
    class: "theme-scandinavian",
    preview: { bg: "#F7F5F2", text: "#4B4B4B", accent: "#6B5040", border: "#DCC5A1" },
  },
  swiss: {
    label: "Swiss",
    desc: "نظم مطلق، دقیق، تایپوگرافی",
    class: "theme-swiss",
    preview: { bg: "#FFFFFF", text: "#111111", accent: "#111111", border: "#111111" },
  },
  glass: {
    label: "Liquid Glass",
    desc: "شفاف، عمق، آینده‌نگر",
    class: "theme-glass",
    preview: { bg: "#dce8ff", text: "#1A237E", accent: "#5C6BC0", border: "rgba(255,255,255,0.5)" },
  },
};

// Backward-compat alias
export const THEMES = DESIGN_THEMES;

export const HEADER_VARIANTS = [
  { id: 1, label: "کلاسیک",  desc: "لوگو راست، ناوبری وسط" },
  { id: 2, label: "دوردیفه", desc: "لوگو مرکز، ناوبری ردیف دوم" },
  { id: 3, label: "پیل",     desc: "آیتم‌های گرد، سبک مدرن" },
  { id: 4, label: "جسورانه", desc: "نوار رنگی بالا، لوگو بزرگ" },
];

export const FOOTER_VARIANTS = [
  { id: 1, label: "کلاسیک", desc: "چهار ستون با اطلاعات کامل" },
  { id: 2, label: "مرکزی",  desc: "مینیمال، متمرکز، ساده" },
  { id: 3, label: "تاریک",  desc: "پس‌زمینه تیره، ایمپکت بالا" },
];

export const HERO_VARIANTS = [
  { id: 1, label: "پوشش",    desc: "تصویر تمام‌صفحه، متن روی آن" },
  { id: 2, label: "دو ستون", desc: "متن راست، تصویر چپ" },
  { id: 3, label: "مورب",    desc: "برش مورب پویا" },
];

export const CARD_VARIANTS = [
  { id: "standard",   label: "استاندارد", desc: "تصویر ۴/۵، متن زیر" },
  { id: "compact",    label: "فشرده",     desc: "مربع، چیدمان متراکم" },
  { id: "horizontal", label: "افقی",      desc: "تصویر کنار متن" },
];

export const BUTTON_STYLES = [
  { id: "sharp",   label: "تیز",    desc: "لبه‌های صاف، کلاسیک" },
  { id: "rounded", label: "گرد",    desc: "گوشه‌های ملایم" },
  { id: "pill",    label: "کپسولی", desc: "کاملاً گرد و مدرن" },
];

export const ACCENT_COLORS = [
  { id: "default", label: "بورگندی",   color: "#7A2232", class: "" },
  { id: "blue",    label: "ایندیگو",   color: "#3B5BDB", class: "accent-blue" },
  { id: "teal",    label: "فیروزه‌ای", color: "#0F766E", class: "accent-teal" },
  { id: "amber",   label: "کهربایی",   color: "#B45309", class: "accent-amber" },
  { id: "purple",  label: "بنفش",      color: "#7C3AED", class: "accent-purple" },
  { id: "rose",    label: "گلبهی",     color: "#BE185D", class: "accent-rose" },
];

export const PAGE_LIST = [
  { path: "/",         label: "صفحه اصلی" },
  { path: "/products", label: "محصولات" },
  { path: "/blog",     label: "بلاگ" },
  { path: "/about",    label: "درباره ما" },
  { path: "/contact",  label: "تماس" },
  { path: "/account",  label: "حساب کاربری" },
];

const THEME_CLASSES  = Object.values(DESIGN_THEMES).map((t) => t.class).filter(Boolean);
const BTN_CLASS_MAP  = { sharp: "", rounded: "ui-rounded", pill: "ui-pill" };
const ACCENT_CLASS_LIST = ACCENT_COLORS.map((a) => a.class).filter(Boolean);

export function applyDesignTheme(name) {
  const html = document.documentElement;
  THEME_CLASSES.forEach((c) => html.classList.remove(c));
  html.classList.remove("dark");
  const t = DESIGN_THEMES[name];
  if (t?.class === "theme-dark") html.classList.add("dark");
  else if (t?.class) html.classList.add(t.class);
}

function applyButtonStyle(style) {
  const html = document.documentElement;
  ["ui-rounded", "ui-pill"].forEach((c) => html.classList.remove(c));
  const cls = BTN_CLASS_MAP[style];
  if (cls) html.classList.add(cls);
}

function applyAccentColor(id) {
  const html = document.documentElement;
  ACCENT_CLASS_LIST.forEach((c) => html.classList.remove(c));
  const item = ACCENT_COLORS.find((a) => a.id === id);
  if (item?.class) html.classList.add(item.class);
}

if (typeof window !== "undefined") {
  window.addEventListener("message", (e) => {
    if (e.data?.type === "navar-design-preview") {
      applyDesignTheme(e.data.designTheme || "minimal");
      applyButtonStyle(e.data.buttonStyle || "sharp");
    }
  });
}

export const useLayoutStore = defineStore("layout", () => {
  const saved = (() => {
    try { return JSON.parse(localStorage.getItem("navar_layout_v3") || "{}"); }
    catch { return {}; }
  })();

  const themeName     = ref(saved.themeName     || "minimal");
  const headerVariant = ref(saved.headerVariant || 1);
  const footerVariant = ref(saved.footerVariant || 1);
  const heroVariant   = ref(saved.heroVariant   || 1);
  const cardVariant   = ref(saved.cardVariant   || "standard");
  const buttonStyle   = ref(saved.buttonStyle   || "sharp");
  const accentColor   = ref(saved.accentColor   || "default");
  const pageDesigns   = ref(saved.pageDesigns   || {});

  applyDesignTheme(themeName.value);
  applyButtonStyle(buttonStyle.value);
  applyAccentColor(accentColor.value);

  function save() {
    localStorage.setItem("navar_layout_v3", JSON.stringify({
      themeName: themeName.value, headerVariant: headerVariant.value,
      footerVariant: footerVariant.value, heroVariant: heroVariant.value,
      cardVariant: cardVariant.value, buttonStyle: buttonStyle.value,
      accentColor: accentColor.value, pageDesigns: pageDesigns.value,
    }));
  }

  function setPageDesign(path, theme) {
    pageDesigns.value = { ...pageDesigns.value, [path]: theme };
    save();
  }

  function getEffectiveDesign(path) {
    return pageDesigns.value[path] || themeName.value;
  }

  watch(themeName,   (n) => { applyDesignTheme(n);  save(); });
  watch(buttonStyle, (n) => { applyButtonStyle(n);  save(); });
  watch(accentColor, (n) => { applyAccentColor(n);  save(); });
  watch([headerVariant, footerVariant, heroVariant, cardVariant], save);

  return {
    themeName, headerVariant, footerVariant, heroVariant,
    cardVariant, buttonStyle, accentColor, pageDesigns,
    setPageDesign, getEffectiveDesign,
  };
});
