import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/lib/api.js";

export const useCouponsStore = defineStore("coupons", () => {
  const coupons = ref([]);
  const loaded = ref(false);

  async function fetchCoupons() {
    try {
      coupons.value = await api.admin.coupons.list();
      loaded.value = true;
    } catch (e) {
      console.error(e.message);
    }
  }

  async function add(coupon) {
    try {
      await api.admin.coupons.create({ ...coupon, code: coupon.code.toUpperCase() });
      await fetchCoupons();
    } catch (e) {
      console.error(e.message);
    }
  }

  async function remove(id) {
    try {
      await api.admin.coupons.remove(id);
      coupons.value = coupons.value.filter((c) => c.id !== id);
    } catch (e) {
      console.error(e.message);
    }
  }

  async function toggle(id) {
    try {
      const res = await api.admin.coupons.toggle(id);
      const c = coupons.value.find((c) => c.id === id);
      if (c) c.is_active = res.is_active;
    } catch (e) {
      console.error(e.message);
    }
  }

  async function validate(code, orderTotal) {
    try {
      const res = await api.coupons.validate(code, orderTotal);
      return { ok: true, coupon: res, discount: res.discount };
    } catch (e) {
      return { ok: false, error: e.message };
    }
  }

  async function use(code) {
    const c = coupons.value.find((c) => c.code === code.trim().toUpperCase());
    if (c) c.used_count = (c.used_count || 0) + 1;
  }

  return { coupons, loaded, fetchCoupons, add, remove, toggle, validate, use };
});
