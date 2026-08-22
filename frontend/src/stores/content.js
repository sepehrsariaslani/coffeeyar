import { defineStore } from "pinia";
import { ref, watch } from "vue";
import { api } from "@/lib/api";
import { isDemoMode } from "@/lib/demo.js";
import { copyDemo, DEMO_CONTENT } from "@/data/demoData.js";

const STORAGE_KEY = "navar_content_v1";

function loadFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export const useContentStore = defineStore("content", () => {
  // Keep a complete first paint for the standalone sandbox preview. A live
  // Frappe site can still replace this with the content returned by the API.
  const content = ref(isDemoMode ? copyDemo(DEMO_CONTENT) : loadFromStorage() || copyDemo(DEMO_CONTENT));
  const loading = ref(false);
  const loaded = ref(false);

  async function fetchContent() {
    if (loaded.value) return;
    loading.value = true;
    try {
      const data = isDemoMode ? copyDemo(DEMO_CONTENT) : await api.content.get();
      if (data && typeof data === "object") {
        content.value = data;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        loaded.value = true;
      }
    } catch {
      // Fallback to the cached content, then to the local preview content.
      content.value = loadFromStorage() || copyDemo(DEMO_CONTENT);
      loaded.value = true;
    } finally {
      loading.value = false;
    }
  }

  async function saveToServer() {
    if (isDemoMode || !content.value) return;
    try {
      await api.admin.content.update({
        home: content.value.home,
        about: content.value.about,
        contact: content.value.contact,
      });
    } catch {
      // silent
    }
  }

  watch(
    content,
    (val) => {
      if (!val) return;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(val));
      saveToServer();
    },
    { deep: true }
  );

  function update(path, value) {
    if (!content.value) return;
    const keys = path.split(".");
    let obj = content.value;
    for (let i = 0; i < keys.length - 1; i++) {
      obj = obj[keys[i]];
    }
    obj[keys[keys.length - 1]] = value;
  }

  function reset() {
    content.value = null;
    localStorage.removeItem(STORAGE_KEY);
    fetchContent();
  }

  // Auto-fetch on store creation
  fetchContent();

  return { content, loading, loaded, update, reset, fetchContent };
});
