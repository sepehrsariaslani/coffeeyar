import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/lib/api";

export const useNavigationStore = defineStore("navigation", () => {
  const headerLinks = ref([]);
  const footerLinks = ref([]);
  const mobileLinks = ref([]);
  const loaded = ref(false);

  async function fetchNavigation() {
    if (loaded.value) return;
    try {
      const data = await api.site.navigation();
      if (data && typeof data === "object") {
        headerLinks.value = data.header || [];
        footerLinks.value = data.footer || [];
        mobileLinks.value = data.mobile || [];
        loaded.value = true;
      }
    } catch (e) {
      console.error("خطا در دریافت ناوبری:", e.message);
    }
  }

  // Auto-fetch on store creation
  fetchNavigation();

  return { headerLinks, footerLinks, mobileLinks, loaded, fetchNavigation };
});
