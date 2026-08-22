import { defineStore } from "pinia";
import { ref, watch } from "vue";
import { api } from "@/lib/api";
import { isDemoMode } from "@/lib/demo.js";

const STORAGE_KEY = "navar_theme_v1";

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

  // This store owns the color tokens only. Design classes are controlled by
  // layoutStore, so changing a palette must never remove the active design
  // theme or a component override.
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
    if (isDemoMode) return;
    try {
      // Public endpoint — no auth needed, works for all visitors
      const data = await api.theme.get();
      if (data && data.theme && Object.keys(data.theme).length) {
        const merged = { ...defaults, ...data.theme };
        theme.value = merged;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(merged));
        applyTheme(merged);
      }
    } catch {
      // use cached localStorage value (already applied on load)
    }
  }

  async function saveToServer() {
    if (isDemoMode) return;
    try {
      // Admin-only write endpoint
      await api.admin.theme.update({ theme: theme.value });
    } catch {
      // silent — non-admins can't save but local changes still apply
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
