import { defineStore } from "pinia";
import { ref, computed } from "vue";

const KEY = "navar_notifications_v1";

function load() {
  try { const r = localStorage.getItem(KEY); return r ? JSON.parse(r) : []; } catch { return []; }
}
function save(v) { localStorage.setItem(KEY, JSON.stringify(v)); }

export const useNotificationsStore = defineStore("notifications", () => {
  const items = ref(load());

  const unreadCount = computed(() => items.value.filter((n) => !n.read).length);

  function add(title, body = "", type = "info") {
    items.value.unshift({
      id: Date.now().toString(),
      title,
      body,
      type,
      read: false,
      date: new Date().toLocaleDateString("fa-IR"),
      time: new Date().toLocaleTimeString("fa-IR"),
    });
    if (items.value.length > 50) items.value = items.value.slice(0, 50);
    save(items.value);
  }

  function markRead(id) {
    const item = items.value.find((n) => n.id === id);
    if (item) { item.read = true; save(items.value); }
  }

  function markAllRead() {
    items.value.forEach((n) => (n.read = true));
    save(items.value);
  }

  function remove(id) {
    items.value = items.value.filter((n) => n.id !== id);
    save(items.value);
  }

  function clear() {
    items.value = [];
    save(items.value);
  }

  return { items, unreadCount, add, markRead, markAllRead, remove, clear };
});
