import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/lib/api.js";
import { useAuthStore } from "./auth.js";

const LOCAL_KEY = "navar_orders_v1";
function loadLocal() {
  try { return JSON.parse(localStorage.getItem(LOCAL_KEY)) || []; } catch { return []; }
}
function saveLocal(v) { localStorage.setItem(LOCAL_KEY, JSON.stringify(v)); }

export const useOrdersStore = defineStore("orders", () => {
  const orders = ref(loadLocal());
  const currentOrder = ref(null);
  const loading = ref(false);

  async function createOrder(data) {
    loading.value = true;
    try {
      const order = await api.orders.create(data);
      orders.value.unshift(order);
      saveLocal(orders.value);
      currentOrder.value = order;
      return { ok: true, order };
    } catch (e) {
      return { ok: false, error: e.message };
    } finally {
      loading.value = false;
    }
  }

  async function fetchOrders() {
    const auth = useAuthStore();
    if (!auth.isLoggedIn) return;
    loading.value = true;
    try {
      orders.value = await api.orders.list();
      saveLocal(orders.value);
    } catch (e) {
      console.error(e.message);
    } finally {
      loading.value = false;
    }
  }

  async function fetchOrder(ref) {
    try {
      currentOrder.value = await api.orders.get(ref);
      return currentOrder.value;
    } catch (e) {
      console.error(e.message);
      return null;
    }
  }

  return { orders, currentOrder, loading, createOrder, fetchOrders, fetchOrder };
});
