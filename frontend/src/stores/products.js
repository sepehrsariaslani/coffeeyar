import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/lib/api.js";

export const useProductsStore = defineStore("products", () => {
  const products = ref([]);
  const currentProduct = ref(null);
  const loading = ref(false);
  const total = ref(0);
  const page = ref(1);
  const hasNext = ref(false);

  async function fetchProducts(params = {}) {
    loading.value = true;
    try {
      const res = await api.products.list(params);
      products.value = res.items;
      total.value = res.total;
      page.value = res.page;
      hasNext.value = res.has_next;
      return res;
    } catch (e) {
      console.error("خطا در دریافت محصولات:", e.message);
      return { items: [], total: 0 };
    } finally {
      loading.value = false;
    }
  }

  async function fetchProduct(slug) {
    loading.value = true;
    try {
      currentProduct.value = await api.products.get(slug);
      return currentProduct.value;
    } catch (e) {
      console.error("خطا در دریافت محصول:", e.message);
      return null;
    } finally {
      loading.value = false;
    }
  }

  async function createProduct(data) {
    const res = await api.admin.products.create(data);
    return res;
  }

  async function updateProduct(id, data) {
    const res = await api.admin.products.update(id, data);
    return res;
  }

  async function deleteProduct(id) {
    await api.admin.products.remove(id);
    products.value = products.value.filter((p) => p.id !== id);
  }

  function getById(id) { return products.value.find((p) => p.id === id); }
  function getBySlug(slug) { return products.value.find((p) => p.slug === slug); }

  return {
    products, currentProduct, loading, total, page, hasNext,
    fetchProducts, fetchProduct, createProduct, updateProduct, deleteProduct,
    getById, getBySlug,
  };
});
