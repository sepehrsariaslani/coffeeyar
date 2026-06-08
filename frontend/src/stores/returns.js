import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useNotificationsStore } from "./notifications.js";
import { useWalletStore } from "./wallet.js";

const KEY = "navar_returns_v1";

function load() {
  try { const r = localStorage.getItem(KEY); return r ? JSON.parse(r) : []; } catch { return []; }
}
function save(v) { localStorage.setItem(KEY, JSON.stringify(v)); }

export const useReturnsStore = defineStore("returns", () => {
  const requests = ref(load());

  const pending = computed(() => requests.value.filter((r) => r.status === "در انتظار بررسی"));
  const approved = computed(() => requests.value.filter((r) => r.status === "تایید شده"));

  function submit({ orderId, orderRef, reason, description, items, totalAmount }) {
    const req = {
      id: "RET-" + Date.now(),
      orderId,
      orderRef,
      reason,
      description,
      items,
      totalAmount,
      status: "در انتظار بررسی",
      date: new Date().toLocaleDateString("fa-IR"),
      time: new Date().toLocaleTimeString("fa-IR"),
      adminNote: "",
    };
    requests.value.unshift(req);
    save(requests.value);
    try {
      const notif = useNotificationsStore();
      notif.add("درخواست مرجوعی ثبت شد", `درخواست مرجوعی برای سفارش ${orderRef} ثبت شد و در حال بررسی است.`, "return");
    } catch {}
    return req;
  }

  function updateStatus(id, status, adminNote = "") {
    const req = requests.value.find((r) => r.id === id);
    if (!req) return;
    req.status = status;
    req.adminNote = adminNote;
    save(requests.value);

    if (status === "تایید شده") {
      try {
        const wallet = useWalletStore();
        wallet.refund(req.totalAmount, `بازگشت وجه سفارش ${req.orderRef}`);
      } catch {}
    }

    try {
      const notif = useNotificationsStore();
      const msg = status === "تایید شده"
        ? `درخواست مرجوعی ${id} تایید شد و وجه به کیف پول شما بازگشت داده شد.`
        : `وضعیت درخواست مرجوعی ${id} به «${status}» تغییر کرد.`;
      notif.add(`مرجوعی ${status}`, msg, status === "تایید شده" ? "success" : "info");
    } catch {}
  }

  function remove(id) {
    requests.value = requests.value.filter((r) => r.id !== id);
    save(requests.value);
  }

  return { requests, pending, approved, submit, updateStatus, remove };
});
