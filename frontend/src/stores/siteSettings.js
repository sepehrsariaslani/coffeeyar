import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/lib/api.js";

const defaultSettings = {
  shop_name: "نوار",
  description: "قهوه‌ی تخصصی، تازه برشته شده.",
  phone: "",
  email: "",
  address: "",
  instagram: "#",
  telegram: "#",
  enamad_code: "",
  payment_online: true,
  payment_cod: true,
  shipping: {
    standard: { enabled: true, label: "ارسال عادی", days: "۲ تا ۴ روز کاری", price: 45000, free_threshold: 500000 },
    express: { enabled: true, label: "ارسال اکسپرس", days: "۲۴ ساعته", price: 90000, free_threshold: 0 },
  },
};

export const useSiteSettingsStore = defineStore("siteSettings", () => {
  const settings = ref({ ...defaultSettings });
  const loaded = ref(false);

  async function fetchSettings() {
    if (loaded.value) return;
    try {
      const s = await api.site.settings();
      settings.value = { ...defaultSettings, ...s };
      loaded.value = true;
    } catch (e) {
      console.error("خطا در دریافت تنظیمات:", e.message);
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

  fetchSettings();

  return { settings, loaded, fetchSettings, save };
});
