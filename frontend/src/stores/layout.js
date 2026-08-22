import { defineStore } from "pinia";
import { ref, watch } from "vue";
import { api } from "@/lib/api";
import { isDemoMode } from "@/lib/demo.js";
import { useThemeStore } from "@/stores/theme.js";

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
    class: "dark",
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
    preview: { bg: "#ebe5dd", text: "#3d2f26", accent: "#8A5A44", border: "rgba(255,255,255,0.58)" },
  },
};

export const THEMES = DESIGN_THEMES;

// A design preset carries a matching palette as well as component shapes.
// Manual color controls can still override these values afterwards.
export const DESIGN_COLOR_PRESETS = {
  minimal: { accentHue: 22, accentChroma: 0.09, accentLightness: 0.42, accentColor: "default", bgLightness: 0.982, bgChroma: 0.006, bgHue: 75 },
  bento: { accentHue: 22, accentChroma: 0.09, accentLightness: 0.42, accentColor: "default", bgLightness: 0.965, bgChroma: 0, bgHue: 0 },
  modern: { accentHue: 265, accentChroma: 0.22, accentLightness: 0.47, accentColor: "blue", bgLightness: 1, bgChroma: 0, bgHue: 240 },
  dark: { accentHue: 55, accentChroma: 0.14, accentLightness: 0.52, accentColor: "amber", bgLightness: 0.12, bgChroma: 0.005, bgHue: 60 },
  earthy: { accentHue: 185, accentChroma: 0.12, accentLightness: 0.43, accentColor: "teal", bgLightness: 0.972, bgChroma: 0.009, bgHue: 100 },
  scandinavian: { accentHue: 55, accentChroma: 0.14, accentLightness: 0.52, accentColor: "amber", bgLightness: 0.972, bgChroma: 0.01, bgHue: 75 },
  swiss: { accentHue: 22, accentChroma: 0.09, accentLightness: 0.42, accentColor: "default", bgLightness: 1, bgChroma: 0, bgHue: 0 },
  glass: { accentHue: 55, accentChroma: 0.14, accentLightness: 0.52, accentColor: "amber", bgLightness: 0.955, bgChroma: 0.018, bgHue: 75 },
};

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
  { id: "default", label: "بورگندی",   color: "#7A2232", class: "", accentHue: 22, accentChroma: 0.09, accentLightness: 0.42 },
  { id: "blue",    label: "ایندیگو",   color: "#3B5BDB", class: "accent-blue", accentHue: 265, accentChroma: 0.22, accentLightness: 0.47 },
  { id: "teal",    label: "فیروزه‌ای", color: "#0F766E", class: "accent-teal", accentHue: 185, accentChroma: 0.12, accentLightness: 0.43 },
  { id: "amber",   label: "کهربایی",   color: "#B45309", class: "accent-amber", accentHue: 55, accentChroma: 0.14, accentLightness: 0.52 },
  { id: "purple",  label: "بنفش",      color: "#7C3AED", class: "accent-purple", accentHue: 295, accentChroma: 0.18, accentLightness: 0.44 },
  { id: "rose",    label: "گلبهی",     color: "#BE185D", class: "accent-rose", accentHue: 340, accentChroma: 0.2, accentLightness: 0.47 },
];

export const PAGE_LIST = [
  { path: "/",              label: "صفحه اصلی" },
  { path: "/products",      label: "محصولات" },
  { path: "/products/:id",  label: "جزئیات محصول" },
  { path: "/blog",          label: "بلاگ" },
  { path: "/blog/:slug",    label: "مقاله بلاگ" },
  { path: "/about",         label: "درباره ما" },
  { path: "/contact",       label: "تماس" },
  { path: "/faq",           label: "سوالات متداول" },
  { path: "/cart",          label: "سبد خرید" },
  { path: "/checkout",      label: "تسویه حساب" },
  { path: "/wishlist",      label: "علاقه‌مندی‌ها" },
  { path: "/account",       label: "حساب کاربری" },
  { path: "/tracking",      label: "پیگیری سفارش" },
  { path: "/policies",      label: "قوانین سایت" },
];

// A component can inherit the active design, or opt into another design
// without changing the rest of the page. These keys are also used by the
// admin appearance panel and the themed component resolvers.
export const DESIGN_COMPONENTS = [
  { id: "layout", label: "چیدمان صفحه" },
  { id: "header", label: "هدر" },
  { id: "footer", label: "فوتر" },
  { id: "hero", label: "بنر اصلی" },
  { id: "sectionHeader", label: "عنوان بخش‌ها" },
  { id: "featuredGrid", label: "گرید منتخب" },
  { id: "productCard", label: "کارت محصول" },
];

const THEME_CLASSES  = Object.values(DESIGN_THEMES).map((t) => t.class).filter(Boolean);
const BTN_CLASS_MAP  = { sharp: "", rounded: "ui-rounded", pill: "ui-pill" };
const ACCENT_CLASS_LIST = ACCENT_COLORS.map((a) => a.class).filter(Boolean);

export function applyDesignTheme(name) {
  if (typeof document === "undefined") return;
  const html = document.documentElement;
  THEME_CLASSES.forEach((c) => html.classList.remove(c));
  const themeKey = DESIGN_THEMES[name] ? name : "minimal";
  const themeClass = DESIGN_THEMES[themeKey]?.class;
  if (themeClass) html.classList.add(themeClass);
  html.dataset.designTheme = themeKey;
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

export function resolvePagePath(path = "") {
  if (PAGE_LIST.some((page) => page.path === path)) return path;
  if (path.startsWith("/products/")) return "/products/:id";
  if (path.startsWith("/blog/")) return "/blog/:slug";
  return path;
}

function syncDesignColor(themeKey) {
  const preset = DESIGN_COLOR_PRESETS[themeKey];
  if (!preset) return;
  const colorPreset = { ...preset };
  delete colorPreset.accentColor;
  try {
    useThemeStore().setColorPreset({ ...colorPreset, designTheme: themeKey });
  } catch {
    // The layout store can also be used in isolated tooling without Pinia.
  }
}

function syncAccentColor(accentId) {
  const accent = ACCENT_COLORS.find((item) => item.id === accentId);
  if (!accent || accent.accentHue === undefined) return;
  try {
    useThemeStore().setColorPreset({
      accentHue: accent.accentHue,
      accentChroma: accent.accentChroma,
      accentLightness: accent.accentLightness,
    });
  } catch {
    // Keep the quick accent picker optional in isolated tooling.
  }
}

if (typeof window !== "undefined") {
  window.addEventListener("message", (e) => {
    if (e.data?.type === "navar-design-preview") {
      applyDesignTheme(e.data.designTheme || "minimal");
      applyButtonStyle(e.data.buttonStyle || "sharp");
      window.dispatchEvent(new CustomEvent("navar-design-preview-state", { detail: e.data }));
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
  const componentThemes = ref(saved.componentThemes || {});
  const pageComponentThemes = ref(saved.pageComponentThemes || {});

  function applyDesignPreviewState(data = {}) {
    if (DESIGN_THEMES[data.designTheme]) themeName.value = data.designTheme;
    if (BUTTON_STYLES.some((style) => style.id === data.buttonStyle)) buttonStyle.value = data.buttonStyle;
    if (data.pageDesigns && typeof data.pageDesigns === "object") pageDesigns.value = { ...data.pageDesigns };
    if (data.componentThemes && typeof data.componentThemes === "object") componentThemes.value = { ...data.componentThemes };
    if (data.pageComponentThemes && typeof data.pageComponentThemes === "object") {
      pageComponentThemes.value = { ...data.pageComponentThemes };
    }
  }

  if (typeof window !== "undefined") {
    window.addEventListener("navar-design-preview-state", (event) => {
      applyDesignPreviewState(event.detail);
    });
  }

  // Migrate older saved sessions and make the active design's palette the
  // first automatic choice. Once the marker matches, manual color edits are
  // left untouched on subsequent reloads.
  try {
    if (useThemeStore().theme.designTheme !== themeName.value) {
      syncDesignColor(themeName.value);
    }
  } catch {
    // Keep layout state usable in isolated tooling without a Pinia instance.
  }

  applyDesignTheme(themeName.value);
  applyButtonStyle(buttonStyle.value);
  applyAccentColor(accentColor.value);

  async function fetchLayout() {
    if (isDemoMode) return;
    try {
      const data = await api.admin.theme.get();
      if (data && data.layout) {
        const l = data.layout;
        if (l.themeName) {
          themeName.value = l.themeName;
          try {
            if (useThemeStore().theme.designTheme !== l.themeName) syncDesignColor(l.themeName);
          } catch {
            // keep the remote layout usable if color state is unavailable
          }
        }
        if (l.headerVariant) headerVariant.value = l.headerVariant;
        if (l.footerVariant) footerVariant.value = l.footerVariant;
        if (l.heroVariant) heroVariant.value = l.heroVariant;
        if (l.cardVariant) cardVariant.value = l.cardVariant;
        if (l.buttonStyle) buttonStyle.value = l.buttonStyle;
        if (l.accentColor) accentColor.value = l.accentColor;
        if (l.pageDesigns) pageDesigns.value = l.pageDesigns;
        if (l.componentThemes) componentThemes.value = l.componentThemes;
        if (l.pageComponentThemes) pageComponentThemes.value = l.pageComponentThemes;
        saveToStorage();
      }
    } catch {
      // use cached
    }
  }

  function saveToStorage() {
    localStorage.setItem("navar_layout_v3", JSON.stringify({
      themeName: themeName.value, headerVariant: headerVariant.value,
      footerVariant: footerVariant.value, heroVariant: heroVariant.value,
      cardVariant: cardVariant.value, buttonStyle: buttonStyle.value,
      accentColor: accentColor.value, pageDesigns: pageDesigns.value,
      componentThemes: componentThemes.value,
      pageComponentThemes: pageComponentThemes.value,
    }));
  }

  async function saveToServer() {
    if (isDemoMode) return;
    try {
      await api.admin.theme.update({
        layout: {
          themeName: themeName.value,
          headerVariant: headerVariant.value,
          footerVariant: footerVariant.value,
          heroVariant: heroVariant.value,
          cardVariant: cardVariant.value,
          buttonStyle: buttonStyle.value,
          accentColor: accentColor.value,
          pageDesigns: pageDesigns.value,
          componentThemes: componentThemes.value,
          pageComponentThemes: pageComponentThemes.value,
        },
      });
    } catch {
      // silent
    }
  }

  function save() {
    saveToStorage();
    saveToServer();
  }

  function setThemeName(name) {
    if (!DESIGN_THEMES[name]) return;
    themeName.value = name;
    if (DESIGN_COLOR_PRESETS[name]?.accentColor) {
      accentColor.value = DESIGN_COLOR_PRESETS[name].accentColor;
    }
    syncDesignColor(name);
  }

  function setPageDesign(path, theme) {
    pageDesigns.value = { ...pageDesigns.value, [path]: theme };
    save();
  }

  function getEffectiveDesign(path) {
    const pageKey = resolvePagePath(path);
    return pageDesigns.value[pageKey] || themeName.value;
  }

  function getComponentTheme(component, path = "") {
    const pageKey = resolvePagePath(path);
    const pageOverrides = pageComponentThemes.value[pageKey] || pageComponentThemes.value[path];
    if (pageOverrides && pageOverrides[component]) return pageOverrides[component];
    if (componentThemes.value[component]) return componentThemes.value[component];
    return getEffectiveDesign(path);
  }

  function setComponentTheme(component, theme, path = null) {
    if (path) {
      const next = { ...pageComponentThemes.value };
      const pageOverrides = { ...(next[path] || {}) };
      if (theme) pageOverrides[component] = theme;
      else delete pageOverrides[component];
      if (Object.keys(pageOverrides).length) next[path] = pageOverrides;
      else delete next[path];
      pageComponentThemes.value = next;
    } else {
      const next = { ...componentThemes.value };
      if (theme) next[component] = theme;
      else delete next[component];
      componentThemes.value = next;
    }
    save();
  }

  function clearComponentThemes(path = null) {
    if (path) {
      const next = { ...pageComponentThemes.value };
      delete next[path];
      pageComponentThemes.value = next;
    } else {
      componentThemes.value = {};
    }
    save();
  }

  watch(themeName,   (n) => { applyDesignTheme(n);  save(); });
  watch(buttonStyle, (n) => { applyButtonStyle(n);  save(); });
  watch(accentColor, (n) => { applyAccentColor(n); syncAccentColor(n); save(); });
  watch([headerVariant, footerVariant, heroVariant, cardVariant], save);

  fetchLayout();

  return {
    themeName, headerVariant, footerVariant, heroVariant,
    cardVariant, buttonStyle, accentColor, pageDesigns,
    componentThemes, pageComponentThemes,
    setThemeName, setPageDesign, getEffectiveDesign, getComponentTheme,
    setComponentTheme, clearComponentThemes,
  };
});
