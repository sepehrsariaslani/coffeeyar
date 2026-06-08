import { defineStore } from "pinia";
import { ref, watch } from "vue";
import { api } from "@/lib/api";

const STORAGE_KEY = "navar_theme_v1";

const ALL_THEME_CLASSES = ["dark", "theme-modern", "theme-earthy", "theme-glass"];

const defaults = {
  accentHue: 22,
  accentChroma: 0.09,
  accentLightness: 0.42,
  bgLightness: 0.982,
  bgChroma: 0.006,
  bgHue: 75,
  themeClass: "",
};

function loadTheme() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return { ...defaults, ...JSON.parse(raw) };
  } catch {}
  return { ...defaults };
}

export function applyTheme(t) {
  const root = document.documentElement;

  root.classList.remove(...ALL_THEME_CLASSES);
  if (t.themeClass) root.classList.add(t.themeClass);

  if (t.themeClass === "theme-glass" || t.themeClass === "theme-modern" || t.themeClass === "theme-earthy" || t.themeClass === "dark") {
    root.style.removeProperty("--maroon");
    root.style.removeProperty("--background");
    root.style.removeProperty("--card");
    root.style.removeProperty("--popover");
    root.style.removeProperty("--sidebar");
    root.style.removeProperty("--muted");
    root.style.removeProperty("--secondary");
    root.style.removeProperty("--accent");
    root.style.removeProperty("--sidebar-accent");
    root.style.removeProperty("--border");
    root.style.removeProperty("--sidebar-border");
    root.style.removeProperty("--input");
    return;
  }

  const maroon = `oklch(${t.accentLightness} ${t.accentChroma} ${t.accentHue})`;
  const bg     = `oklch(${t.bgLightness} ${t.bgChroma} ${t.bgHue})`;
  const sidebar  = `oklch(${Math.min(t.bgLightness + 0.01, 1)} ${t.bgChroma} ${t.bgHue})`;
  const muted    = `oklch(${t.bgLightness - 0.02} ${t.bgChroma} ${t.bgHue})`;
  const accent   = `oklch(${t.bgLightness - 0.04} ${t.bgChroma} ${t.bgHue})`;
  const border   = `oklch(${t.bgLightness - 0.1} ${t.bgChroma * 0.5} ${t.bgHue})`;

  root.style.setProperty("--maroon",         maroon);
  root.style.setProperty("--background",     bg);
  root.style.setProperty("--card",           bg);
  root.style.setProperty("--popover",        bg);
  root.style.setProperty("--sidebar",        sidebar);
  root.style.setProperty("--muted",          muted);
  root.style.setProperty("--secondary",      muted);
  root.style.setProperty("--accent",         accent);
  root.style.setProperty("--sidebar-accent", accent);
  root.style.setProperty("--border",         border);
  root.style.setProperty("--sidebar-border", border);
  root.style.setProperty("--input",          border);
}

if (typeof window !== "undefined") {
  window.addEventListener("message", (e) => {
    if (e.data && e.data.type === "navar-theme-preview") {
      applyTheme(e.data.theme);
    }
  });
}

export const useThemeStore = defineStore("theme", () => {
  const theme = ref(loadTheme());

  applyTheme(theme.value);

  async function fetchTheme() {
    try {
      const data = await api.admin.theme.get();
      if (data && data.theme) {
        const merged = { ...defaults, ...data.theme };
        theme.value = merged;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(merged));
      }
    } catch {
      // use cached
    }
  }

  async function saveToServer() {
    try {
      await api.admin.theme.update({ theme: theme.value });
    } catch {
      // silent
    }
  }

  watch(
    theme,
    (val) => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(val));
      applyTheme(val);
      saveToServer();
    },
    { deep: true }
  );

  function reset() {
    theme.value = { ...defaults };
  }

  function setThemeClass(cls) {
    theme.value.themeClass = cls;
  }

  fetchTheme();

  return { theme, reset, defaults, setThemeClass };
});
