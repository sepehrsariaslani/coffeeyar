import { defineStore } from "pinia";
import { ref, computed } from "vue";

const KEY = "navar-cart-v1";

function loadCart() {
  try {
    return JSON.parse(localStorage.getItem(KEY) || "[]");
  } catch {
    return [];
  }
}

function saveCart(items) {
  localStorage.setItem(KEY, JSON.stringify(items));
}

export const useCartStore = defineStore("cart", () => {
  const items = ref(loadCart());

  const count = computed(() => items.value.reduce((s, i) => s + i.qty, 0));
  const total = computed(() =>
    items.value.reduce((s, i) => s + i.unitPrice * i.qty, 0)
  );

  function add(item) {
    const id = `${item.productId}-${item.weight}-${item.grind}`;
    const existing = items.value.find((i) => i.id === id);
    if (existing) {
      existing.qty += item.qty;
    } else {
      items.value.push({ ...item, id });
    }
    saveCart(items.value);
  }

  function remove(id) {
    items.value = items.value.filter((i) => i.id !== id);
    saveCart(items.value);
  }

  function setQty(id, qty) {
    if (qty <= 0) {
      remove(id);
      return;
    }
    const item = items.value.find((i) => i.id === id);
    if (item) {
      item.qty = qty;
      saveCart(items.value);
    }
  }

  function clear() {
    items.value = [];
    saveCart(items.value);
  }

  return { items, count, total, add, remove, setQty, clear };
});
