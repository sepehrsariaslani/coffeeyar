<script setup>
import { ref, computed, watch, toRaw } from "vue";
import {
  useLayoutStore,
  DESIGN_THEMES, HEADER_VARIANTS, FOOTER_VARIANTS,
  HERO_VARIANTS, CARD_VARIANTS, BUTTON_STYLES, ACCENT_COLORS, PAGE_LIST, DESIGN_COMPONENTS,
} from "@/stores/layout.js";
import { useThemeStore } from "@/stores/theme.js";
import {
  Check, Palette, Layout, Square, Layers, Image, Type, Droplets,
  Monitor, Smartphone, RefreshCw, RotateCcw, Globe, Eye, Lock,
} from "lucide-vue-next";

const layoutStore = useLayoutStore();
const themeStore  = useThemeStore();
const t = computed(() => themeStore.theme);

const activeTab = ref("design");
const tabs = [
  { id: "design",     label: "تم طراحی",   icon: Palette },
  { id: "color",      label: "تم رنگی",    icon: Droplets },
  { id: "components", label: "کامپوننت‌ها", icon: Layers },
  { id: "pages",      label: "صفحات",       icon: Globe },
];

const componentThemeOptions = Object.entries(DESIGN_THEMES).map(([key, theme]) => ({ key, ...theme }));
const pageComponentOpen = ref({});

function togglePageComponents(path) {
  pageComponentOpen.value = {
    ...pageComponentOpen.value,
    [path]: !pageComponentOpen.value[path],
  };
}

function pageComponentTheme(path, component) {
  return layoutStore.pageComponentThemes[path]?.[component] || "";
}

function setPageComponentTheme(path, component, value) {
  layoutStore.setComponentTheme(component, value || null, path);
}

function clearAllPageOverrides() {
  PAGE_LIST.forEach((page) => {
    layoutStore.setPageDesign(page.path, null);
    layoutStore.clearComponentThemes(page.path);
  });
}

// ── Component preview styles per theme ───────────────
const COMP_PREVIEW = {
  minimal: {
    wrap: { background: "#FFFFFF", border: "1px solid #E8E8E8", padding: "16px" },
    nav:  { background: "#FFFFFF", borderBottom: "1px solid #E5E5E5", padding: "10px 16px", display: "flex", alignItems: "center", justifyContent: "space-between" },
    navLogo: { fontWeight: "700", fontSize: "14px", color: "#111111", letterSpacing: "-0.02em" },
    navLinks: { display: "flex", gap: "16px" },
    navLink: { fontSize: "11px", color: "#666666" },
    btnPrimary: { background: "#111111", color: "#FFFFFF", borderRadius: "10px", padding: "8px 18px", fontSize: "12px", fontWeight: "500", boxShadow: "0 1px 4px rgba(0,0,0,0.10)", border: "none", cursor: "default" },
    btnOutline: { background: "transparent", color: "#111111", borderRadius: "10px", padding: "8px 18px", fontSize: "12px", border: "1.5px solid #E0E0E0", cursor: "default" },
    card: { background: "#FFFFFF", border: "1px solid #E5E5E5", borderRadius: "10px", overflow: "hidden", boxShadow: "0 2px 8px rgba(0,0,0,0.05)" },
    cardTitle: { fontSize: "12px", fontWeight: "600", color: "#111111", marginBottom: "2px" },
    cardPrice: { fontSize: "11px", color: "#888888" },
    input: { background: "#F5F5F5", border: "1px solid #E5E5E5", borderRadius: "8px", padding: "8px 12px", fontSize: "12px", width: "100%", color: "#111111", outline: "none" },
    badge: { background: "#F5F5F5", color: "#444444", borderRadius: "4px", padding: "2px 7px", fontSize: "10px", display: "inline-block" },
    accentBar: "#111111",
  },
  bento: {
    wrap: { background: "#F0EFEC", border: "1px solid #E0DFDA", padding: "16px" },
    nav:  { background: "#FAFAF8", borderBottom: "1px solid #E4E4E0", padding: "10px 16px", display: "flex", alignItems: "center", justifyContent: "space-between" },
    navLogo: { fontWeight: "700", fontSize: "14px", color: "#111111" },
    navLinks: { display: "flex", gap: "14px" },
    navLink: { fontSize: "11px", color: "#666666" },
    btnPrimary: { background: "#111111", color: "#FFFFFF", borderRadius: "8px", padding: "8px 18px", fontSize: "12px", fontWeight: "600", border: "none", cursor: "default" },
    btnOutline: { background: "rgba(0,0,0,0.05)", color: "#111111", borderRadius: "8px", padding: "8px 18px", fontSize: "12px", border: "1px solid #D8D8D5", cursor: "default" },
    card: { background: "#E6E5E1", border: "none", borderRadius: "14px", overflow: "hidden" },
    cardTitle: { fontSize: "12px", fontWeight: "700", color: "#111111", marginBottom: "2px" },
    cardPrice: { fontSize: "11px", color: "#777777" },
    input: { background: "#FFFFFF", border: "1.5px solid #D5D5D0", borderRadius: "8px", padding: "8px 12px", fontSize: "12px", width: "100%", color: "#111111", outline: "none" },
    badge: { background: "#111111", color: "#FFFFFF", borderRadius: "6px", padding: "2px 7px", fontSize: "10px", display: "inline-block" },
    accentBar: "#333333",
  },
  modern: {
    wrap: { background: "#FFFFFF", border: "1px solid #E2E8F0", padding: "16px" },
    nav:  { background: "#FFFFFF", borderBottom: "1px solid #E2E8F0", padding: "10px 16px", display: "flex", alignItems: "center", justifyContent: "space-between" },
    navLogo: { fontWeight: "700", fontSize: "14px", color: "#0A0F1E" },
    navLinks: { display: "flex", gap: "14px" },
    navLink: { fontSize: "11px", color: "#64748B" },
    btnPrimary: { background: "#3B5BDB", color: "#FFFFFF", borderRadius: "8px", padding: "8px 18px", fontSize: "12px", fontWeight: "500", boxShadow: "0 4px 14px rgba(59,91,219,0.30)", border: "none", cursor: "default" },
    btnOutline: { background: "transparent", color: "#3B5BDB", borderRadius: "8px", padding: "8px 18px", fontSize: "12px", border: "1.5px solid #3B5BDB", cursor: "default" },
    card: { background: "#FFFFFF", border: "1px solid #E2E8F0", borderRadius: "12px", overflow: "hidden", boxShadow: "0 4px 24px rgba(59,91,219,0.07)" },
    cardTitle: { fontSize: "12px", fontWeight: "600", color: "#0A0F1E", marginBottom: "2px" },
    cardPrice: { fontSize: "11px", color: "#3B5BDB" },
    input: { background: "#FFFFFF", border: "1.5px solid #E2E8F0", borderRadius: "8px", padding: "8px 12px", fontSize: "12px", width: "100%", color: "#0A0F1E", outline: "none" },
    badge: { background: "rgba(59,91,219,0.1)", color: "#3B5BDB", borderRadius: "999px", padding: "2px 8px", fontSize: "10px", display: "inline-block" },
    accentBar: "#3B5BDB",
  },
  dark: {
    wrap: { background: "#161412", border: "1px solid #2E2A26", padding: "16px" },
    nav:  { background: "#1A1715", borderBottom: "1px solid rgba(255,255,255,0.08)", padding: "10px 16px", display: "flex", alignItems: "center", justifyContent: "space-between" },
    navLogo: { fontWeight: "700", fontSize: "14px", color: "#F5F0EA" },
    navLinks: { display: "flex", gap: "14px" },
    navLink: { fontSize: "11px", color: "#9A958F" },
    btnPrimary: { background: "#D4956A", color: "#0D0B09", borderRadius: "2px", padding: "8px 18px", fontSize: "12px", fontWeight: "700", border: "none", cursor: "default" },
    btnOutline: { background: "transparent", color: "#F5F0EA", borderRadius: "2px", padding: "8px 18px", fontSize: "12px", border: "1px solid rgba(255,255,255,0.15)", cursor: "default" },
    card: { background: "#1F1C19", border: "1px solid rgba(255,255,255,0.07)", borderRadius: "2px", overflow: "hidden", boxShadow: "0 2px 16px rgba(0,0,0,0.3)" },
    cardTitle: { fontSize: "12px", fontWeight: "600", color: "#F5F0EA", marginBottom: "2px" },
    cardPrice: { fontSize: "11px", color: "#D4956A" },
    input: { background: "rgba(255,255,255,0.07)", border: "1px solid rgba(255,255,255,0.12)", borderRadius: "2px", padding: "8px 12px", fontSize: "12px", width: "100%", color: "#F5F0EA", outline: "none" },
    badge: { background: "rgba(212,149,106,0.15)", color: "#D4956A", borderRadius: "2px", padding: "2px 7px", fontSize: "10px", display: "inline-block" },
    accentBar: "#D4956A",
  },
  earthy: {
    wrap: { background: "#F4F7F2", border: "1px solid #C8D8C4", padding: "16px" },
    nav:  { background: "#EDF2EB", borderBottom: "1px solid #C8D8C4", padding: "10px 16px", display: "flex", alignItems: "center", justifyContent: "space-between" },
    navLogo: { fontWeight: "700", fontSize: "14px", color: "#1A2A18" },
    navLinks: { display: "flex", gap: "14px" },
    navLink: { fontSize: "11px", color: "#4A6248" },
    btnPrimary: { background: "#3A7D44", color: "#FFFFFF", borderRadius: "6px", padding: "8px 18px", fontSize: "12px", fontWeight: "500", boxShadow: "0 2px 8px rgba(58,125,68,0.20)", border: "none", cursor: "default" },
    btnOutline: { background: "transparent", color: "#1A2A18", borderRadius: "6px", padding: "8px 18px", fontSize: "12px", border: "1px solid #C8D8C4", cursor: "default" },
    card: { background: "#F4F7F2", border: "1px solid #C8D8C4", borderRadius: "6px", overflow: "hidden", boxShadow: "0 2px 10px rgba(58,125,68,0.06)" },
    cardTitle: { fontSize: "12px", fontWeight: "600", color: "#1A2A18", marginBottom: "2px" },
    cardPrice: { fontSize: "11px", color: "#3A7D44" },
    input: { background: "#EDF2EB", border: "1px solid #C8D8C4", borderRadius: "6px", padding: "8px 12px", fontSize: "12px", width: "100%", color: "#1A2A18", outline: "none" },
    badge: { background: "rgba(58,125,68,0.12)", color: "#3A7D44", borderRadius: "4px", padding: "2px 7px", fontSize: "10px", display: "inline-block" },
    accentBar: "#3A7D44",
  },
  scandinavian: {
    wrap: { background: "#F7F5F2", border: "1px solid #DCC5A1", padding: "16px" },
    nav:  { background: "#F7F5F2", borderBottom: "1px solid #DCC5A1", padding: "10px 16px", display: "flex", alignItems: "center", justifyContent: "space-between" },
    navLogo: { fontWeight: "500", fontSize: "14px", color: "#4B4B4B", letterSpacing: "0.02em" },
    navLinks: { display: "flex", gap: "18px" },
    navLink: { fontSize: "11px", color: "#7A7268" },
    btnPrimary: { background: "#4B4B4B", color: "#FFFFFF", borderRadius: "4px", padding: "8px 18px", fontSize: "12px", fontWeight: "400", border: "none", cursor: "default" },
    btnOutline: { background: "transparent", color: "#4B4B4B", borderRadius: "4px", padding: "8px 18px", fontSize: "12px", border: "1px solid #DCC5A1", cursor: "default" },
    card: { background: "#F7F5F2", border: "1px solid #DCC5A1", borderRadius: "4px", overflow: "hidden", boxShadow: "0 2px 8px rgba(75,75,75,0.05)" },
    cardTitle: { fontSize: "12px", fontWeight: "500", color: "#4B4B4B", marginBottom: "2px" },
    cardPrice: { fontSize: "11px", color: "#A89B8C" },
    input: { background: "#FFFFFF", border: "1px solid #DCC5A1", borderRadius: "4px", padding: "8px 12px", fontSize: "12px", width: "100%", color: "#4B4B4B", outline: "none" },
    badge: { background: "#EDE6DA", color: "#7A7268", borderRadius: "2px", padding: "2px 7px", fontSize: "10px", display: "inline-block" },
    accentBar: "#6B5040",
  },
  swiss: {
    wrap: { background: "#FFFFFF", border: "2px solid #111111", padding: "16px" },
    nav:  { background: "#FFFFFF", borderBottom: "3px solid #111111", padding: "10px 16px", display: "flex", alignItems: "center", justifyContent: "space-between" },
    navLogo: { fontWeight: "900", fontSize: "14px", color: "#111111", letterSpacing: "-0.01em", textTransform: "uppercase" },
    navLinks: { display: "flex", gap: "16px" },
    navLink: { fontSize: "10px", color: "#444444", fontWeight: "700", letterSpacing: "0.08em", textTransform: "uppercase" },
    btnPrimary: { background: "#111111", color: "#FFFFFF", borderRadius: "0px", padding: "8px 20px", fontSize: "11px", fontWeight: "700", letterSpacing: "0.06em", textTransform: "uppercase", border: "none", cursor: "default" },
    btnOutline: { background: "transparent", color: "#111111", borderRadius: "0px", padding: "8px 20px", fontSize: "11px", fontWeight: "700", letterSpacing: "0.06em", textTransform: "uppercase", border: "2px solid #111111", cursor: "default" },
    card: { background: "#FFFFFF", border: "2px solid #111111", borderRadius: "0px", overflow: "hidden" },
    cardTitle: { fontSize: "12px", fontWeight: "700", color: "#111111", letterSpacing: "0.02em", marginBottom: "2px" },
    cardPrice: { fontSize: "11px", color: "#444444", fontWeight: "500" },
    input: { background: "#FFFFFF", border: "2px solid #111111", borderRadius: "0px", padding: "8px 12px", fontSize: "12px", width: "100%", color: "#111111", outline: "none", fontWeight: "500" },
    badge: { background: "#111111", color: "#FFFFFF", borderRadius: "0px", padding: "2px 7px", fontSize: "10px", fontWeight: "700", letterSpacing: "0.06em", textTransform: "uppercase", display: "inline-block" },
    accentBar: "#111111",
  },
  glass: {
    wrapIsGradient: true,
    wrap: { background: "linear-gradient(135deg, oklch(0.72 0.18 280) 0%, oklch(0.78 0.08 270) 50%, oklch(0.7 0.2 340) 100%)", padding: "16px" },
    nav:  { background: "rgba(255,255,255,0.45)", backdropFilter: "blur(20px)", borderBottom: "1px solid rgba(255,255,255,0.45)", padding: "10px 16px", display: "flex", alignItems: "center", justifyContent: "space-between" },
    navLogo: { fontWeight: "600", fontSize: "14px", color: "#1A237E" },
    navLinks: { display: "flex", gap: "14px" },
    navLink: { fontSize: "11px", color: "#3949AB" },
    btnPrimary: { background: "rgba(92,107,192,0.85)", color: "#FFFFFF", borderRadius: "999px", padding: "8px 18px", fontSize: "12px", fontWeight: "500", boxShadow: "0 4px 16px rgba(80,60,200,0.3), inset 0 1px 0 rgba(255,255,255,0.3)", border: "1px solid rgba(255,255,255,0.3)", cursor: "default", backdropFilter: "blur(10px)" },
    btnOutline: { background: "rgba(255,255,255,0.35)", color: "#1A237E", borderRadius: "999px", padding: "8px 18px", fontSize: "12px", border: "1px solid rgba(255,255,255,0.55)", cursor: "default", backdropFilter: "blur(10px)" },
    card: { background: "rgba(255,255,255,0.42)", border: "1px solid rgba(255,255,255,0.55)", borderRadius: "20px", overflow: "hidden", boxShadow: "inset 0 2px 1px rgba(255,255,255,0.65), 0 12px 40px rgba(80,60,200,0.15)", backdropFilter: "blur(24px)" },
    cardTitle: { fontSize: "12px", fontWeight: "600", color: "#1A237E", marginBottom: "2px" },
    cardPrice: { fontSize: "11px", color: "#5C6BC0" },
    input: { background: "rgba(255,255,255,0.45)", border: "1px solid rgba(255,255,255,0.5)", borderRadius: "10px", padding: "8px 12px", fontSize: "12px", width: "100%", color: "#1A237E", outline: "none", backdropFilter: "blur(10px)" },
    badge: { background: "rgba(255,255,255,0.4)", color: "#3949AB", borderRadius: "999px", padding: "2px 8px", fontSize: "10px", border: "1px solid rgba(255,255,255,0.5)", display: "inline-block" },
    accentBar: "#5C6BC0",
  },
};

const compPreview = computed(() => COMP_PREVIEW[layoutStore.themeName] || COMP_PREVIEW.minimal);

// ── Live Preview ──────────────────────────────────────
const iframeRef       = ref(null);
const mobileIframeRef = ref(null);
const previewReady    = ref(false);
const previewDevice   = ref("desktop");
const previewPage   = ref("/");
const iframeKey     = ref(0);

const PREVIEW_PAGES = [
  { path: "/",         label: "خانه" },
  { path: "/products", label: "محصولات" },
  { path: "/blog",     label: "بلاگ" },
  { path: "/about",    label: "درباره ما" },
];

const IFRAME_W  = 1280;
const IFRAME_H  = 2600;   // tall enough for full page — panel scrolls
const PANEL_W   = 490;
const MOB_W     = 390;
const MOB_H     = 2400;
const desktopScale = computed(() => PANEL_W / IFRAME_W);
const mobileScale  = computed(() => (PANEL_W * 0.44) / MOB_W);

function postToFrame(frame, message) {
  try { frame?.contentWindow?.postMessage(message, "*"); } catch {}
}

function postToFrames(message) {
  postToFrame(iframeRef.value, message);
  postToFrame(mobileIframeRef.value, message);
}

function sendColorToIframe(val) {
  postToFrames({ type: "navar-theme-preview", theme: toRaw(val) });
}

function sendDesignToIframe() {
  postToFrames({
    type: "navar-design-preview",
    designTheme: layoutStore.themeName,
    buttonStyle: layoutStore.buttonStyle,
    pageDesigns: toRaw(layoutStore.pageDesigns),
    componentThemes: toRaw(layoutStore.componentThemes),
    pageComponentThemes: toRaw(layoutStore.pageComponentThemes),
  });
}

function onIframeLoad(event) {
  previewReady.value = true;
  setTimeout(() => {
    const frame = event?.target;
    postToFrame(frame, { type: "navar-theme-preview", theme: toRaw(themeStore.theme) });
    postToFrame(frame, {
      type: "navar-design-preview",
      designTheme: layoutStore.themeName,
      buttonStyle: layoutStore.buttonStyle,
      pageDesigns: toRaw(layoutStore.pageDesigns),
      componentThemes: toRaw(layoutStore.componentThemes),
      pageComponentThemes: toRaw(layoutStore.pageComponentThemes),
    });
  }, 120);
}
function switchPage(path) { previewPage.value = path; previewReady.value = false; iframeKey.value++; }
function reloadPreview() { previewReady.value = false; iframeKey.value++; }

let rafId = null;
watch(() => themeStore.theme, (val) => {
  if (rafId) cancelAnimationFrame(rafId);
  rafId = requestAnimationFrame(() => sendColorToIframe(toRaw(val)));
}, { deep: true });
watch(
  [
    () => layoutStore.themeName,
    () => layoutStore.buttonStyle,
    () => layoutStore.pageDesigns,
    () => layoutStore.componentThemes,
    () => layoutStore.pageComponentThemes,
  ],
  () => {
    if (rafId) cancelAnimationFrame(rafId);
    rafId = requestAnimationFrame(() => sendDesignToIframe());
  },
  { deep: true },
);

// ── Full coordinated color palettes ─────────────────
const FULL_PRESETS = [
  {
    id: "navar",     label: "نوار اصیل",   desc: "مارون گرم روی کرم کلاسیک",
    swatches: ["oklch(0.982 0.006 75)", "oklch(0.42 0.09 22)"],
    v: { accentHue:22,  accentChroma:0.09,  accentLightness:0.42, bgLightness:0.982, bgChroma:0.006, bgHue:75  },
  },
  {
    id: "ocean",     label: "اقیانوس",     desc: "فیروزه‌ای عمیق روی آبی یخی",
    swatches: ["oklch(0.978 0.008 220)", "oklch(0.42 0.13 200)"],
    v: { accentHue:200, accentChroma:0.13,  accentLightness:0.42, bgLightness:0.978, bgChroma:0.008, bgHue:220 },
  },
  {
    id: "forest",    label: "جنگل",        desc: "سبز عمیق روی سبز مه‌آلود",
    swatches: ["oklch(0.978 0.007 140)", "oklch(0.40 0.13 145)"],
    v: { accentHue:145, accentChroma:0.13,  accentLightness:0.40, bgLightness:0.978, bgChroma:0.007, bgHue:140 },
  },
  {
    id: "sahara",    label: "صحرا",        desc: "عنبر گرم روی شن‌های کرم",
    swatches: ["oklch(0.980 0.010 65)",  "oklch(0.50 0.14 55)"],
    v: { accentHue:55,  accentChroma:0.14,  accentLightness:0.50, bgLightness:0.980, bgChroma:0.010, bgHue:65  },
  },
  {
    id: "midnight",  label: "نیمه‌شب",   desc: "بنفش تیره روی سفید خنثی",
    swatches: ["oklch(1.000 0 0)",        "oklch(0.40 0.18 295)"],
    v: { accentHue:295, accentChroma:0.18,  accentLightness:0.40, bgLightness:1.000, bgChroma:0,     bgHue:0   },
  },
  {
    id: "blossom",   label: "شکوفه",      desc: "گلابی ملایم روی کرم صورتی",
    swatches: ["oklch(0.978 0.008 10)",   "oklch(0.46 0.20 340)"],
    v: { accentHue:340, accentChroma:0.20,  accentLightness:0.46, bgLightness:0.978, bgChroma:0.008, bgHue:10  },
  },
  {
    id: "coal",      label: "زغال‌سنگ",  desc: "مشکی عمیق روی سفید سرد",
    swatches: ["oklch(0.975 0.003 240)",  "oklch(0.22 0 0)"],
    v: { accentHue:0,   accentChroma:0,     accentLightness:0.22, bgLightness:0.975, bgChroma:0.003, bgHue:240 },
  },
  {
    id: "indigo",    label: "ایندیگو",    desc: "آبی نیلی روی آبی پریده",
    swatches: ["oklch(0.978 0.006 260)",  "oklch(0.42 0.22 265)"],
    v: { accentHue:265, accentChroma:0.22,  accentLightness:0.42, bgLightness:0.978, bgChroma:0.006, bgHue:260 },
  },
];

function applyFullPreset(preset) {
  Object.assign(themeStore.theme, preset.v);
}
function isFullPresetActive(preset) {
  const v = preset.v;
  return Math.round(themeStore.theme.accentHue) === v.accentHue
    && Math.round(themeStore.theme.bgLightness * 1000) === Math.round(v.bgLightness * 1000);
}

// ── Fine-tune presets ────────────────────────────────
const accentPresets = [
  { label: "مارون",     accentHue: 22,  accentChroma: 0.09, accentLightness: 0.42 },
  { label: "قهوه‌ای",  accentHue: 40,  accentChroma: 0.10, accentLightness: 0.40 },
  { label: "زیتون",    accentHue: 120, accentChroma: 0.07, accentLightness: 0.38 },
  { label: "آبی نیلی", accentHue: 230, accentChroma: 0.10, accentLightness: 0.40 },
  { label: "بنفش",     accentHue: 280, accentChroma: 0.10, accentLightness: 0.38 },
  { label: "خاکستری",  accentHue: 0,   accentChroma: 0,    accentLightness: 0.35 },
];
const bgPresets = [
  { label: "کرم",       bgLightness: 0.982, bgChroma: 0.006, bgHue: 75  },
  { label: "سفید",      bgLightness: 1.000, bgChroma: 0,     bgHue: 0   },
  { label: "کرم گرم",  bgLightness: 0.975, bgChroma: 0.010, bgHue: 70  },
  { label: "خاکستری",  bgLightness: 0.970, bgChroma: 0.002, bgHue: 240 },
  { label: "صورتی",    bgLightness: 0.978, bgChroma: 0.008, bgHue: 10  },
  { label: "سبز",      bgLightness: 0.978, bgChroma: 0.007, bgHue: 140 },
];
function applyAccentPreset(p) { themeStore.theme.accentHue = p.accentHue; themeStore.theme.accentChroma = p.accentChroma; themeStore.theme.accentLightness = p.accentLightness; }
function applyBgPreset(p) { themeStore.theme.bgLightness = p.bgLightness; themeStore.theme.bgChroma = p.bgChroma; themeStore.theme.bgHue = p.bgHue; }
const accentCss = (p) => `oklch(${p.accentLightness} ${p.accentChroma} ${p.accentHue})`;
const bgCss     = (p) => `oklch(${p.bgLightness} ${p.bgChroma} ${p.bgHue})`;
const currentAccent  = computed(() => accentCss(t.value));
const currentBg      = computed(() => bgCss(t.value));
const currentMuted   = computed(() => `oklch(${(t.value.bgLightness - 0.02).toFixed(3)} ${t.value.bgChroma} ${t.value.bgHue})`);
const currentBorder  = computed(() => `oklch(${(t.value.bgLightness - 0.10).toFixed(3)} ${(t.value.bgChroma * 0.5).toFixed(3)} ${t.value.bgHue})`);
const currentSidebar = computed(() => `oklch(${Math.min(t.value.bgLightness + 0.01, 1).toFixed(3)} ${t.value.bgChroma} ${t.value.bgHue})`);

function activeClass(cond) {
  return cond ? "border-maroon bg-maroon/5 text-foreground" : "border-border hover:border-maroon/40 hover:bg-accent/40";
}
function isAccentPresetActive(p) {
  return Math.round(themeStore.theme.accentHue) === p.accentHue && Math.round(themeStore.theme.accentChroma * 100) === Math.round(p.accentChroma * 100);
}
function isBgPresetActive(p) {
  return Math.round(themeStore.theme.bgLightness * 1000) === Math.round(p.bgLightness * 1000);
}
</script>

<template>
  <div class="flex h-screen overflow-hidden" dir="rtl">

    <!-- ═══ LEFT PANEL — Controls ═══════════════════════ -->
    <div class="flex flex-col flex-1 min-w-0 overflow-hidden">

      <!-- Header -->
      <div class="border-b border-border bg-background px-6 py-4 shrink-0">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 class="text-2xl font-light">ظاهر و قالب <span class="text-maroon">.</span></h1>
            <p class="mt-0.5 text-xs text-muted-foreground">تمام تنظیمات ظاهری — تغییرات آنی در پیش‌نمایش اعمال می‌شن</p>
          </div>
          <div class="flex items-center gap-2 border border-border px-3 py-1.5 text-xs">
            <span class="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
            تم فعال: <strong class="text-maroon">{{ DESIGN_THEMES[layoutStore.themeName]?.label }}</strong>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="border-b border-border bg-background shrink-0 px-6 flex gap-0">
        <button
          v-for="tab in tabs" :key="tab.id" type="button"
          @click="activeTab = tab.id"
          :class="['flex items-center gap-2 px-4 py-3 text-sm border-b-2 transition-colors', activeTab === tab.id ? 'border-maroon text-maroon font-medium' : 'border-transparent text-muted-foreground hover:text-foreground']"
        >
          <component :is="tab.icon" class="h-3.5 w-3.5" />{{ tab.label }}
        </button>
      </div>

      <!-- Content -->
      <div class="flex-1 overflow-y-auto">

        <!-- ══ TAB: DESIGN THEME ═════════════════════════ -->
        <div v-if="activeTab === 'design'" class="p-6 space-y-6">

          <p class="text-xs text-muted-foreground">تم طراحی سبک بصری کامپوننت‌ها رو تعیین می‌کنه — شکل، گوشه‌ها، سایه. رنگ‌ها تغییر نمی‌کنن.</p>

          <!-- Theme grid -->
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
            <button
              v-for="(theme, key) in DESIGN_THEMES" :key="key"
              type="button"
              @click="layoutStore.themeName = key"
              :class="['group relative border-2 text-right overflow-hidden transition-all', layoutStore.themeName === key ? 'border-maroon ring-2 ring-maroon/20' : 'border-border hover:border-maroon/40']"
            >
              <!-- Visual mockup -->
              <div class="h-32 flex flex-col overflow-hidden" :style="{ background: theme.preview.bg }">
                <!-- Mini nav -->
                <div class="flex items-center justify-between px-2.5 py-1.5 border-b" :style="{ borderColor: theme.preview.border }">
                  <div class="h-1.5 w-8 rounded-sm opacity-80" :style="{ background: theme.preview.text }" />
                  <div class="flex gap-1.5">
                    <div class="h-1 w-5 rounded-sm opacity-40" :style="{ background: theme.preview.text }" />
                    <div class="h-1 w-5 rounded-sm opacity-40" :style="{ background: theme.preview.text }" />
                    <div class="h-1 w-5 rounded-sm opacity-40" :style="{ background: theme.preview.text }" />
                  </div>
                </div>
                <!-- Hero snippet -->
                <div class="flex-1 px-2.5 py-2 flex flex-col justify-between">
                  <div class="space-y-1">
                    <div class="h-2 w-3/4 rounded-sm opacity-60" :style="{ background: theme.preview.text }" />
                    <div class="h-1.5 w-full rounded-sm opacity-30" :style="{ background: theme.preview.text }" />
                  </div>
                  <!-- Mini button styled per theme -->
                  <div class="flex items-center gap-1.5 mt-1">
                    <div
                      class="h-5 px-2.5 text-[8px] flex items-center font-semibold"
                      :style="{
                        background: theme.preview.accent,
                        color: key === 'dark' ? '#0D0B09' : '#fff',
                        borderRadius: key === 'minimal' ? '6px' : key === 'glass' ? '999px' : key === 'swiss' ? '0' : key === 'scandinavian' ? '3px' : key === 'bento' ? '6px' : '5px',
                        border: key === 'swiss' ? '2px solid ' + theme.preview.text : 'none',
                        textTransform: key === 'swiss' ? 'uppercase' : 'none',
                        letterSpacing: key === 'swiss' ? '0.06em' : 'normal',
                      }"
                    >دکمه</div>
                    <!-- Mini card -->
                    <div
                      class="flex-1 h-9 overflow-hidden"
                      :style="{
                        background: key === 'bento' ? 'oklch(0.91 0 0)' : key === 'dark' ? '#1F1C19' : theme.preview.bg,
                        border: '1px solid ' + theme.preview.border,
                        borderRadius: key === 'minimal' ? '5px' : key === 'glass' ? '10px' : key === 'swiss' ? '0' : key === 'scandinavian' ? '3px' : key === 'bento' ? '8px' : '6px',
                        boxShadow: key === 'glass' ? 'inset 0 1px 0 rgba(255,255,255,0.5)' : 'none',
                      }"
                    >
                      <div class="h-5 opacity-20" :style="{ background: theme.preview.text }" />
                      <div class="px-1 pt-0.5">
                        <div class="h-1 w-3/4 rounded-sm opacity-40" :style="{ background: theme.preview.text }" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- Label -->
              <div class="px-3 py-2.5 border-t flex items-center justify-between" :style="{ borderColor: theme.preview.border, background: theme.preview.bg }">
                <div>
                  <div class="text-xs font-semibold" :style="{ color: theme.preview.text }">{{ theme.label }}</div>
                  <div class="text-[10px] opacity-55 mt-0.5" :style="{ color: theme.preview.text }">{{ theme.desc }}</div>
                </div>
                <div v-if="layoutStore.themeName === key" class="h-5 w-5 bg-maroon text-white flex items-center justify-center rounded-full shrink-0">
                  <Check class="h-3 w-3" />
                </div>
              </div>
            </button>
          </div>

          <!-- ── Component Preview Panel ── -->
          <div class="border border-border bg-muted/20">
            <div class="border-b border-border px-5 py-3 flex items-center justify-between">
              <div>
                <div class="text-xs font-semibold text-maroon uppercase tracking-widest">پیش‌نمایش کامپوننت‌ها</div>
                <div class="text-xs text-muted-foreground mt-0.5">طراحی دکمه، کارت، ورودی و هدر در تم «{{ DESIGN_THEMES[layoutStore.themeName]?.label }}»</div>
              </div>
              <div
                class="h-2 w-2 rounded-full animate-pulse"
                :style="{ background: compPreview.accentBar }"
              />
            </div>

            <div class="p-5 grid grid-cols-1 sm:grid-cols-2 gap-4">

              <!-- BUTTONS -->
              <div>
                <div class="text-[10px] text-muted-foreground uppercase tracking-widest mb-2">دکمه‌ها</div>
                <div class="p-4 rounded-sm" :style="compPreview.wrap">
                  <div class="flex gap-2 flex-wrap">
                    <button :style="compPreview.btnPrimary">مشاهده محصولات</button>
                    <button :style="compPreview.btnOutline">بیشتر بدانید</button>
                  </div>
                </div>
              </div>

              <!-- CARD -->
              <div>
                <div class="text-[10px] text-muted-foreground uppercase tracking-widest mb-2">کارت محصول</div>
                <div class="p-4 rounded-sm" :style="compPreview.wrap">
                  <div :style="{ ...compPreview.card, maxWidth: '150px' }">
                    <div :style="{ height: '70px', background: compPreview.accentBar + '22', display: 'flex', alignItems: 'center', justifyContent: 'center' }">
                      <div :style="{ width: '32px', height: '32px', borderRadius: '50%', background: compPreview.accentBar + '44' }" />
                    </div>
                    <div style="padding: 10px">
                      <div :style="compPreview.cardTitle">قهوه اتیوپی</div>
                      <div :style="compPreview.cardPrice">۱۵۰,۰۰۰ تومان</div>
                      <div style="margin-top:8px">
                        <button :style="{ ...compPreview.btnPrimary, padding: '4px 12px', fontSize: '10px' }">افزودن</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- INPUT -->
              <div>
                <div class="text-[10px] text-muted-foreground uppercase tracking-widest mb-2">فیلد ورودی</div>
                <div class="p-4 rounded-sm" :style="compPreview.wrap">
                  <input :style="compPreview.input" placeholder="جستجو در محصولات..." readonly />
                  <div style="margin-top: 8px">
                    <span :style="compPreview.badge">ارگانیک</span>
                    &nbsp;
                    <span :style="compPreview.badge">تک‌خاستگاه</span>
                    &nbsp;
                    <span :style="compPreview.badge">برزیل</span>
                  </div>
                </div>
              </div>

              <!-- HEADER / NAV -->
              <div>
                <div class="text-[10px] text-muted-foreground uppercase tracking-widest mb-2">نوار ناوبری</div>
                <div class="rounded-sm overflow-hidden" :style="{ border: compPreview.wrap.border }">
                  <div :style="compPreview.nav">
                    <span :style="compPreview.navLogo">نـوار.</span>
                    <div :style="compPreview.navLinks">
                      <span v-for="lbl in ['خانه','محصولات','بلاگ']" :key="lbl" :style="compPreview.navLink">{{ lbl }}</span>
                    </div>
                    <button :style="{ ...compPreview.btnPrimary, padding: '4px 10px', fontSize: '10px' }">ورود</button>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- Glass notice -->
          <Transition name="fade">
            <div v-if="layoutStore.themeName === 'glass'" class="flex items-start gap-3 rounded-xl p-4" style="background: rgba(255,255,255,0.4); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.6);">
              <span class="text-lg shrink-0">✦</span>
              <div>
                <p class="text-sm font-medium">Liquid Glass فعال است</p>
                <p class="text-xs text-muted-foreground mt-1">تمام سطح‌های سایت شفاف و شیشه‌ای می‌شن. پس‌زمینه رنگارنگ از زیر شیشه دیده می‌شه.</p>
              </div>
            </div>
          </Transition>

        </div>

        <!-- ══ TAB: COLOR THEME ══════════════════════════ -->
        <div v-else-if="activeTab === 'color'" class="p-6 space-y-6">

          <p class="text-xs text-muted-foreground">تم رنگی فقط رنگ‌ها رو تغییر می‌ده — بدون تأثیر روی شکل کامپوننت‌ها.</p>

          <!-- ── Full Coordinated Presets ───────────────── -->
          <section class="border border-border p-5">
            <div class="flex items-center gap-2 mb-1">
              <Palette class="h-3.5 w-3.5 text-maroon" />
              <h2 class="text-sm font-medium">پریست‌های کامل</h2>
            </div>
            <p class="text-xs text-muted-foreground mb-4">با یک کلیک رنگ اکسنت + پس‌زمینه رو همزمان تغییر بده</p>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
              <button
                v-for="preset in FULL_PRESETS" :key="preset.id"
                type="button"
                @click="applyFullPreset(preset)"
                :class="[
                  'flex flex-col items-start gap-2 p-3 border transition-all text-right',
                  isFullPresetActive(preset)
                    ? 'border-foreground shadow-sm bg-accent/30'
                    : 'border-border hover:border-foreground/40 hover:bg-accent/20'
                ]"
              >
                <!-- Swatch pair -->
                <div class="flex gap-1 w-full">
                  <div class="h-6 flex-1 rounded-sm border border-black/10 shadow-sm" :style="{ background: preset.swatches[0] }" />
                  <div class="h-6 flex-1 rounded-sm border border-black/10 shadow-sm" :style="{ background: preset.swatches[1] }" />
                </div>
                <div class="flex items-center justify-between w-full">
                  <span class="text-[11px] font-medium text-foreground">{{ preset.label }}</span>
                  <Check v-if="isFullPresetActive(preset)" class="h-3 w-3 text-maroon shrink-0" />
                </div>
                <p class="text-[9px] text-muted-foreground leading-tight">{{ preset.desc }}</p>
              </button>
            </div>
          </section>

          <!-- Live palette -->
          <section class="border border-border p-5">
            <div class="flex items-center gap-2 mb-4">
              <Eye class="h-3.5 w-3.5 text-maroon" />
              <span class="text-xs font-medium">پالت رنگی فعلی</span>
            </div>
            <div class="flex flex-wrap gap-4">
              <div v-for="sw in [
                { label: 'پس‌زمینه',  color: currentBg },
                { label: 'رنگ تأکید', color: currentAccent },
                { label: 'خاکستری',   color: currentMuted },
                { label: 'حاشیه',     color: currentBorder },
                { label: 'سایدبار',   color: currentSidebar },
              ]" :key="sw.label" class="flex flex-col items-center gap-1.5">
                <div class="h-12 w-12 rounded-md border border-black/10 shadow-sm" :style="{ background: sw.color }" />
                <span class="text-[10px] text-muted-foreground">{{ sw.label }}</span>
                <span class="text-[9px] font-mono text-muted-foreground/50 text-center max-w-[52px] break-all leading-tight">{{ sw.color.replace('oklch(','').replace(')','') }}</span>
              </div>
            </div>
          </section>

          <!-- Accent presets -->
          <section class="border border-border p-5">
            <h2 class="text-sm font-medium mb-1">رنگ اکسنت</h2>
            <p class="text-xs text-muted-foreground mb-4">دکمه‌ها، لینک‌ها و المان‌های تأکیدی</p>
            <div class="grid grid-cols-3 sm:grid-cols-6 gap-2 mb-5">
              <button v-for="p in accentPresets" :key="p.label" type="button" @click="applyAccentPreset(p)"
                :class="['flex flex-col items-center gap-1.5 p-2.5 border transition-all', isAccentPresetActive(p) ? 'border-foreground shadow-sm bg-accent/40' : 'border-border hover:border-foreground/40']">
                <span class="h-7 w-7 rounded-full border border-black/10 shadow-sm" :style="{ background: accentCss(p) }" />
                <span class="text-[10px] text-center text-muted-foreground leading-tight">{{ p.label }}</span>
              </button>
            </div>
            <div class="space-y-3">
              <div v-for="[key, min, max, step, label] in [['accentHue',0,360,1,'هیو'],['accentChroma',0,0.25,0.005,'کروما'],['accentLightness',0.2,0.7,0.01,'روشنایی']]" :key="key"
                class="grid grid-cols-[1fr_auto] items-center gap-3">
                <div>
                  <div class="text-xs text-muted-foreground mb-1">{{ label }}</div>
                  <input type="range" :min="min" :max="max" :step="step" v-model.number="t[key]" class="w-full h-1.5 rounded cursor-pointer accent-[var(--maroon)]" />
                </div>
                <span class="w-10 text-center text-xs tabular-nums text-muted-foreground">{{ typeof t[key] === 'number' && step < 1 ? t[key].toFixed(2) : t[key] }}</span>
              </div>
            </div>
            <div class="mt-4 flex items-center gap-3">
              <span class="h-8 w-8 rounded-sm border border-black/10 shadow-sm" :style="{ background: currentAccent }" />
              <span class="text-xs font-mono text-muted-foreground">{{ currentAccent }}</span>
            </div>
          </section>

          <!-- BG presets -->
          <section class="border border-border p-5">
            <h2 class="text-sm font-medium mb-1">رنگ پس‌زمینه</h2>
            <p class="text-xs text-muted-foreground mb-4">پس‌زمینه کلی صفحات</p>
            <div class="grid grid-cols-3 sm:grid-cols-6 gap-2 mb-5">
              <button v-for="p in bgPresets" :key="p.label" type="button" @click="applyBgPreset(p)"
                :class="['flex flex-col items-center gap-1.5 p-2.5 border transition-all', isBgPresetActive(p) ? 'border-foreground shadow-sm bg-accent/40' : 'border-border hover:border-foreground/40']">
                <span class="h-7 w-7 rounded-full border border-black/20 shadow-sm" :style="{ background: bgCss(p) }" />
                <span class="text-[10px] text-center text-muted-foreground leading-tight">{{ p.label }}</span>
              </button>
            </div>
            <div class="space-y-3">
              <div v-for="[key, min, max, step, label] in [['bgLightness',0.95,1.0,0.001,'روشنایی'],['bgChroma',0,0.02,0.001,'کروما'],['bgHue',0,360,1,'هیو']]" :key="key"
                class="grid grid-cols-[1fr_auto] items-center gap-3">
                <div>
                  <div class="text-xs text-muted-foreground mb-1">{{ label }}</div>
                  <input type="range" :min="min" :max="max" :step="step" v-model.number="t[key]" class="w-full h-1.5 rounded cursor-pointer accent-[var(--maroon)]" />
                </div>
                <span class="w-12 text-center text-xs tabular-nums text-muted-foreground">{{ typeof t[key] === 'number' && step < 1 ? t[key].toFixed(3) : t[key] }}</span>
              </div>
            </div>
            <div class="mt-4 flex items-center justify-between">
              <div class="flex items-center gap-3">
                <span class="h-8 w-8 rounded-sm border border-black/20 shadow-sm" :style="{ background: currentBg }" />
                <span class="text-xs font-mono text-muted-foreground">{{ currentBg }}</span>
              </div>
              <button type="button" @click="themeStore.reset()" class="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground border border-border px-3 py-1.5">
                <RotateCcw class="h-3 w-3" /> بازنشانی
              </button>
            </div>
          </section>
        </div>

        <!-- ══ TAB: COMPONENTS ═══════════════════════════ -->
        <div v-else-if="activeTab === 'components'" class="p-6 space-y-8">

          <p class="text-xs text-muted-foreground">هر کامپوننت به‌صورت پیش‌فرض از تم کلی ارث می‌برد. اگر برای یک کامپوننت تم دیگری انتخاب کنید، فقط همان بخش تغییر می‌کند و بقیه صفحه دست‌نخورده می‌ماند.</p>

          <!-- Component design inheritance -->
          <section class="border border-border bg-muted/20 p-5">
            <div class="mb-4 flex items-start justify-between gap-4">
              <div>
                <div class="flex items-center gap-2">
                  <Layers class="h-4 w-4 text-maroon" />
                  <h2 class="text-sm font-medium">تم هر کامپوننت</h2>
                </div>
                <p class="mt-1 text-xs leading-6 text-muted-foreground">«همگام با تم کلی» یعنی انتخاب شما از تم صفحه و سپس تم کلی پیروی می‌کند.</p>
              </div>
              <button
                type="button"
                @click="layoutStore.clearComponentThemes()"
                class="shrink-0 border border-dashed border-border px-3 py-1.5 text-[10px] text-muted-foreground transition-colors hover:border-maroon hover:text-maroon"
              >
                پاک‌سازی overrides
              </button>
            </div>

            <div class="grid gap-2 sm:grid-cols-2">
              <label
                v-for="component in DESIGN_COMPONENTS"
                :key="component.id"
                class="flex items-center justify-between gap-3 border border-border bg-background px-3 py-2.5"
              >
                <span class="text-xs font-medium">{{ component.label }}</span>
                <select
                  :value="layoutStore.componentThemes[component.id] || ''"
                  @change="layoutStore.setComponentTheme(component.id, $event.target.value || null)"
                  class="min-w-0 max-w-[9rem] border border-border bg-background px-2 py-1.5 text-[11px] outline-none focus:border-maroon"
                >
                  <option value="">همگام با تم کلی</option>
                  <option v-for="theme in componentThemeOptions" :key="theme.key" :value="theme.key">
                    {{ theme.label }}
                  </option>
                </select>
              </label>
            </div>
          </section>

          <!-- Header -->
          <section>
            <div class="mb-4 flex items-center gap-2">
              <Layout class="h-4 w-4 text-maroon" />
              <div>
                <div class="text-xs uppercase tracking-widest text-maroon font-semibold">هدر سایت</div>
                <div class="text-xs text-muted-foreground">طرح نوار ناوبری بالای صفحه</div>
              </div>
            </div>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
              <button v-for="h in HEADER_VARIANTS" :key="h.id" type="button"
                class="border p-3 text-right transition-all" :class="activeClass(layoutStore.headerVariant === h.id)"
                @click="layoutStore.headerVariant = h.id">
                <div class="mb-2 h-8 border border-current/10 bg-muted/50 flex items-center px-2 gap-1">
                  <template v-if="h.id === 1">
                    <div class="h-1.5 w-8 bg-current opacity-40 rounded-sm mr-auto" /><div v-for="i in 3" :key="i" class="h-1.5 w-4 bg-current opacity-20 rounded-sm" />
                  </template>
                  <template v-else-if="h.id === 2">
                    <div class="h-1.5 w-5 bg-current opacity-20 rounded-sm" /><div class="h-1.5 w-8 bg-current opacity-40 rounded-sm mx-auto" /><div class="h-1.5 w-5 bg-current opacity-20 rounded-sm" />
                  </template>
                  <template v-else-if="h.id === 3">
                    <div class="h-4 w-4 bg-maroon/20 rounded-full" /><div class="h-4 w-8 bg-maroon/20 rounded-full" /><div class="h-1.5 w-6 bg-current opacity-40 rounded-sm mr-auto" />
                  </template>
                  <template v-else>
                    <div class="h-3 w-12 bg-current opacity-40 rounded-sm mx-auto" />
                  </template>
                </div>
                <div class="flex items-center justify-between">
                  <div><div class="text-xs font-medium">{{ h.label }}</div><div class="text-[10px] text-muted-foreground mt-0.5">{{ h.desc }}</div></div>
                  <Check v-if="layoutStore.headerVariant === h.id" class="h-3.5 w-3.5 text-maroon shrink-0" />
                </div>
              </button>
            </div>
          </section>

          <!-- Footer -->
          <section>
            <div class="mb-4 flex items-center gap-2">
              <Square class="h-4 w-4 text-maroon" />
              <div>
                <div class="text-xs uppercase tracking-widest text-maroon font-semibold">فوتر سایت</div>
                <div class="text-xs text-muted-foreground">طرح نوار پایین صفحه</div>
              </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
              <button v-for="f in FOOTER_VARIANTS" :key="f.id" type="button"
                class="border p-3 text-right transition-all" :class="activeClass(layoutStore.footerVariant === f.id)"
                @click="layoutStore.footerVariant = f.id">
                <div class="mb-2 h-14 border border-current/10 overflow-hidden" :class="f.id === 3 ? 'bg-gray-800' : 'bg-muted/40'">
                  <template v-if="f.id === 1">
                    <div class="grid grid-cols-4 gap-1 p-1.5 h-full">
                      <div v-for="i in 4" :key="i" class="space-y-1"><div class="h-1.5 w-full bg-current opacity-25 rounded-sm" /><div class="h-1 w-full bg-current opacity-15 rounded-sm" /></div>
                    </div>
                  </template>
                  <template v-else-if="f.id === 2">
                    <div class="flex flex-col items-center justify-center h-full gap-1">
                      <div class="h-2 w-14 bg-current opacity-35 rounded-sm" /><div class="flex gap-1.5"><div v-for="i in 3" :key="i" class="h-1 w-5 bg-current opacity-20 rounded-sm" /></div>
                    </div>
                  </template>
                  <template v-else>
                    <div class="grid grid-cols-3 gap-1 p-1.5 h-full">
                      <div v-for="i in 3" :key="i" class="space-y-1"><div class="h-1.5 w-full bg-white opacity-25 rounded-sm" /><div class="h-1 w-full bg-white opacity-15 rounded-sm" /></div>
                    </div>
                  </template>
                </div>
                <div class="flex items-center justify-between">
                  <div><div class="text-xs font-medium">{{ f.label }}</div><div class="text-[10px] text-muted-foreground mt-0.5">{{ f.desc }}</div></div>
                  <Check v-if="layoutStore.footerVariant === f.id" class="h-3.5 w-3.5 text-maroon shrink-0" />
                </div>
              </button>
            </div>
          </section>

          <!-- Hero -->
          <section>
            <div class="mb-4 flex items-center gap-2">
              <Image class="h-4 w-4 text-maroon" />
              <div>
                <div class="text-xs uppercase tracking-widest text-maroon font-semibold">بنر اصلی</div>
                <div class="text-xs text-muted-foreground">چیدمان Hero در صفحه اصلی</div>
              </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
              <button v-for="hv in HERO_VARIANTS" :key="hv.id" type="button"
                class="border p-3 text-right transition-all" :class="activeClass(layoutStore.heroVariant === hv.id)"
                @click="layoutStore.heroVariant = hv.id">
                <div class="mb-2 h-16 bg-gray-800/10 border border-current/10 overflow-hidden relative">
                  <template v-if="hv.id === 1">
                    <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                    <div class="absolute bottom-2 right-2 space-y-0.5"><div class="h-1.5 w-14 bg-white opacity-50 rounded-sm" /><div class="h-1 w-18 bg-white opacity-30 rounded-sm" /></div>
                  </template>
                  <template v-else-if="hv.id === 2">
                    <div class="grid grid-cols-2 h-full">
                      <div class="bg-muted/60 flex flex-col justify-center p-1.5 gap-1"><div class="h-1.5 w-full bg-current opacity-30 rounded-sm" /><div class="h-2 w-8 bg-maroon/50 rounded-sm mt-0.5" /></div>
                      <div class="bg-gray-400/20" />
                    </div>
                  </template>
                  <template v-else>
                    <div class="absolute inset-0 bg-gradient-to-br from-black/70 to-transparent" />
                    <div class="absolute right-2 top-1/2 -translate-y-1/2 space-y-0.5"><div class="h-1.5 w-12 bg-white opacity-60 rounded-sm" /></div>
                  </template>
                </div>
                <div class="flex items-center justify-between">
                  <div><div class="text-xs font-medium">{{ hv.label }}</div><div class="text-[10px] text-muted-foreground mt-0.5">{{ hv.desc }}</div></div>
                  <Check v-if="layoutStore.heroVariant === hv.id" class="h-3.5 w-3.5 text-maroon shrink-0" />
                </div>
              </button>
            </div>
          </section>

          <!-- Cards -->
          <section>
            <div class="mb-4 flex items-center gap-2">
              <Layers class="h-4 w-4 text-maroon" />
              <div>
                <div class="text-xs uppercase tracking-widest text-maroon font-semibold">کارت محصولات</div>
                <div class="text-xs text-muted-foreground">نمایش در لیست محصولات</div>
              </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
              <button v-for="cv in CARD_VARIANTS" :key="cv.id" type="button"
                class="border p-3 text-right transition-all" :class="activeClass(layoutStore.cardVariant === cv.id)"
                @click="layoutStore.cardVariant = cv.id">
                <div class="mb-2 border border-current/10 overflow-hidden bg-muted/30">
                  <template v-if="cv.id === 'standard'">
                    <div class="aspect-[4/3] bg-gray-300/30 relative"><div class="absolute inset-0 bg-gradient-to-br from-gray-200/40 to-gray-400/20" /></div>
                    <div class="p-2 space-y-1"><div class="h-1.5 w-3/4 bg-current opacity-30 rounded-sm" /><div class="h-2 w-1/3 bg-maroon/50 rounded-sm" /></div>
                  </template>
                  <template v-else-if="cv.id === 'compact'">
                    <div class="aspect-square bg-gray-300/30 relative"><div class="absolute bottom-0 inset-x-0 h-1/3 bg-gradient-to-t from-black/50 to-transparent flex items-end p-1"><div class="h-1.5 w-10 bg-white opacity-60 rounded-sm" /></div></div>
                    <div class="p-1.5 space-y-0.5"><div class="h-1.5 w-3/4 bg-current opacity-30 rounded-sm" /></div>
                  </template>
                  <template v-else>
                    <div class="flex h-14"><div class="w-1/3 bg-gray-300/40 flex-shrink-0" /><div class="flex-1 p-2 flex flex-col justify-between"><div class="h-1.5 w-4/5 bg-current opacity-30 rounded-sm" /><div class="h-1.5 w-1/2 bg-maroon/40 rounded-sm" /></div></div>
                  </template>
                </div>
                <div class="flex items-center justify-between">
                  <div><div class="text-xs font-medium">{{ cv.label }}</div><div class="text-[10px] text-muted-foreground mt-0.5">{{ cv.desc }}</div></div>
                  <Check v-if="layoutStore.cardVariant === cv.id" class="h-3.5 w-3.5 text-maroon shrink-0" />
                </div>
              </button>
            </div>
          </section>

          <!-- Button style -->
          <section>
            <div class="mb-4 flex items-center gap-2">
              <Type class="h-4 w-4 text-maroon" />
              <div>
                <div class="text-xs uppercase tracking-widest text-maroon font-semibold">استایل دکمه</div>
                <div class="text-xs text-muted-foreground">شکل گوشه‌های دکمه‌ها</div>
              </div>
            </div>
            <div class="flex flex-wrap gap-3">
              <button v-for="bs in BUTTON_STYLES" :key="bs.id" type="button"
                class="border px-5 py-3 transition-all" :class="activeClass(layoutStore.buttonStyle === bs.id)"
                @click="layoutStore.buttonStyle = bs.id">
                <div class="mb-2 flex gap-2 items-center justify-center">
                  <div class="h-7 px-4 bg-maroon/20 flex items-center text-[10px] text-maroon font-medium" :style="{ borderRadius: bs.id==='sharp'?'0':bs.id==='rounded'?'5px':'9999px' }">دکمه</div>
                  <div class="h-7 w-12 border border-current/20" :style="{ borderRadius: bs.id==='sharp'?'0':bs.id==='rounded'?'5px':'9999px' }" />
                </div>
                <div class="flex items-center justify-between gap-3">
                  <div><div class="text-xs font-medium">{{ bs.label }}</div><div class="text-[10px] text-muted-foreground mt-0.5">{{ bs.desc }}</div></div>
                  <Check v-if="layoutStore.buttonStyle === bs.id" class="h-3.5 w-3.5 text-maroon shrink-0" />
                </div>
              </button>
            </div>
          </section>

        </div>

        <!-- ══ TAB: PAGES ════════════════════════════════ -->
        <div v-else-if="activeTab === 'pages'" class="p-6 space-y-5">

          <!-- ── Summary bar ── -->
          <div class="flex items-center justify-between border border-border bg-muted/30 px-4 py-3">
            <div>
              <div class="text-xs text-muted-foreground">
                تم کلی سایت:
                <span
                  class="mr-1 inline-flex items-center gap-1.5 font-medium text-foreground"
                >
                  <span
                    class="h-2.5 w-2.5 rounded-full border border-black/10 inline-block"
                    :style="{ background: DESIGN_THEMES[layoutStore.themeName]?.preview?.accent }"
                  />
                  {{ DESIGN_THEMES[layoutStore.themeName]?.label }}
                </span>
              </div>
              <div class="mt-0.5 text-[11px] text-muted-foreground">
                <template v-if="Object.values(layoutStore.pageDesigns).filter(Boolean).length">
                  <span class="text-maroon font-medium">{{ Object.values(layoutStore.pageDesigns).filter(Boolean).length }}</span>
                  صفحه تم اختصاصی دارند
                </template>
                <template v-else>هیچ صفحه‌ای تم اختصاصی ندارد</template>
              </div>
            </div>
            <button
              v-if="Object.values(layoutStore.pageDesigns).filter(Boolean).length"
              type="button"
              @click="clearAllPageOverrides()"
              class="flex items-center gap-1.5 border border-dashed border-border px-3 py-1.5 text-xs text-muted-foreground transition-colors hover:border-red-400 hover:text-red-500"
            >
              <RotateCcw class="h-3 w-3" />
              حذف همه سفارشی‌سازی‌ها
            </button>
          </div>

          <!-- ── Page cards ── -->
          <div class="space-y-3">
            <div
              v-for="page in PAGE_LIST"
              :key="page.path"
              :class="[
                'border transition-colors',
                layoutStore.pageDesigns[page.path] ? 'border-maroon/30 bg-maroon/[0.02]' : 'border-border',
              ]"
            >
              <!-- Card header -->
              <div class="flex items-center justify-between px-4 py-3 border-b border-border/60">
                <div class="flex items-center gap-3">
                  <div>
                    <div class="flex items-center gap-2">
                      <span class="text-sm font-medium">{{ page.label }}</span>
                      <span
                        v-if="layoutStore.pageDesigns[page.path]"
                        class="inline-flex items-center gap-1 rounded-full border border-maroon/30 bg-maroon/5 px-2 py-0.5 text-[10px] text-maroon"
                      >
                        <Lock class="h-2.5 w-2.5" />
                        {{ DESIGN_THEMES[layoutStore.pageDesigns[page.path]]?.label }}
                      </span>
                      <span
                        v-else
                        class="inline-flex items-center gap-1 rounded-full border border-border px-2 py-0.5 text-[10px] text-muted-foreground"
                      >از تم کلی</span>
                    </div>
                    <div class="mt-0.5 font-mono text-[11px] text-muted-foreground">{{ page.path }}</div>
                  </div>
                </div>
                <button
                  type="button"
                  @click="switchPage(page.path)"
                  class="flex items-center gap-1.5 border border-border px-2.5 py-1 text-[10px] text-muted-foreground transition-colors hover:border-maroon hover:text-maroon"
                >
                  <Eye class="h-3 w-3" />
                  پیش‌نمایش
                </button>
              </div>

              <!-- Theme swatches -->
              <div class="px-4 py-3">
                <div class="grid grid-cols-9 gap-1.5">
                  <!-- Default option -->
                  <button
                    type="button"
                    @click="layoutStore.setPageDesign(page.path, null)"
                    :class="[
                      'flex flex-col items-center gap-1 p-1 transition-colors col-span-1',
                      !layoutStore.pageDesigns[page.path]
                        ? 'ring-2 ring-maroon ring-offset-1 ring-offset-background'
                        : 'hover:bg-accent',
                    ]"
                    title="پیش‌فرض (از تم کلی)"
                  >
                    <div class="relative h-8 w-full overflow-hidden border border-border bg-gradient-to-br from-muted to-background">
                      <div class="absolute inset-0 flex items-center justify-center">
                        <span class="text-[8px] text-muted-foreground">پیش‌فرض</span>
                      </div>
                      <div
                        v-if="!layoutStore.pageDesigns[page.path]"
                        class="absolute inset-0 flex items-center justify-center bg-black/10"
                      >
                        <div class="h-1.5 w-1.5 rounded-full bg-maroon" />
                      </div>
                    </div>
                  </button>

                  <!-- Theme swatches -->
                  <button
                    v-for="(theme, key) in DESIGN_THEMES"
                    :key="key"
                    type="button"
                    @click="layoutStore.setPageDesign(page.path, key); switchPage(page.path)"
                    :title="theme.label"
                    :class="[
                      'flex flex-col items-center gap-1 p-1 transition-colors',
                      layoutStore.pageDesigns[page.path] === key
                        ? 'ring-2 ring-maroon ring-offset-1 ring-offset-background'
                        : 'hover:bg-accent',
                    ]"
                  >
                    <div
                      class="relative h-8 w-full overflow-hidden border border-border"
                      :style="{ background: theme.preview.bg }"
                    >
                      <div
                        class="absolute bottom-0 left-0 right-0 h-2"
                        :style="{ background: theme.preview.accent }"
                      />
                      <div
                        class="absolute right-0.5 top-1 h-1 w-3 opacity-60"
                        :style="{ background: theme.preview.text }"
                      />
                      <div
                        v-if="layoutStore.pageDesigns[page.path] === key"
                        class="absolute inset-0 flex items-center justify-center bg-black/10"
                      >
                        <div class="flex h-3.5 w-3.5 items-center justify-center rounded-full bg-white/80">
                          <div class="h-1 w-1 rounded-full bg-maroon" />
                        </div>
                      </div>
                    </div>
                    <span class="text-[8px] leading-tight text-muted-foreground truncate w-full text-center">{{ theme.label }}</span>
                  </button>
                </div>
              </div>

              <!-- Per-page component overrides -->
              <div class="border-t border-border/60 px-4 py-3">
                <button
                  type="button"
                  @click="togglePageComponents(page.path)"
                  class="flex w-full items-center justify-between text-right text-xs text-muted-foreground transition-colors hover:text-maroon"
                >
                  <span class="flex items-center gap-2">
                    <Layers class="h-3.5 w-3.5" />
                    سفارشی‌سازی کامپوننت‌های این صفحه
                    <span v-if="layoutStore.pageComponentThemes[page.path] && Object.keys(layoutStore.pageComponentThemes[page.path]).length" class="rounded-full bg-maroon/10 px-1.5 py-0.5 text-[9px] text-maroon">
                      {{ Object.keys(layoutStore.pageComponentThemes[page.path]).length }}
                    </span>
                  </span>
                  <span class="text-[10px]">{{ pageComponentOpen[page.path] ? 'بستن' : 'باز کردن' }}</span>
                </button>

                <div v-if="pageComponentOpen[page.path]" class="mt-3 space-y-2 border-t border-border/60 pt-3">
                  <div class="flex items-center justify-between gap-3">
                    <p class="text-[10px] leading-5 text-muted-foreground">این تنظیمات فقط روی همین صفحه اعمال می‌شوند و بر تم کلی سایت اثری ندارند.</p>
                    <button
                      type="button"
                      @click="layoutStore.clearComponentThemes(page.path)"
                      class="shrink-0 text-[10px] text-muted-foreground underline underline-offset-2 hover:text-red-500"
                    >پاک‌سازی</button>
                  </div>
                  <label v-for="component in DESIGN_COMPONENTS" :key="component.id" class="flex items-center justify-between gap-3 border border-border bg-background px-3 py-2">
                    <span class="text-[11px]">{{ component.label }}</span>
                    <select
                      :value="pageComponentTheme(page.path, component.id)"
                      @change="setPageComponentTheme(page.path, component.id, $event.target.value)"
                      class="max-w-[9rem] border border-border bg-background px-2 py-1 text-[10px] outline-none focus:border-maroon"
                    >
                      <option value="">از تم صفحه</option>
                      <option v-for="theme in componentThemeOptions" :key="theme.key" :value="theme.key">{{ theme.label }}</option>
                    </select>
                  </label>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- ═══ RIGHT PANEL — Live Preview ══════════════════ -->
    <div class="hidden lg:flex flex-col w-[520px] shrink-0 border-r border-border bg-muted/30 h-screen">
      <div class="flex items-center justify-between gap-2 border-b border-border px-4 py-2.5 bg-background shrink-0">
        <div class="flex items-center gap-1">
          <span class="text-xs text-muted-foreground ml-2">صفحه:</span>
          <button v-for="pg in PREVIEW_PAGES" :key="pg.path" type="button" @click="switchPage(pg.path)"
            :class="['px-2.5 py-1 text-xs transition-colors rounded-sm', previewPage === pg.path ? 'bg-foreground text-background' : 'hover:bg-accent text-muted-foreground']">{{ pg.label }}</button>
        </div>
        <div class="flex items-center gap-1 shrink-0">
          <button type="button" @click="previewDevice='desktop'" :class="['p-1.5 rounded-sm', previewDevice==='desktop'?'bg-foreground text-background':'hover:bg-accent text-muted-foreground']"><Monitor class="h-3.5 w-3.5" /></button>
          <button type="button" @click="previewDevice='mobile'" :class="['p-1.5 rounded-sm', previewDevice==='mobile'?'bg-foreground text-background':'hover:bg-accent text-muted-foreground']"><Smartphone class="h-3.5 w-3.5" /></button>
          <button type="button" @click="reloadPreview" class="p-1.5 rounded-sm hover:bg-accent text-muted-foreground"><RefreshCw class="h-3.5 w-3.5" /></button>
        </div>
      </div>

      <!-- Scrollable preview area -->
      <div class="flex-1 overflow-y-auto flex items-start justify-center py-4 px-3">

        <!-- Desktop -->
        <div v-if="previewDevice === 'desktop'" class="w-full">
          <div class="border border-border rounded-t-sm bg-muted shadow-lg">
            <!-- Browser chrome -->
            <div class="flex items-center gap-1.5 px-3 py-2 border-b border-border bg-background sticky top-0 z-10">
              <span class="h-2.5 w-2.5 rounded-full bg-red-400/70" /><span class="h-2.5 w-2.5 rounded-full bg-yellow-400/70" /><span class="h-2.5 w-2.5 rounded-full bg-green-400/70" />
              <div class="mr-2 flex-1 rounded bg-muted px-3 py-0.5 text-[10px] text-muted-foreground text-center truncate">{{ previewPage === '/' ? 'نوار — فروشگاه قهوه' : previewPage }}</div>
            </div>
            <!-- Scaled iframe container — height matches scaled IFRAME_H -->
            <div class="relative" :style="{ height: `${Math.round(IFRAME_H * desktopScale)}px` }">
              <div :style="{ width:`${IFRAME_W}px`, height:`${IFRAME_H}px`, transform:`scale(${desktopScale})`, transformOrigin:'top right', position:'absolute', top:0, right:0, pointerEvents:'none' }">
                <iframe
                  :key="iframeKey" ref="iframeRef" :src="previewPage"
                  @load="onIframeLoad"
                  class="border-0"
                  :style="{ width:`${IFRAME_W}px`, height:`${IFRAME_H}px`, display:'block' }"
                  sandbox="allow-scripts allow-same-origin"
                />
              </div>
              <Transition name="fade">
                <div v-if="!previewReady" class="absolute inset-0 flex items-center justify-center bg-muted/80 backdrop-blur-sm z-10">
                  <div class="flex flex-col items-center gap-2 text-muted-foreground"><RefreshCw class="h-5 w-5 animate-spin" /><span class="text-xs">در حال بارگذاری...</span></div>
                </div>
              </Transition>
            </div>
          </div>
        </div>

        <!-- Mobile -->
        <div v-else class="flex justify-center w-full">
          <div
            class="relative rounded-[1.8rem] border-[7px] border-foreground/80 bg-foreground/80 shadow-2xl overflow-hidden"
            :style="{ width:`${Math.round(MOB_W*mobileScale)}px`, height:`${Math.round(MOB_H*mobileScale)}px` }"
          >
            <div class="absolute top-0 left-1/2 -translate-x-1/2 z-20 h-3.5 w-14 rounded-b-xl bg-foreground/80" />
            <div class="relative rounded-[1.3rem] bg-background w-full h-full overflow-hidden">
              <div :style="{ width:`${MOB_W}px`, height:`${MOB_H}px`, transform:`scale(${mobileScale})`, transformOrigin:'top right', position:'absolute', top:0, right:0, pointerEvents:'none' }">
                <iframe
                  :key="iframeKey+'m'" ref="mobileIframeRef" :src="previewPage"
                  @load="onIframeLoad"
                  class="border-0"
                  :style="{ width:`${MOB_W}px`, height:`${MOB_H}px`, display:'block' }"
                  sandbox="allow-scripts allow-same-origin"
                />
              </div>
              <Transition name="fade">
                <div v-if="!previewReady" class="absolute inset-0 flex items-center justify-center bg-muted/80 backdrop-blur-sm z-10"><RefreshCw class="h-4 w-4 animate-spin text-muted-foreground" /></div>
              </Transition>
            </div>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
