import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { api } from "@/lib/api.js";
import { useAuthStore } from "./auth.js";

/**
 * Customer notifications store — backed by the Frappe `User Notification`
 * doctype. Falls back silently to an empty list when not logged in.
 */
export const useNotificationsStore = defineStore("notifications", () => {
  const items = ref([]);
  const loaded = ref(false);

  const unreadCount = computed(() => items.value.filter((n) => !n.read).length);

  /**
   * Fetch the current user's notifications from the server.
   * @returns {Promise<void>}
   */
  async function refresh() {
    const auth = useAuthStore();
    if (!auth.isLoggedIn) {
      items.value = [];
      return;
    }
    try {
      const rows = await api.notifications.list();
      items.value = (rows || []).map(normalizeNotif);
      loaded.value = true;
    } catch (e) {
      console.error("خطا در دریافت اعلان‌ها:", e.message);
    }
  }

  /**
   * Mark a single notification as read.
   * @param {string} id Notification id.
   * @returns {Promise<void>}
   */
  async function markRead(id) {
    const item = items.value.find((n) => n.id === id);
    if (item) item.read = true;
    try { await api.notifications.markRead(id); } catch {}
  }

  /**
   * Mark all notifications as read.
   * @returns {Promise<void>}
   */
  async function markAllRead() {
    items.value.forEach((n) => (n.read = true));
    try { await api.notifications.markAllRead(); } catch {}
  }

  /**
   * Remove a notification.
   * @param {string} id Notification id.
   * @returns {Promise<void>}
   */
  async function remove(id) {
    items.value = items.value.filter((n) => n.id !== id);
    try { await api.notifications.remove(id); } catch {}
  }

  /**
   * Add an optimistic, client-side notification to the top of the list.
   * Used by flows (e.g. checkout) that want immediate UI feedback.
   * Server-originated notifications still come through `refresh()`.
   * @param {string} title Notification title.
   * @param {string} [body] Notification body.
   * @param {string} [type] Notification type tag.
   * @returns {void}
   */
  function add(title, body = "", type = "info") {
    items.value.unshift({
      id: "local-" + Date.now(),
      title,
      body,
      type,
      read: false,
      date: new Date().toLocaleDateString("fa-IR"),
      time: new Date().toLocaleTimeString("fa-IR"),
    });
    if (items.value.length > 50) items.value = items.value.slice(0, 50);
  }

  /**
   * Remove all notifications for the current user.
   * @returns {Promise<void>}
   */
  async function clear() {
    const ids = items.value.map((n) => n.id);
    items.value = [];
    await Promise.all(ids.map((id) => api.notifications.remove(id).catch(() => {})));
  }

  return { items, unreadCount, loaded, refresh, add, markRead, markAllRead, remove, clear };
});

/**
 * Normalize a raw notification into the UI shape.
 * @param {object} n Raw notification from the API.
 * @returns {object} Normalized notification.
 */
function normalizeNotif(n) {
  const d = n.datetime ? new Date(n.datetime) : new Date();
  return {
    id: n.id,
    title: n.title,
    body: n.body || "",
    type: n.type || "info",
    read: !!n.read,
    date: d.toLocaleDateString("fa-IR"),
    time: d.toLocaleTimeString("fa-IR"),
  };
}
