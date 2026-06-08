import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { api } from "@/lib/api.js";
import { useAuthStore } from "./auth.js";
import { useNotificationsStore } from "./notifications.js";

/**
 * Returns store — backed by the Frappe `Return Request` doctype.
 * Customers create requests; admins list and update their status.
 */
export const useReturnsStore = defineStore("returns", () => {
  const requests = ref([]);

  const pending = computed(() => requests.value.filter((r) => r.status === "در انتظار بررسی"));
  const approved = computed(() => requests.value.filter((r) => r.status === "تایید شده"));

  /**
   * Fetch the current user's return requests from the server.
   * @returns {Promise<void>}
   */
  async function fetchReturns() {
    const auth = useAuthStore();
    if (!auth.isLoggedIn) return;
    try {
      requests.value = (await api.returns.list()) || [];
    } catch (e) {
      console.error("خطا در دریافت مرجوعی‌ها:", e.message);
    }
  }

  /**
   * Fetch ALL return requests (admin view) from the server.
   * @returns {Promise<void>}
   */
  async function fetchAdminReturns() {
    try {
      requests.value = (await api.admin.returns.list()) || [];
    } catch (e) {
      console.error("خطا در دریافت مرجوعی‌ها:", e.message);
    }
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

  /**
   * Update a return request's status (admin). Persists to the server.
   * @param {string} id Return request id.
   * @param {string} status New status.
   * @param {string} [adminNote] Optional admin note.
   * @returns {Promise<void>}
   */
  async function updateStatus(id, status, adminNote = "") {
    const req = requests.value.find((r) => r.id === id);
    if (req) { req.status = status; req.adminNote = adminNote; }
    try {
      await api.admin.returns.updateStatus(id, { status, admin_note: adminNote });
    } catch (e) {
      console.error("خطا در به‌روزرسانی مرجوعی:", e.message);
    }
  }

  function remove(id) {
    requests.value = requests.value.filter((r) => r.id !== id);
  }

  return { requests, pending, approved, submit, updateStatus, remove, fetchReturns, fetchAdminReturns };
});
