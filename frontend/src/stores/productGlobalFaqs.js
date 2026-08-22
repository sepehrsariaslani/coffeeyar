import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/lib/api";
import { isDemoMode } from "@/lib/demo.js";
import { copyDemo, DEMO_GLOBAL_FAQS } from "@/data/demoData.js";

export const useProductGlobalFaqsStore = defineStore("productGlobalFaqs", () => {
  const faqs = ref([]);
  const loaded = ref(false);

  async function fetchFaqs() {
    if (loaded.value) return;
    try {
      const data = isDemoMode ? copyDemo(DEMO_GLOBAL_FAQS) : await api.productGlobalFaqs.get();
      if (Array.isArray(data) && data.length > 0) {
        faqs.value = data;
        localStorage.setItem("productGlobalFaqs", JSON.stringify(data));
      }
    } catch {
      // Fallback to localStorage cache, then to the local preview content.
      try {
        const saved = localStorage.getItem("productGlobalFaqs");
        faqs.value = saved ? JSON.parse(saved) : copyDemo(DEMO_GLOBAL_FAQS);
      } catch {
        faqs.value = copyDemo(DEMO_GLOBAL_FAQS);
      }
    }
    loaded.value = true;
  }

  async function saveToServer() {
    if (isDemoMode) return;
    try {
      await api.admin.productFaqs.update(faqs.value);
    } catch {
      // silent
    }
  }

  function save() {
    localStorage.setItem("productGlobalFaqs", JSON.stringify(faqs.value));
    saveToServer();
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

  // Auto-fetch on store creation
  fetchFaqs();

  return { faqs, loaded, save, add, remove, moveUp, moveDown, getFaqsForType };
});
