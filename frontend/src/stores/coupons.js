import { defineStore } from "pinia";
import { ref } from "vue";

export const useCouponsStore = defineStore("coupons", () => {
  const coupons = ref(
    JSON.parse(localStorage.getItem("navar_coupons_v1") || "null") || [
      { code: "NAVAR10", type: "percent", value: 10, label: "۱۰٪ تخفیف", minOrder: 0, maxUses: 100, used: 3, active: true, expiry: "" },
      { code: "NAVAR20", type: "percent", value: 20, label: "۲۰٪ تخفیف", minOrder: 500000, maxUses: 50, used: 1, active: true, expiry: "" },
      { code: "WELCOME", type: "percent", value: 15, label: "۱۵٪ تخفیف خوش‌آمدگویی", minOrder: 0, maxUses: 200, used: 12, active: true, expiry: "" },
    ]
  );

  function _save() {
    localStorage.setItem("navar_coupons_v1", JSON.stringify(coupons.value));
  }

  function add(coupon) {
    coupons.value.push({ ...coupon, code: coupon.code.toUpperCase(), used: 0 });
    _save();
  }

  function remove(code) {
    const idx = coupons.value.findIndex((c) => c.code === code);
    if (idx !== -1) coupons.value.splice(idx, 1);
    _save();
  }

  function toggle(code) {
    const c = coupons.value.find((c) => c.code === code);
    if (c) { c.active = !c.active; _save(); }
  }

  function validate(code, orderTotal) {
    const c = coupons.value.find((c) => c.code === code.trim().toUpperCase());
    if (!c) return { ok: false, error: "کد تخفیف نامعتبر است" };
    if (!c.active) return { ok: false, error: "این کد تخفیف غیرفعال است" };
    if (c.minOrder && orderTotal < c.minOrder)
      return { ok: false, error: `حداقل خرید برای این کد ${c.minOrder.toLocaleString("fa-IR")} تومان است` };
    if (c.maxUses && c.used >= c.maxUses)
      return { ok: false, error: "ظرفیت استفاده از این کد تمام شده است" };
    if (c.expiry && new Date(c.expiry) < new Date())
      return { ok: false, error: "این کد تخفیف منقضی شده است" };
    return { ok: true, coupon: c };
  }

  function use(code) {
    const c = coupons.value.find((c) => c.code === code.trim().toUpperCase());
    if (c) { c.used++; _save(); }
  }

  return { coupons, add, remove, toggle, validate, use };
});
