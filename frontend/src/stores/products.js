import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/lib/api.js";
import { isDemoMode } from "@/lib/demo.js";
import { getDemoProduct, getDemoProducts } from "@/data/demoData.js";

export const useProductsStore = defineStore("products", () => {
  const products = ref([]);
  const currentProduct = ref(null);
  const loading = ref(false);
  const total = ref(0);
  const page = ref(1);
  const hasNext = ref(false);

  function _mapProduct(p) {
    return {
      // Identity
      id: p.slug || p.name,
      name: p.title || p.name,
      title: p.title || p.name,
      item_name: p.title || p.name,
      slug: p.slug || p.name,
      // Category
      category: p.category,
      category_title: p.category_title,
      category_name: p.category_title || p.category,
      category_slug: p.category_slug || p.category_root || p.category,
      category_id: p.category,
      // Pricing
      price: p.effective_price_toman || p.price_toman || 0,
      price_toman: p.price_toman || 0,
      discount_toman: p.discount_toman || 0,
      effective_price_toman: p.effective_price_toman || p.price_toman || 0,
      // Stock
      stock_qty: p.stock_qty || 0,
      stock: p.stock_qty > 5 ? "in_stock" : p.stock_qty > 0 ? "low_stock" : "out_of_stock",
      // Media
      image: p.image,
      gallery: p.gallery || (p.image ? [p.image] : []),
      gallery_json: p.gallery_json,
      // Description
      short_description: p.short_description,
      description: p.description || p.short_description,
      // Flags
      has_variants: p.has_variants,
      is_featured: p.is_featured,
      is_published: p.is_published,
      display_order: p.display_order,
      // Variants
      variants: p.variants || [],
      // Extra fields expected by components
      type: p.type || "coffee",
      origin: p.origin || p.category_title || "",
      roast: p.roast || "",
      notes: p.notes || [],
      grinds: p.grinds || [],
      specs: p.specs || [],
      flavor: p.flavor || null,
      brand: p.brand || "",
      productFaqs: p.product_faqs || [],
      // SEO
      seo_title: p.seo_title || "",
      seo_description: p.seo_description || "",
    };
  }

  async function fetchProducts(params = {}) {
    loading.value = true;
    try {
      const res = isDemoMode ? getDemoProducts(params) : await api.products.list(params);
      products.value = (res.items || []).map(_mapProduct);
      total.value = res.total || 0;
      page.value = res.page || 1;
      hasNext.value = res.has_next || false;
      return res;
    } catch (e) {
      // A local catalogue keeps the preview useful when the API is offline.
      console.error("خطا در دریافت محصولات:", e.message);
      const fallback = getDemoProducts(params);
      products.value = fallback.items.map(_mapProduct);
      total.value = fallback.total;
      page.value = fallback.page;
      hasNext.value = fallback.has_next;
      return fallback;
    } finally {
      loading.value = false;
    }
  }

  async function fetchProduct(slug) {
    loading.value = true;
    try {
      const raw = isDemoMode ? getDemoProduct(slug) : await api.products.get(slug);
      currentProduct.value = raw ? _mapProduct(raw) : null;
      return currentProduct.value;
    } catch (e) {
      console.error("خطا در دریافت محصول:", e.message);
      const fallback = getDemoProduct(slug);
      currentProduct.value = fallback ? _mapProduct(fallback) : null;
      return currentProduct.value;
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
