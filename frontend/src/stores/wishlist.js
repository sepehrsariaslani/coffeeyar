import { defineStore } from "pinia";
import { ref, computed } from "vue";

const KEY = "navar_wishlist_v1";

function load() {
  try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; }
}

export const useWishlistStore = defineStore("wishlist", () => {
  const ids = ref(load());

  function save() { localStorage.setItem(KEY, JSON.stringify(ids.value)); }

  const count = computed(() => ids.value.length);

  function isWishlisted(productId) { return ids.value.includes(productId); }

  function toggle(productId) {
    const idx = ids.value.indexOf(productId);
    if (idx !== -1) ids.value.splice(idx, 1);
    else ids.value.push(productId);
    save();
  }

  function remove(productId) {
    ids.value = ids.value.filter((id) => id !== productId);
    save();
  }

  return { ids, count, isWishlisted, toggle, remove };
});
