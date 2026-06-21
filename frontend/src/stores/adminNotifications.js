import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useAdminNotificationsStore = defineStore("adminNotifications", () => {
  const notifications = ref([]);

  function load() {
    try {
      const saved = localStorage.getItem("adminNotifications");
      if (saved) notifications.value = JSON.parse(saved);
    } catch {}
  }

  function save() {
    localStorage.setItem("adminNotifications", JSON.stringify(notifications.value));
  }

  function add(title, body, orderId = null, amount = null) {
    notifications.value.unshift({
      id: Date.now(),
      title,
      body,
      orderId,
      amount,
      read: false,
      time: new Date().toLocaleString("fa-IR"),
    });
    if (notifications.value.length > 50) notifications.value = notifications.value.slice(0, 50);
    save();
  }

  function markRead(id) {
    const n = notifications.value.find((n) => n.id === id);
    if (n) { n.read = true; save(); }
  }

  function markAllRead() {
    notifications.value.forEach((n) => (n.read = true));
    save();
  }

  function remove(id) {
    notifications.value = notifications.value.filter((n) => n.id !== id);
    save();
  }

  const unread = computed(() => notifications.value.filter((n) => !n.read).length);

  load();

  return { notifications, unread, add, markRead, markAllRead, remove };
});
