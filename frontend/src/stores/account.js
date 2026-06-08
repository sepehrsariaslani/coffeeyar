import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/lib/api.js";

export const STATUS_COLOR = {
  "در حال پردازش": "text-amber-600 bg-amber-50",
  "تایید شده": "text-blue-600 bg-blue-50",
  "در حال ارسال": "text-purple-600 bg-purple-50",
  "تحویل داده شده": "text-green-600 bg-green-50",
  "لغو شده": "text-red-600 bg-red-50",
};

/**
 * Account store — connected to the backend API.
 * Manages the logged-in customer's profile, addresses, and orders.
 * Falls back gracefully (empty lists) when the user is not authenticated
 * or the API is unreachable.
 */
export const useAccountStore = defineStore("account", () => {
  const profile = ref({ name: "", email: "", phone: "" });
  const addresses = ref([]);
  const orders = ref([]);

  const loadingOrders = ref(false);
  const loadingAddresses = ref(false);
  const loaded = ref(false);

  /**
   * Fetch the current user's profile from the server.
   * @returns {Promise<void>}
   */
  async function fetchProfile() {
    if (!api.getToken()) return;
    try {
      const me = await api.auth.me();
      profile.value = {
        name: me.name || me.profile?.full_name || "",
        email: me.email || "",
        phone: me.phone || me.profile?.mobile || "",
      };
    } catch (e) {
      console.error("خطا در دریافت پروفایل:", e.message);
    }
  }

  /**
   * Fetch the current user's orders from the server.
   * @returns {Promise<void>}
   */
  async function fetchOrders() {
    if (!api.getToken()) return;
    loadingOrders.value = true;
    try {
      const rows = await api.orders.list();
      orders.value = (rows || []).map(normalizeOrder);
    } catch (e) {
      console.error("خطا در دریافت سفارش‌ها:", e.message);
    } finally {
      loadingOrders.value = false;
    }
  }

  /**
   * Fetch a single order with its line items.
   * @param {string} ref Order reference / id.
   * @returns {Promise<object|null>}
   */
  async function fetchOrder(ref) {
    try {
      const o = await api.orders.get(ref);
      const normalized = normalizeOrder(o);
      const idx = orders.value.findIndex((x) => x.id === normalized.id);
      if (idx !== -1) orders.value[idx] = { ...orders.value[idx], ...normalized };
      return normalized;
    } catch (e) {
      console.error("خطا در دریافت سفارش:", e.message);
      return null;
    }
  }

  /**
   * Fetch the current user's saved addresses from the server.
   * @returns {Promise<void>}
   */
  async function fetchAddresses() {
    if (!api.getToken()) return;
    loadingAddresses.value = true;
    try {
      addresses.value = (await api.addresses.list()) || [];
    } catch (e) {
      console.error("خطا در دریافت آدرس‌ها:", e.message);
    } finally {
      loadingAddresses.value = false;
    }
  }

  /**
   * Load all account data in one shot. Safe to call multiple times.
   * @param {boolean} [force=false] Re-fetch even if already loaded.
   * @returns {Promise<void>}
   */
  async function init(force = false) {
    if (loaded.value && !force) return;
    loaded.value = true;
    await Promise.all([fetchProfile(), fetchOrders(), fetchAddresses()]);
  }

  /**
   * Update the user's profile both locally and on the server.
   * @param {{name?: string, email?: string, phone?: string}} patch
   * @returns {Promise<void>}
   */
  async function updateProfile(patch) {
    profile.value = { ...profile.value, ...patch };
    try {
      await api.auth.updateMe(patch);
    } catch (e) {
      console.error("خطا در ذخیره پروفایل:", e.message);
    }
  }

  /**
   * Create a new address on the server and refresh the list.
   * @param {object} addr Address payload.
   * @returns {Promise<void>}
   */
  async function addAddress(addr) {
    try {
      await api.addresses.create(addr);
      await fetchAddresses();
    } catch (e) {
      console.error("خطا در افزودن آدرس:", e.message);
    }
  }

  /**
   * Update an address. The backend has no PUT for addresses, so we
   * delete the old record and create a fresh one with the new data.
   * @param {object} addr Address payload including its `id`.
   * @returns {Promise<void>}
   */
  async function updateAddress(addr) {
    try {
      if (addr.id) await api.addresses.remove(addr.id);
      const { id, ...rest } = addr;
      await api.addresses.create(rest);
      await fetchAddresses();
    } catch (e) {
      console.error("خطا در ویرایش آدرس:", e.message);
    }
  }

  /**
   * Remove an address from the server and refresh the list.
   * @param {string} id Address id.
   * @returns {Promise<void>}
   */
  async function removeAddress(id) {
    try {
      await api.addresses.remove(id);
      addresses.value = addresses.value.filter((a) => a.id !== id);
    } catch (e) {
      console.error("خطا در حذف آدرس:", e.message);
    }
  }

  return {
    profile, addresses, orders,
    loadingOrders, loadingAddresses, loaded,
    init, fetchProfile, fetchOrders, fetchOrder, fetchAddresses,
    updateProfile, addAddress, updateAddress, removeAddress,
  };
});

/**
 * Normalize a raw order object from the API into the shape the UI expects.
 * @param {object} o Raw order from the backend.
 * @returns {object} Normalized order.
 */
function normalizeOrder(o) {
  return {
    id: o.id || o.name,
    date: o.date || "",
    status: o.status || o.order_status || "در حال پردازش",
    items: (o.items || []).map((it) => ({
      productId: it.productId || it.product || "",
      name: it.name || it.product_title || "",
      image: it.image || "",
      weight: it.weight || it.variant_title || "",
      grind: it.grind || "",
      unitPrice: Number(it.unitPrice || it.unit_price_toman || 0),
      qty: Number(it.qty || 1),
    })),
    totalPrice: Number(o.totalPrice || o.total_toman || 0),
    address: o.address || o.shipping_address || "",
    trackingCode: o.trackingCode || o.tracking_code || "",
  };
}
