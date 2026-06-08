import { defineStore } from "pinia";
import { ref } from "vue";

export const useSiteSettingsStore = defineStore("siteSettings", () => {
  const settings = ref({
    shopName: "نوار",
    description: "قهوه‌ی تخصصی، تازه برشته شده. ما به سادگی، شفافیت و فنجانی بی‌نقص باور داریم.",
    phone: "",
    email: "",
    address: "",
    instagram: "#",
    telegram: "#",
    enamadCode: "",
    zarinpalMerchantId: "",
    zarinpalEnabled: false,
    zarinpalSandbox: true,
    paymentMethods: {
      online: true,
      cod: true,
      wallet: true,
    },
    shipping: {
      standard: {
        enabled: true,
        label: "ارسال عادی",
        days: "۲ تا ۴ روز کاری",
        price: 45000,
        freeThreshold: 500000,
      },
      express: {
        enabled: true,
        label: "ارسال اکسپرس",
        days: "۲۴ ساعته",
        price: 90000,
        freeThreshold: 0,
      },
    },
  });

  function load() {
    try {
      const saved = localStorage.getItem("siteSettings");
      if (saved) {
        const parsed = JSON.parse(saved);
        settings.value = {
          ...settings.value,
          ...parsed,
          paymentMethods: { ...settings.value.paymentMethods, ...(parsed.paymentMethods || {}) },
          shipping: {
            standard: { ...settings.value.shipping.standard, ...(parsed.shipping?.standard || {}) },
            express: { ...settings.value.shipping.express, ...(parsed.shipping?.express || {}) },
          },
        };
      }
    } catch {}
  }

  function save() {
    localStorage.setItem("siteSettings", JSON.stringify(settings.value));
  }

  load();

  return { settings, save };
});
