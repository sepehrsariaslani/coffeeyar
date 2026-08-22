import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/lib/api";
import { isDemoMode } from "@/lib/demo.js";
import { copyDemo, DEMO_POLICIES } from "@/data/demoData.js";

const KEY = "navar-policies-v1";

export const usePoliciesStore = defineStore("policies", () => {
  const policies = ref(copyDemo(DEMO_POLICIES));
  const loaded = ref(false);

  async function fetchPolicies() {
    if (loaded.value) return;
    try {
      const data = isDemoMode ? copyDemo(DEMO_POLICIES) : await api.policies.get();
      if (data && typeof data === "object") {
        policies.value = data;
        localStorage.setItem(KEY, JSON.stringify(data));
      }
      loaded.value = true;
    } catch {
      // Fallback to localStorage cache, then to local preview content.
      try {
        const saved = localStorage.getItem(KEY);
        policies.value = saved ? JSON.parse(saved) : copyDemo(DEMO_POLICIES);
      } catch {
        policies.value = copyDemo(DEMO_POLICIES);
      }
      loaded.value = true;
    }
  }

  async function saveToServer() {
    if (isDemoMode || !policies.value) return;
    try {
      await api.admin.policies.update(policies.value);
    } catch {
      // silent
    }
  }

  function save() {
    if (!policies.value) return;
    localStorage.setItem(KEY, JSON.stringify(policies.value));
    saveToServer();
  }

  // Auto-fetch on store creation
  fetchPolicies();

  return { policies, loaded, save, fetchPolicies };
});
