import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/lib/api.js";
import { isDemoMode } from "@/lib/demo.js";
import { copyDemo, DEMO_SITE_SETTINGS } from "@/data/demoData.js";

export const useSiteSettingsStore = defineStore("siteSettings", () => {
  const settings = ref(copyDemo(DEMO_SITE_SETTINGS));
  const loaded = ref(false);

  function normalizeSettings(value) {
    if (!value || typeof value !== "object") return copyDemo(DEMO_SITE_SETTINGS);
    return {
      ...value,
      shopName: value.shopName || value.shop_name || DEMO_SITE_SETTINGS.shopName,
    };
  }

  async function fetchSettings() {
    if (loaded.value) return;
    try {
      const s = isDemoMode ? copyDemo(DEMO_SITE_SETTINGS) : await api.site.settings();
      settings.value = normalizeSettings(s);
      loaded.value = true;
    } catch (e) {
      console.error("خطا در دریافت تنظیمات:", e.message);
      settings.value = copyDemo(DEMO_SITE_SETTINGS);
      loaded.value = true;
    }
  }

  async function save(patch) {
    try {
      const flat = {};
      if (patch.shop_name !== undefined) flat.shop_name = patch.shop_name;
      if (patch.description !== undefined) flat.description = patch.description;
      if (patch.phone !== undefined) flat.phone = patch.phone;
      if (patch.email !== undefined) flat.email = patch.email;
      if (patch.address !== undefined) flat.address = patch.address;
      if (patch.instagram !== undefined) flat.instagram = patch.instagram;
      if (patch.telegram !== undefined) flat.telegram = patch.telegram;
      if (patch.enamad_code !== undefined) flat.enamad_code = patch.enamad_code;
      if (patch.shipping?.standard?.price !== undefined)
        flat.shipping_standard_price = patch.shipping.standard.price;
      if (patch.shipping?.standard?.free_threshold !== undefined)
        flat.shipping_standard_free_threshold = patch.shipping.standard.free_threshold;
      if (patch.shipping?.express?.price !== undefined)
        flat.shipping_express_price = patch.shipping.express.price;
      await api.admin.settings.update(flat);
      settings.value = { ...settings.value, ...patch };
    } catch (e) {
      console.error(e.message);
    }
  }

  // Auto-fetch on store creation
  fetchSettings();

  return { settings, loaded, fetchSettings, save };
});
