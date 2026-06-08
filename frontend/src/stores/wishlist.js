import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { api } from "@/lib/api.js";
import { useAuthStore } from "./auth.js";

const LOCAL_KEY = "navar_wishlist_v1";

function loadLocal() {
  try { return JSON.parse(localStorage.getItem(LOCAL_KEY)) || []; } catch { return []; }
}
function saveLocal(v) { localStorage.setItem(LOCAL_KEY, JSON.stringify(v)); }

export const useWishlistStore = defineStore("wishlist", () => {
  const ids = ref(loadLocal());
  const products = ref([]);

  const count = computed(() => ids.value.length);

  function isWishlisted(productId) {
    return ids.value.includes(productId) || ids.value.includes(String(productId));
  }

  async function toggle(productId) {
    const auth = useAuthStore();
    if (auth.isLoggedIn) {
      try {
        const res = await api.wishlist.toggle(productId);
        if (res.wishlisted) {
          if (!ids.value.includes(productId)) ids.value.push(productId);
        } else {
          ids.value = ids.value.filter((id) => id !== productId && id !== String(productId));
        }
        saveLocal(ids.value);
        return;
      } catch (e) {
        console.error(e.message);
      }
    }
    const idx = ids.value.indexOf(productId);
    if (idx !== -1) ids.value.splice(idx, 1);
    else ids.value.push(productId);
    saveLocal(ids.value);
  }

  async function fetchWishlistIds() {
    const auth = useAuthStore();
    if (!auth.isLoggedIn) return;
    try {
      const res = await api.wishlist.ids();
      ids.value = res.ids;
      saveLocal(ids.value);
    } catch {}
  }

  async function fetchWishlistProducts() {
    const auth = useAuthStore();
    if (!auth.isLoggedIn) return [];
    try {
      products.value = await api.wishlist.list();
      return products.value;
    } catch {
      return [];
    }
  }

  function remove(productId) {
    ids.value = ids.value.filter((id) => id !== productId && id !== String(productId));
    saveLocal(ids.value);
  }

  async function fetchWishlist() {
    await fetchWishlistIds();
    await fetchWishlistProducts();
  }

  const items = computed(() => products.value);

  return { ids, products, items, count, isWishlisted, toggle, remove, fetchWishlistIds, fetchWishlistProducts, fetchWishlist };
});
