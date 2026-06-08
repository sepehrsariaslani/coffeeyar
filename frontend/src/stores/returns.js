import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { api } from "@/lib/api.js";
import { useAuthStore } from "./auth.js";
import { useNotificationsStore } from "./notifications.js";

const LOCAL_KEY = "navar_returns_v1";
function loadLocal() {
  try { const r = localStorage.getItem(LOCAL_KEY); return r ? JSON.parse(r) : []; } catch { return []; }
}
function saveLocal(v) { localStorage.setItem(LOCAL_KEY, JSON.stringify(v)); }

export const useReturnsStore = defineStore("returns", () => {
  const requests = ref(loadLocal());

  const pending = computed(() => requests.value.filter((r) => r.status === "در انتظار بررسی"));
  const approved = computed(() => requests.value.filter((r) => r.status === "تایید شده"));

  async function fetchReturns() {
    const auth = useAuthStore();
    if (!auth.isLoggedIn) return;
    try {
      const res = await api.returns.list();
      requests.value = res;
      saveLocal(requests.value);
    } catch {}
  }

  async function submit({ orderId, orderRef, reason, description, items, totalAmount }) {
    const auth = useAuthStore();
    let req;
    try {
      if (auth.isLoggedIn) {
        const res = await api.returns.create({
          order_id: orderId || null,
          order_ref: orderRef || "",
          reason,
          description,
          items: items || [],
          total_amount: totalAmount || 0,
        });
        req = { id: res.id, orderId, orderRef, reason, description, items, totalAmount, status: "در انتظار بررسی", adminNote: "", created_at: res.created_at };
      } else {
        req = {
          id: "RET-" + Date.now(), orderId, orderRef, reason, description,
          items, totalAmount, status: "در انتظار بررسی",
          date: new Date().toLocaleDateString("fa-IR"),
          time: new Date().toLocaleTimeString("fa-IR"),
          adminNote: "",
        };
      }
      requests.value.unshift(req);
      saveLocal(requests.value);
      try {
        const notif = useNotificationsStore();
        notif.add("درخواست مرجوعی ثبت شد", `درخواست مرجوعی برای سفارش ${orderRef} ثبت شد.`, "return");
      } catch {}
      return req;
    } catch (e) {
      console.error(e.message);
      return null;
    }
  }

  function updateStatus(id, status, adminNote = "") {
    const req = requests.value.find((r) => r.id === id);
    if (!req) return;
    req.status = status;
    req.adminNote = adminNote;
    saveLocal(requests.value);
  }

  function remove(id) {
    requests.value = requests.value.filter((r) => r.id !== id);
    saveLocal(requests.value);
  }

  return { requests, pending, approved, submit, updateStatus, remove, fetchReturns };
});
