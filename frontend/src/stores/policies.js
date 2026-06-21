import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/lib/api";

const KEY = "navar-policies-v1";

export const usePoliciesStore = defineStore("policies", () => {
  const policies = ref(null);
  const loaded = ref(false);

  async function fetchPolicies() {
    if (loaded.value) return;
    try {
      const data = await api.policies.get();
      if (data && typeof data === "object") {
        policies.value = data;
        localStorage.setItem(KEY, JSON.stringify(data));
        loaded.value = true;
      }
    } catch {
      // Fallback to localStorage cache
      try {
        const saved = localStorage.getItem(KEY);
        if (saved) {
          policies.value = JSON.parse(saved);
        }
      } catch {
        // silent
      }
    }
    loaded.value = true;
  }

  async function saveToServer() {
    if (!policies.value) return;
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
