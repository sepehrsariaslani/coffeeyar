import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { api } from "@/lib/api.js";
import { isDemoMode } from "@/lib/demo.js";
import { copyDemo, DEMO_CATEGORIES } from "@/data/demoData.js";

export const useCategoriesStore = defineStore("categories", () => {
  const categories = ref([]);
  const loading = ref(false);
  const loaded = ref(false);

  const roots = computed(() =>
    categories.value.filter((c) => !c.parent_id).sort((a, b) => a.display_order - b.display_order)
  );

  function children(parentId) {
    return categories.value
      .filter((c) => c.parent_id === parentId)
      .sort((a, b) => a.display_order - b.display_order);
  }

  function getById(id) { return categories.value.find((c) => c.id === id); }
  function getBySlug(slug) { return categories.value.find((c) => c.slug === slug); }

  function getRootFor(id) {
    const cat = getById(id);
    if (!cat) return null;
    if (!cat.parent_id) return cat;
    return getById(cat.parent_id) || cat;
  }

  function getAttrsFor(id) {
    const root = getRootFor(id);
    return root?.attributes || [];
  }

  const tree = computed(() =>
    roots.value.map((r) => ({ ...r, children: children(r.id) }))
  );

  async function fetchCategories() {
    if (loaded.value) return;
    loading.value = true;
    try {
      categories.value = isDemoMode ? copyDemo(DEMO_CATEGORIES) : await api.categories.list();
      loaded.value = true;
    } catch (e) {
      console.error("خطا در دریافت دسته‌بندی‌ها:", e.message);
      categories.value = copyDemo(DEMO_CATEGORIES);
      loaded.value = true;
    } finally {
      loading.value = false;
    }
  }

  async function add(data) {
    try {
      const cat = await api.admin.categories.create({
        name: data.name,
        slug: data.slug || "",
        parent_id: data.parentId || data.parent_id || null,
        icon: data.icon || "📦",
        color: data.color || "#6b7280",
        has_variants: data.hasVariants || false,
        variant_label: data.variantLabel || "",
        has_grinds: data.hasGrinds || false,
        default_variants_json: JSON.stringify(data.defaultVariants || []),
        default_grinds_json: JSON.stringify(data.defaultGrinds || []),
        attributes_json: JSON.stringify(data.attributes || []),
        display_order: data.order ?? 0,
        is_active: true,
      });
      loaded.value = false;
      await fetchCategories();
      return cat;
    } catch (e) {
      console.error(e.message);
    }
  }

  async function update(id, patch) {
    const cat = getById(id);
    if (!cat) return;
    try {
      await api.admin.categories.update(id, {
        name: patch.name ?? cat.name,
        slug: patch.slug ?? cat.slug,
        parent_id: patch.parentId ?? patch.parent_id ?? cat.parent_id,
        icon: patch.icon ?? cat.icon,
        color: patch.color ?? cat.color,
        has_variants: patch.hasVariants ?? cat.has_variants,
        variant_label: patch.variantLabel ?? cat.variant_label,
        has_grinds: patch.hasGrinds ?? cat.has_grinds,
        default_variants_json: JSON.stringify(patch.defaultVariants ?? cat.default_variants),
        default_grinds_json: JSON.stringify(patch.defaultGrinds ?? cat.default_grinds),
        attributes_json: JSON.stringify(patch.attributes ?? cat.attributes),
        display_order: patch.order ?? cat.display_order,
        is_active: patch.is_active ?? cat.is_active,
        image: patch.image ?? cat.image,
        description: patch.description ?? cat.description,
      });
      loaded.value = false;
      await fetchCategories();
    } catch (e) {
      console.error(e.message);
    }
  }

  async function remove(id) {
    if (!confirm("این دسته‌بندی حذف شود؟")) return;
    try {
      await api.admin.categories.remove(id);
      categories.value = categories.value.filter((c) => c.id !== id && c.parent_id !== id);
    } catch (e) {
      console.error(e.message);
    }
  }

  return { categories, roots, loading, loaded, children, getById, getBySlug, getRootFor, getAttrsFor, tree, fetchCategories, add, update, remove };
});
