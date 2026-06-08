import { defineStore } from "pinia";
import { ref, computed } from "vue";

const KEY = "navar_categories_v2";

const defaultCategories = [
  {
    id: "cat-coffee",
    name: "قهوه",
    slug: "coffee",
    icon: "☕",
    color: "#6b4226",
    parentId: null,
    order: 0,
    attributes: [
      { key: "origin", label: "خاستگاه", type: "text", options: [] },
      { key: "roast", label: "درجه برشته", type: "select", options: ["روشن", "متوسط", "تیره"] },
      { key: "process", label: "فرآوری", type: "select", options: ["شسته", "نچرال", "هانی", "شسته دوگانه"] },
    ],
    hasVariants: true,
    variantLabel: "وزن",
    defaultVariants: [
      { label: "۲۵۰ گرم", multiplier: 1 },
      { label: "۵۰۰ گرم", multiplier: 1.9 },
      { label: "۱ کیلوگرم", multiplier: 3.5 },
    ],
    hasGrinds: true,
    defaultGrinds: ["دانه کامل", "اسپرسو", "موکاپات", "فرنچ پرس", "V60"],
  },
  {
    id: "sub-coffee-single",
    name: "قهوه تک‌خاستگاه",
    slug: "single-origin",
    icon: "🌱",
    color: "#6b4226",
    parentId: "cat-coffee",
    order: 0,
    attributes: [],
    hasVariants: false,
    variantLabel: "",
    defaultVariants: [],
    hasGrinds: false,
    defaultGrinds: [],
  },
  {
    id: "sub-coffee-blend",
    name: "بلند قهوه",
    slug: "blend",
    icon: "🔀",
    color: "#6b4226",
    parentId: "cat-coffee",
    order: 1,
    attributes: [],
    hasVariants: false,
    variantLabel: "",
    defaultVariants: [],
    hasGrinds: false,
    defaultGrinds: [],
  },
  {
    id: "cat-accessories",
    name: "اکسسوری",
    slug: "accessories",
    icon: "🫖",
    color: "#8b6914",
    parentId: null,
    order: 1,
    attributes: [
      { key: "brand", label: "برند", type: "text", options: [] },
      { key: "material", label: "جنس", type: "text", options: [] },
    ],
    hasVariants: false,
    variantLabel: "",
    defaultVariants: [],
    hasGrinds: false,
    defaultGrinds: [],
  },
  {
    id: "sub-acc-brewing",
    name: "وسایل دم‌آوری",
    slug: "brewing",
    icon: "🫗",
    color: "#8b6914",
    parentId: "cat-accessories",
    order: 0,
    attributes: [],
    hasVariants: false,
    variantLabel: "",
    defaultVariants: [],
    hasGrinds: false,
    defaultGrinds: [],
  },
  {
    id: "sub-acc-grinder",
    name: "آسیاب",
    slug: "grinder",
    icon: "⚙️",
    color: "#8b6914",
    parentId: "cat-accessories",
    order: 1,
    attributes: [],
    hasVariants: false,
    variantLabel: "",
    defaultVariants: [],
    hasGrinds: false,
    defaultGrinds: [],
  },
];

function load() {
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? JSON.parse(raw) : defaultCategories;
  } catch { return defaultCategories; }
}
function save(v) { localStorage.setItem(KEY, JSON.stringify(v)); }

export const useCategoriesStore = defineStore("categories", () => {
  const categories = ref(load());

  const roots = computed(() =>
    categories.value.filter((c) => !c.parentId).sort((a, b) => a.order - b.order)
  );

  function children(parentId) {
    return categories.value
      .filter((c) => c.parentId === parentId)
      .sort((a, b) => a.order - b.order);
  }

  function getById(id) { return categories.value.find((c) => c.id === id); }

  function getRootFor(id) {
    const cat = getById(id);
    if (!cat) return null;
    if (!cat.parentId) return cat;
    return getById(cat.parentId) || cat;
  }

  function getAttrsFor(id) {
    const root = getRootFor(id);
    return root?.attributes || [];
  }

  const tree = computed(() =>
    roots.value.map((r) => ({ ...r, children: children(r.id) }))
  );

  function add(data) {
    const newCat = {
      id: "cat-" + Date.now(),
      name: data.name || "دسته جدید",
      slug: data.slug || ("cat-" + Date.now()),
      icon: data.icon || "📦",
      color: data.color || "#6b7280",
      parentId: data.parentId || null,
      order: data.order ?? categories.value.filter((c) => c.parentId === (data.parentId || null)).length,
      attributes: data.attributes || [],
      hasVariants: data.hasVariants || false,
      variantLabel: data.variantLabel || "",
      defaultVariants: data.defaultVariants || [],
      hasGrinds: data.hasGrinds || false,
      defaultGrinds: data.defaultGrinds || [],
    };
    categories.value.push(newCat);
    save(categories.value);
    return newCat;
  }

  function update(id, patch) {
    const idx = categories.value.findIndex((c) => c.id === id);
    if (idx !== -1) {
      categories.value[idx] = { ...categories.value[idx], ...patch };
      save(categories.value);
    }
  }

  function remove(id) {
    if (!confirm("این دسته‌بندی و تمام زیردسته‌هایش حذف شوند؟")) return;
    categories.value = categories.value.filter(
      (c) => c.id !== id && c.parentId !== id
    );
    save(categories.value);
  }

  function reorder(id, dir) {
    const cat = getById(id);
    if (!cat) return;
    const siblings = cat.parentId ? children(cat.parentId) : roots.value;
    const idx = siblings.findIndex((c) => c.id === id);
    const swapIdx = dir === "up" ? idx - 1 : idx + 1;
    if (swapIdx < 0 || swapIdx >= siblings.length) return;
    const swapId = siblings[swapIdx].id;
    const catIdx = categories.value.findIndex((c) => c.id === id);
    const swapCatIdx = categories.value.findIndex((c) => c.id === swapId);
    [categories.value[catIdx].order, categories.value[swapCatIdx].order] = [
      categories.value[swapCatIdx].order,
      categories.value[catIdx].order,
    ];
    save(categories.value);
  }

  function getBySlug(slug) { return categories.value.find((c) => c.slug === slug); }

  return { categories, roots, children, getById, getRootFor, getAttrsFor, getBySlug, add, update, remove, reorder, tree };
});
