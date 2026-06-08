<script setup>
import { ref, computed, watch, onMounted, nextTick } from "vue";
import { useRoute } from "vue-router";
import { useProductsStore } from "@/stores/products.js";
function formatPrice(n) { return n ? Number(n).toLocaleString("fa-IR") : "۰"; }
import { useTemplatesStore } from "@/stores/templates.js";
import { useCategoriesStore } from "@/stores/categories.js";
import { Plus, Pencil, Trash2, Search, X, Eye, EyeOff, Layers, Check, Download, Upload, FolderOpen, ChevronDown, BarChart2 } from "lucide-vue-next";
import ViewSwitcher from "@/components/admin/ViewSwitcher.vue";
import ImageUploader from "@/components/ImageUploader.vue";

const route = useRoute();

const templatesStore = useTemplatesStore();
const categoriesStore = useCategoriesStore();

const productsStore = useProductsStore();
const list = ref([]);
const query = ref("");
const categoryFilter = ref("all");
const subCategoryFilter = ref("all");
const hidden = ref(new Set());

const editState = ref({ mode: "closed" });
const inlineEdit = ref(null);
const inlineForm = ref({});

const filtered = computed(() =>
  list.value.filter((p) => {
    const catOk = categoryFilter.value === "all" || p.categoryId === categoryFilter.value;
    const subOk = subCategoryFilter.value === "all" || p.subCategoryId === subCategoryFilter.value;
    const queryOk =
      !query.value ||
      p.name.includes(query.value) ||
      Object.values(p.attrs || {}).some((v) => String(v).includes(query.value));
    return catOk && subOk && queryOk;
  })
);

const catName = (catId) => {
  if (!catId) return "—";
  return categoriesStore.getById(catId)?.name || "—";
};
const subCatName = (subId) => {
  if (!subId) return "—";
  return categoriesStore.getById(subId)?.name || "—";
};

function remove(id) {
  if (confirm("این محصول حذف شود؟")) {
    list.value = list.value.filter((p) => p.id !== id);
    if (inlineEdit.value === id) inlineEdit.value = null;
  }
}

function toggleHide(id) {
  const n = new Set(hidden.value);
  if (n.has(id)) n.delete(id);
  else n.add(id);
  hidden.value = n;
}

function save(data) {
  const exists = list.value.find((p) => p.id === data.id);
  if (exists) {
    list.value = list.value.map((p) => (p.id === data.id ? data : p));
  } else {
    list.value.push(data);
  }
  editState.value = { mode: "closed" };
}

function openInline(p) {
  if (inlineEdit.value === p.id) {
    inlineEdit.value = null;
    return;
  }
  inlineForm.value = {
    id: p.id,
    name: p.name,
    price: p.price,
    categoryId: p.categoryId || "",
    subCategoryId: p.subCategoryId || "",
    stock: p.stock || "in_stock",
    stockCount: p.stockCount ?? 0,
  };
  inlineEdit.value = p.id;
}

function saveInline() {
  list.value = list.value.map((p) => {
    if (p.id !== inlineForm.value.id) return p;
    return { ...p, ...inlineForm.value };
  });
  inlineEdit.value = null;
}

const emptyProduct = {
  id: "", name: "", categoryId: "", subCategoryId: "",
  attrs: {},
  price: 0, image: "", gallery: [],
  weights: [], grinds: [],
  flavor: { bitterness: 5, acidity: 5, aroma: 5 },
  notes: [], description: "",
  specs: [{ label: "", value: "" }],
  customAttributes: {}, productFaqs: [],
};

// ─── CSV Export / Import ────────────────────────────────────────────────────

function exportCSV() {
  const headers = ["id", "categoryId", "subCategoryId", "name", "price", "description", "stock", "stockCount"];
  const rows = list.value.map((p) => [
    p.id, p.categoryId || "", p.subCategoryId || "", p.name, p.price,
    (p.description || "").replace(/\r?\n/g, " "),
    p.stock || "in_stock", p.stockCount ?? 0,
  ]);
  const escape = (v) => `"${String(v ?? "").replace(/"/g, '""')}"`;
  const csv = [headers, ...rows].map((r) => r.map(escape).join(",")).join("\r\n");
  const blob = new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "products-navar.csv";
  a.click();
  URL.revokeObjectURL(url);
}

const importInput = ref(null);
function triggerImport() { importInput.value?.click(); }

function parseCSVLine(line) {
  const result = [];
  let cur = "", inQ = false;
  for (let i = 0; i < line.length; i++) {
    if (line[i] === '"') {
      if (inQ && line[i + 1] === '"') { cur += '"'; i++; }
      else inQ = !inQ;
    } else if (line[i] === "," && !inQ) {
      result.push(cur.trim());
      cur = "";
    } else {
      cur += line[i];
    }
  }
  result.push(cur.trim());
  return result;
}

function handleImport(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (ev) => {
    try {
      const text = ev.target.result.replace(/^\uFEFF/, "");
      const lines = text.split(/\r?\n/).filter(Boolean);
      if (lines.length < 2) { alert("فایل CSV معتبر نیست."); return; }
      const headers = parseCSVLine(lines[0]);
      const idx = (k) => headers.indexOf(k);
      let updated = 0;
      lines.slice(1).forEach((line) => {
        const row = parseCSVLine(line);
        const id = row[idx("id")];
        if (!id) return;
        const match = list.value.find((p) => p.id === id);
        if (!match) return;
        if (idx("name") >= 0 && row[idx("name")]) match.name = row[idx("name")];
        if (idx("price") >= 0 && row[idx("price")]) {
          const p = parseFloat(row[idx("price")]);
          if (!isNaN(p)) match.price = p;
        }
        if (idx("description") >= 0) match.description = row[idx("description")] || match.description;
        if (idx("roast") >= 0 && row[idx("roast")]) match.roast = row[idx("roast")];
        if (idx("category") >= 0 && row[idx("category")]) match.category = row[idx("category")];
        updated++;
      });
      alert(`${updated} محصول با موفقیت بروزرسانی شد.`);
    } catch {
      alert("خطا در پردازش فایل CSV.");
    }
    e.target.value = "";
  };
  reader.readAsText(file, "UTF-8");
}

// ─── Product-specific FAQ helpers ───────────────────────────────────────────

function addFaq() {
  if (!form.value.productFaqs) form.value.productFaqs = [];
  form.value.productFaqs.push({ q: "", a: "" });
}
function removeFaq(i) { form.value.productFaqs.splice(i, 1); }

const form = ref({ ...emptyProduct });
const notesText = ref("");
const grindsText = ref("");
const drawerTab = ref("basic");

const selectedRootCat = computed(() => {
  if (!form.value.categoryId) return null;
  return categoriesStore.getRootFor(form.value.categoryId) || categoriesStore.getById(form.value.categoryId);
});
const selectedCatChildren = computed(() => {
  if (!form.value.categoryId) return [];
  return categoriesStore.children(form.value.categoryId);
});
const selectedCatAttrs = computed(() => selectedRootCat.value?.attributes || []);
const selectedCatHasVariants = computed(() => selectedRootCat.value?.hasVariants || false);
const selectedCatHasGrinds = computed(() => selectedRootCat.value?.hasGrinds || false);

function openCreate() {
  form.value = { ...emptyProduct };
  notesText.value = "";
  grindsText.value = "";
  drawerTab.value = "basic";
  editState.value = { mode: "create" };
}

function openEdit(p) {
  form.value = {
    ...emptyProduct,
    ...p,
    attrs: p.attrs ? { ...p.attrs } : {},
    specs: p.specs ? [...p.specs.map((s) => ({ ...s }))] : [{ label: "", value: "" }],
    productFaqs: p.productFaqs ? [...p.productFaqs.map((f) => ({ ...f }))] : [],
  };
  notesText.value = p.notes ? p.notes.join("، ") : "";
  grindsText.value = p.grinds ? p.grinds.join("، ") : "";
  drawerTab.value = "basic";
  editState.value = { mode: "edit", product: p };
  inlineEdit.value = null;
}

function applyTemplate(templateId) {
  const tpl = templatesStore.templates.find((t) => t.id === templateId);
  if (!tpl) return;
  const attrs = {};
  tpl.attributes.forEach((a) => {
    attrs[a.name] = form.value.customAttributes?.[a.name] ?? (a.options[0]?.value ?? "");
  });
  form.value = {
    ...form.value,
    templateId,
    weights: [...tpl.weights],
    grinds: [...tpl.grinds],
    roast: tpl.defaultRoast,
    process: tpl.defaultProcess,
    customAttributes: attrs,
  };
  grindsText.value = tpl.grinds.join("، ");
}

function submitForm(e) {
  e.preventDefault();
  save({
    ...form.value,
    id: form.value.id || form.value.name.replace(/\s+/g, "-").toLowerCase() + "-" + Date.now(),
    notes: notesText.value ? notesText.value.split(/[،,]/).map((n) => n.trim()).filter(Boolean) : (form.value.notes || []),
    grinds: grindsText.value ? grindsText.value.split(/[،,]/).map((n) => n.trim()).filter(Boolean) : (form.value.grinds || []),
    gallery: form.value.gallery.filter(Boolean),
    specs: (form.value.specs || []).filter((s) => s.label.trim()),
    weights: (form.value.weights || []).filter((w) => w.label?.trim()),
  });
}

function addGalleryImg() { form.value.gallery.push(""); }
function setGalleryImg(i, v) { form.value.gallery[i] = v; }
function removeGalleryImg(i) { form.value.gallery.splice(i, 1); }
function addWeight() { form.value.weights.push({ label: "", multiplier: 1 }); }
function removeWeight(i) { form.value.weights.splice(i, 1); }
function addSpec() { form.value.specs.push({ label: "", value: "" }); }
function removeSpec(i) { form.value.specs.splice(i, 1); }

const activeTabs = computed(() => [
  { id: "basic", label: "اطلاعات پایه" },
  { id: "media", label: "گالری تصاویر" },
  ...(selectedCatHasVariants.value ? [{ id: "variants", label: "وزن‌ها و آسیاب" }] : []),
  { id: "specs", label: "مشخصات فنی" },
  { id: "faqs", label: "سوالات" },
]);

onMounted(() => {
  const tplId = route.query.template;
  if (tplId) {
    openCreate();
    nextTick(() => applyTemplate(tplId));
  }
});

// ── View mode ──
const viewMode = ref(localStorage.getItem("navar-products-view") || "list");
watch(viewMode, (v) => localStorage.setItem("navar-products-view", v));

// ── Filter presets ──
const savedPresets = ref(JSON.parse(localStorage.getItem("navar-product-presets") || "[]"));
const presetDraft = ref("");
const showPresetInput = ref(false);

function saveCurrentPreset() {
  if (!presetDraft.value.trim()) return;
  savedPresets.value.push({
    id: Date.now(),
    name: presetDraft.value,
    filters: { query: query.value, categoryFilter: categoryFilter.value, subCategoryFilter: subCategoryFilter.value },
  });
  localStorage.setItem("navar-product-presets", JSON.stringify(savedPresets.value));
  presetDraft.value = "";
  showPresetInput.value = false;
}
function applyPreset(p) {
  query.value = p.filters.query || "";
  categoryFilter.value = p.filters.categoryFilter || "all";
  subCategoryFilter.value = p.filters.subCategoryFilter || "all";
}
function deletePreset(id) {
  savedPresets.value = savedPresets.value.filter((p) => p.id !== id);
  localStorage.setItem("navar-product-presets", JSON.stringify(savedPresets.value));
}

// ── Kanban: products grouped by sub-category ──
const kanbanColumns = computed(() => {
  const cols = categoriesStore.categories
    .filter((c) => c.parentId)
    .map((sub) => ({
      id: sub.id,
      name: sub.name,
      icon: sub.icon,
      color: sub.color,
      products: filtered.value.filter((p) => p.subCategoryId === sub.id),
    })).filter((c) => c.products.length > 0);
  const noCat = filtered.value.filter((p) => !p.subCategoryId);
  if (noCat.length) cols.push({ id: "__none", name: "بدون دسته", icon: "📦", color: "#6b7280", products: noCat });
  return cols;
});

// ── Tree: expandable category hierarchy ──
const expandedGroups = ref(new Set(["__none", ...categoriesStore.categories.filter((c) => c.parentId).map((c) => c.id)]));
function toggleGroup(id) {
  const s = new Set(expandedGroups.value);
  if (s.has(id)) s.delete(id); else s.add(id);
  expandedGroups.value = s;
}

// ── Report stats ──
const reportStats = computed(() => {
  const all = list.value;
  const maxPrice = Math.max(...all.map((p) => p.price), 1);
  const avgPrice = all.length ? Math.round(all.reduce((s, p) => s + p.price, 0) / all.length) : 0;
  const byCategory = categoriesStore.roots.map((r) => ({
    name: r.name,
    icon: r.icon,
    count: all.filter((p) => p.categoryId === r.id).length,
    max: all.length || 1,
  })).filter((c) => c.count > 0);
  const bySubCat = categoriesStore.categories.filter((c) => c.parentId).map((sub) => ({
    name: sub.name,
    count: all.filter((p) => p.subCategoryId === sub.id).length,
    max: all.length || 1,
  })).filter((c) => c.count > 0);
  return { total: all.length, avgPrice, maxPrice, byCategory, bySubCat };
});
</script>

<template>
  <div class="p-4 md:p-10">
    <div class="mb-8 flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 class="text-3xl font-light">محصولات <span class="text-maroon">.</span></h1>
        <p class="mt-2 text-sm text-muted-foreground">{{ filtered.length }} از {{ list.length }} محصول</p>
      </div>
      <div class="flex flex-wrap gap-2">
        <button
          type="button"
          @click="exportCSV"
          class="inline-flex items-center gap-2 border border-border px-4 py-2.5 text-sm hover:bg-accent"
          title="دانلود CSV همه محصولات"
        >
          <Download class="h-4 w-4" /> خروجی CSV
        </button>
        <button
          type="button"
          @click="triggerImport"
          class="inline-flex items-center gap-2 border border-border px-4 py-2.5 text-sm hover:bg-accent"
          title="ورودی CSV — بروزرسانی محصولات"
        >
          <Upload class="h-4 w-4" /> ورودی CSV
        </button>
        <input ref="importInput" type="file" accept=".csv" class="hidden" @change="handleImport" />
        <button
          type="button"
          @click="openCreate()"
          class="inline-flex items-center gap-2 bg-maroon px-4 py-2.5 text-sm text-maroon-foreground hover:opacity-90"
        >
          <Plus class="h-4 w-4" /> محصول جدید
        </button>
        <ViewSwitcher v-model="viewMode" :modes="['list','gallery','kanban','tree','report']" />
      </div>
    </div>

    <!-- Filters -->
    <div class="mb-6 flex flex-wrap items-center gap-3">
      <div class="relative min-w-[200px] flex-1">
        <Search class="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <input v-model="query" placeholder="جستجو در محصولات…" class="w-full border border-border bg-background py-2.5 pr-10 pl-3 text-sm outline-none focus:border-maroon" />
      </div>
      <!-- Category filter -->
      <div class="flex gap-1 border border-border p-1 flex-wrap">
        <button
          type="button"
          @click="categoryFilter = 'all'; subCategoryFilter = 'all'"
          :class="['px-3 py-1.5 text-xs transition-colors', categoryFilter === 'all' ? 'bg-maroon text-maroon-foreground' : 'hover:bg-accent']"
        >همه</button>
        <button
          v-for="cat in categoriesStore.roots"
          :key="cat.id"
          type="button"
          @click="categoryFilter = cat.id; subCategoryFilter = 'all'"
          :class="['px-3 py-1.5 text-xs transition-colors flex items-center gap-1', categoryFilter === cat.id ? 'bg-maroon text-maroon-foreground' : 'hover:bg-accent']"
        >{{ cat.icon }} {{ cat.name }}</button>
      </div>
      <!-- Sub-category filter -->
      <select
        v-if="categoryFilter !== 'all' && categoriesStore.children(categoryFilter).length > 0"
        v-model="subCategoryFilter"
        class="border border-border bg-background px-3 py-2 text-xs outline-none focus:border-maroon"
      >
        <option value="all">همه زیردسته‌ها</option>
        <option v-for="sub in categoriesStore.children(categoryFilter)" :key="sub.id" :value="sub.id">
          {{ sub.icon }} {{ sub.name }}
        </option>
      </select>
    </div>

    <!-- Filter presets -->
    <div v-if="savedPresets.length > 0" class="mb-3 flex flex-wrap items-center gap-2">
      <span class="text-xs text-muted-foreground shrink-0">فیلترهای ذخیره شده:</span>
      <button
        v-for="preset in savedPresets"
        :key="preset.id"
        class="flex items-center gap-1.5 border border-border px-2.5 py-1 text-xs hover:border-maroon/50 hover:bg-accent transition-colors"
        @click="applyPreset(preset)"
      >
        {{ preset.name }}
        <span @click.stop="deletePreset(preset.id)" class="text-muted-foreground hover:text-maroon leading-none">×</span>
      </button>
    </div>
    <div class="mb-6">
      <div v-if="showPresetInput" class="flex items-center gap-2 flex-wrap">
        <input
          v-model="presetDraft"
          @keydown.enter="saveCurrentPreset"
          @keydown.escape="showPresetInput = false"
          placeholder="نام فیلتر…"
          class="border border-border px-3 py-1.5 text-xs outline-none focus:border-maroon bg-background"
          autofocus
        />
        <button @click="saveCurrentPreset" class="bg-maroon px-3 py-1.5 text-xs text-white hover:opacity-90">ذخیره</button>
        <button @click="showPresetInput = false" class="border border-border px-3 py-1.5 text-xs hover:bg-accent">انصراف</button>
      </div>
      <button
        v-else
        @click="showPresetInput = true"
        class="text-xs text-muted-foreground hover:text-maroon transition-colors"
      >+ ذخیره فیلتر فعلی</button>
    </div>

    <!-- ── LIST VIEW ── -->
    <template v-if="viewMode === 'list'">
    <!-- MOBILE: Card list -->
    <div class="md:hidden space-y-3">
      <div
        v-for="p in filtered"
        :key="p.id"
        :class="['border border-border', hidden.has(p.id) ? 'opacity-50' : '']"
      >
        <div class="flex items-center gap-3 p-3">
          <img v-if="p.image" :src="p.image" alt="" class="h-14 w-14 shrink-0 object-cover" />
          <div v-else class="h-14 w-14 shrink-0 bg-muted flex items-center justify-center text-muted-foreground text-xs">بدون</div>
          <div class="flex-1 min-w-0">
            <div class="font-medium text-sm truncate">{{ p.name }}</div>
            <div class="mt-0.5 text-xs text-muted-foreground">{{ catName(p.categoryId) }}{{ p.subCategoryId ? ' / ' + subCatName(p.subCategoryId) : '' }}</div>
            <div class="mt-1 flex items-center gap-2 flex-wrap">
              <span class="text-xs text-maroon font-medium">{{ formatPrice(p.price) }}</span>
              <span :class="['text-xs', hidden.has(p.id) ? 'text-muted-foreground' : 'text-maroon']">
                {{ hidden.has(p.id) ? "پنهان" : "فعال" }}
              </span>
            </div>
          </div>
          <div class="flex flex-col gap-1 shrink-0">
            <button type="button" @click="openInline(p)" :class="['p-2 hover:bg-accent', inlineEdit === p.id ? 'text-maroon' : 'hover:text-maroon']">
              <Pencil class="h-4 w-4" />
            </button>
            <button type="button" @click="toggleHide(p.id)" class="p-2 hover:bg-accent hover:text-maroon">
              <EyeOff v-if="hidden.has(p.id)" class="h-4 w-4" />
              <Eye v-else class="h-4 w-4" />
            </button>
          </div>
        </div>

        <!-- Mobile inline edit -->
        <div v-if="inlineEdit === p.id" class="border-t border-border bg-muted/30 p-3 space-y-3">
          <div class="grid grid-cols-2 gap-2">
            <label class="block">
              <span class="text-xs text-muted-foreground uppercase tracking-wider">نام</span>
              <input v-model="inlineForm.name" class="mt-1 w-full border border-border bg-background px-2 py-1.5 text-sm outline-none focus:border-maroon" />
            </label>
            <label class="block">
              <span class="text-xs text-muted-foreground uppercase tracking-wider">قیمت</span>
              <input type="number" v-model.number="inlineForm.price" class="mt-1 w-full border border-border bg-background px-2 py-1.5 text-sm outline-none focus:border-maroon" />
            </label>
          </div>
          <div class="grid grid-cols-2 gap-2">
            <label class="block">
              <span class="text-xs text-muted-foreground uppercase tracking-wider">دسته اصلی</span>
              <select v-model="inlineForm.categoryId" class="mt-1 w-full border border-border bg-background px-2 py-1.5 text-sm outline-none focus:border-maroon">
                <option value="">— انتخاب</option>
                <option v-for="c in categoriesStore.roots" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
              </select>
            </label>
            <label class="block">
              <span class="text-xs text-muted-foreground uppercase tracking-wider">زیردسته</span>
              <select v-model="inlineForm.subCategoryId" class="mt-1 w-full border border-border bg-background px-2 py-1.5 text-sm outline-none focus:border-maroon">
                <option value="">— انتخاب</option>
                <option v-for="s in categoriesStore.children(inlineForm.categoryId || '')" :key="s.id" :value="s.id">{{ s.name }}</option>
              </select>
            </label>
          </div>
          <div class="grid grid-cols-2 gap-2">
            <label class="block">
              <span class="text-xs text-muted-foreground uppercase tracking-wider">موجودی انبار</span>
              <select v-model="inlineForm.stock" class="mt-1 w-full border border-border bg-background px-2 py-1.5 text-sm outline-none focus:border-maroon">
                <option value="in_stock">موجود</option>
                <option value="low_stock">موجودی محدود</option>
                <option value="out_of_stock">ناموجود</option>
              </select>
            </label>
            <label class="block">
              <span class="text-xs text-muted-foreground uppercase tracking-wider">تعداد موجود</span>
              <input type="number" v-model.number="inlineForm.stockCount" min="0" class="mt-1 w-full border border-border bg-background px-2 py-1.5 text-sm outline-none focus:border-maroon" />
            </label>
          </div>
          <div class="flex items-center gap-2 justify-end">
            <button type="button" @click="inlineEdit = null" class="border border-border px-4 py-1.5 text-xs hover:bg-accent">انصراف</button>
            <button type="button" @click="saveInline" class="bg-maroon px-4 py-1.5 text-xs text-maroon-foreground hover:opacity-90 flex items-center gap-1.5">
              <Check class="h-3 w-3" /> ذخیره
            </button>
            <button type="button" @click="openEdit(p)" class="border border-maroon px-4 py-1.5 text-xs text-maroon hover:bg-maroon hover:text-white transition-colors">ویرایش کامل</button>
          </div>
        </div>

        <!-- Mobile delete -->
        <div class="flex border-t border-border divide-x divide-border">
          <button type="button" @click="openEdit(p)" class="flex-1 py-2 text-xs text-muted-foreground hover:text-maroon hover:bg-accent text-center">ویرایش کامل</button>
          <button type="button" @click="remove(p.id)" class="flex-1 py-2 text-xs text-maroon hover:bg-accent text-center">حذف</button>
        </div>
      </div>
      <div v-if="filtered.length === 0" class="border border-dashed border-border p-12 text-center text-muted-foreground text-sm">هیچ محصولی یافت نشد</div>
    </div>

    <!-- DESKTOP: Table -->
    <div class="hidden md:block border border-border">
      <table class="w-full text-sm">
        <thead class="bg-muted text-xs uppercase tracking-widest text-muted-foreground">
          <tr>
            <th class="px-5 py-4 text-right">محصول</th>
            <th class="px-5 py-4 text-right">دسته اصلی</th>
            <th class="px-5 py-4 text-right">زیردسته</th>
            <th class="px-5 py-4 text-right">قیمت</th>
            <th class="px-5 py-4 text-right">وضعیت</th>
            <th class="px-5 py-4"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-border">
          <template v-for="p in filtered" :key="p.id">
            <tr :class="['hover:bg-accent/40 transition-colors', hidden.has(p.id) ? 'opacity-50' : '', inlineEdit === p.id ? 'bg-maroon/5' : '']">
              <td class="px-5 py-3">
                <div class="flex items-center gap-3">
                  <img v-if="p.image" :src="p.image" alt="" class="h-11 w-11 object-cover shrink-0" />
                  <div v-else class="h-11 w-11 bg-muted flex items-center justify-center text-muted-foreground text-xs shrink-0">بدون</div>
                  <div>
                    <div class="font-medium">{{ p.name }}</div>
                    <div class="text-xs text-muted-foreground">{{ p.notes?.join(" · ") || "—" }}</div>
                  </div>
                </div>
              </td>
              <td class="px-5 py-3">
                <span :class="['text-xs px-2 py-0.5 border', p.categoryId ? 'border-maroon/30 text-maroon' : 'border-border text-muted-foreground']">
                  {{ catName(p.categoryId) }}
                </span>
              </td>
              <td class="px-5 py-3 text-muted-foreground text-sm">
                {{ subCatName(p.subCategoryId) }}
              </td>
              <td class="px-5 py-3 text-maroon text-sm">{{ formatPrice(p.price) }}</td>
              <td class="px-5 py-3">
                <div class="space-y-1">
                  <span :class="['text-xs block', hidden.has(p.id) ? 'text-muted-foreground' : 'text-green-600']">
                    {{ hidden.has(p.id) ? "پنهان" : "فعال" }}
                  </span>
                  <span :class="['text-xs block', p.stock === 'out_of_stock' ? 'text-red-500' : p.stock === 'low_stock' ? 'text-amber-500' : 'text-muted-foreground']">
                    {{ p.stock === 'out_of_stock' ? 'ناموجود' : p.stock === 'low_stock' ? `محدود (${p.stockCount})` : p.stockCount ? `موجود (${p.stockCount})` : 'موجود' }}
                  </span>
                </div>
              </td>
              <td class="px-5 py-3">
                <div class="flex justify-end gap-1">
                  <button
                    type="button"
                    @click="openInline(p)"
                    :class="['p-2 hover:bg-accent text-xs gap-1 flex items-center', inlineEdit === p.id ? 'text-maroon bg-accent' : 'hover:text-maroon text-muted-foreground']"
                    title="ویرایش سریع"
                  >
                    <Pencil class="h-3.5 w-3.5" />
                  </button>
                  <button type="button" @click="toggleHide(p.id)" class="p-2 hover:bg-accent hover:text-maroon">
                    <EyeOff v-if="hidden.has(p.id)" class="h-3.5 w-3.5" />
                    <Eye v-else class="h-3.5 w-3.5" />
                  </button>
                  <button type="button" @click="openEdit(p)" class="p-2 hover:bg-accent hover:text-maroon text-muted-foreground" title="ویرایش کامل">
                    <Layers class="h-3.5 w-3.5" />
                  </button>
                  <button type="button" @click="remove(p.id)" class="p-2 hover:bg-accent">
                    <Trash2 class="h-3.5 w-3.5 text-maroon" />
                  </button>
                </div>
              </td>
            </tr>

            <!-- Inline edit row -->
            <tr v-if="inlineEdit === p.id" class="bg-maroon/5 border-b border-maroon/20">
              <td colspan="6" class="px-5 py-4">
                <div class="flex flex-wrap items-end gap-4">
                  <label class="block">
                    <span class="text-xs text-muted-foreground uppercase tracking-wider block mb-1">نام محصول</span>
                    <input v-model="inlineForm.name" class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon w-48" />
                  </label>
                  <label class="block">
                    <span class="text-xs text-muted-foreground uppercase tracking-wider block mb-1">قیمت (تومان)</span>
                    <input type="number" v-model.number="inlineForm.price" class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon w-36" />
                  </label>
                  <label class="block">
                    <span class="text-xs text-muted-foreground uppercase tracking-wider block mb-1">دسته اصلی</span>
                    <select v-model="inlineForm.categoryId" class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon w-40">
                      <option value="">— انتخاب</option>
                      <option v-for="c in categoriesStore.roots" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
                    </select>
                  </label>
                  <label class="block">
                    <span class="text-xs text-muted-foreground uppercase tracking-wider block mb-1">زیردسته</span>
                    <select v-model="inlineForm.subCategoryId" class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon w-40">
                      <option value="">— انتخاب</option>
                      <option v-for="s in categoriesStore.children(inlineForm.categoryId || '')" :key="s.id" :value="s.id">{{ s.name }}</option>
                    </select>
                  </label>
                  <label class="block">
                    <span class="text-xs text-muted-foreground uppercase tracking-wider block mb-1">موجودی</span>
                    <select v-model="inlineForm.stock" class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon w-36">
                      <option value="in_stock">موجود</option>
                      <option value="low_stock">محدود</option>
                      <option value="out_of_stock">ناموجود</option>
                    </select>
                  </label>
                  <label class="block">
                    <span class="text-xs text-muted-foreground uppercase tracking-wider block mb-1">تعداد</span>
                    <input type="number" v-model.number="inlineForm.stockCount" min="0" class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon w-28" />
                  </label>
                  <div class="flex items-end gap-2 mr-auto">
                    <button type="button" @click="inlineEdit = null" class="border border-border px-4 py-2 text-xs hover:bg-accent">انصراف</button>
                    <button type="button" @click="saveInline" class="bg-maroon px-5 py-2 text-xs text-maroon-foreground hover:opacity-90 flex items-center gap-1.5">
                      <Check class="h-3.5 w-3.5" /> ذخیره
                    </button>
                    <button type="button" @click="openEdit(p)" class="border border-maroon px-4 py-2 text-xs text-maroon hover:bg-maroon hover:text-white transition-colors">
                      ویرایش کامل
                    </button>
                  </div>
                </div>
              </td>
            </tr>
          </template>
          <tr v-if="filtered.length === 0">
            <td colspan="6" class="px-6 py-16 text-center text-muted-foreground">هیچ محصولی یافت نشد</td>
          </tr>
        </tbody>
      </table>
    </div>
    </template><!-- /list -->

    <!-- ── GALLERY VIEW ── -->
    <template v-else-if="viewMode === 'gallery'">
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
        <div
          v-for="p in filtered"
          :key="p.id"
          :class="['border border-border overflow-hidden', hidden.has(p.id) ? 'opacity-40' : '']"
        >
          <div class="aspect-square bg-muted overflow-hidden relative">
            <img v-if="p.image" :src="p.image" alt="" class="w-full h-full object-cover" />
            <div v-else class="w-full h-full flex items-center justify-center text-muted-foreground text-xs">بدون تصویر</div>
            <div class="absolute top-2 right-2">
              <span v-if="p.type === 'coffee'" class="bg-maroon text-white text-[10px] px-1.5 py-0.5">{{ p.roast }}</span>
              <span v-else class="bg-foreground text-background text-[10px] px-1.5 py-0.5">اکسسوری</span>
            </div>
          </div>
          <div class="p-3">
            <div class="font-medium text-sm truncate">{{ p.name }}</div>
            <div class="text-xs text-muted-foreground mt-0.5 truncate">{{ catName(p.categoryId) }}</div>
            <div class="text-maroon text-sm font-medium mt-2">{{ formatPrice(p.price) }}</div>
            <div class="mt-3 flex items-center gap-1">
              <button @click="openEdit(p)" class="flex-1 border border-border py-1.5 text-xs hover:bg-accent text-center transition-colors">ویرایش</button>
              <button
                @click="toggleHide(p.id)"
                :class="['p-1.5 border border-border hover:bg-accent transition-colors', hidden.has(p.id) ? 'text-maroon' : 'text-muted-foreground']"
              >
                <EyeOff v-if="hidden.has(p.id)" class="h-3.5 w-3.5" />
                <Eye v-else class="h-3.5 w-3.5" />
              </button>
            </div>
          </div>
        </div>
        <div v-if="filtered.length === 0" class="col-span-full border border-dashed border-border p-16 text-center text-sm text-muted-foreground">
          هیچ محصولی یافت نشد
        </div>
      </div>
    </template>

    <!-- ── KANBAN VIEW ── -->
    <template v-else-if="viewMode === 'kanban'">
      <div class="flex gap-4 overflow-x-auto pb-6" style="min-height:420px">
        <div v-for="col in kanbanColumns" :key="col.id" class="flex-shrink-0 w-60">
          <div class="flex flex-col h-full border border-border">
            <div class="border-b border-border px-4 py-3 flex items-center justify-between bg-muted/40">
              <span class="text-xs font-medium">{{ col.name }}</span>
              <span class="text-xs text-muted-foreground border border-border px-1.5 py-0.5 bg-background">{{ col.products.length }}</span>
            </div>
            <div class="p-2 space-y-2 flex-1">
              <div
                v-for="p in col.products"
                :key="p.id"
                :class="['bg-background border border-border p-3 cursor-pointer hover:border-maroon/40 transition-colors', hidden.has(p.id) ? 'opacity-40' : '']"
                @click="openEdit(p)"
              >
                <div class="flex items-center gap-2">
                  <img v-if="p.image" :src="p.image" alt="" class="h-10 w-10 object-cover shrink-0" />
                  <div v-else class="h-10 w-10 bg-muted shrink-0 flex items-center justify-center text-[10px] text-muted-foreground">بدون</div>
                  <div class="min-w-0 flex-1">
                    <div class="text-xs font-medium truncate">{{ p.name }}</div>
                    <div class="text-maroon text-xs mt-0.5">{{ formatPrice(p.price) }}</div>
                    <div class="text-[10px] text-muted-foreground mt-0.5">{{ subCatName(p.subCategoryId) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="kanbanColumns.length === 0" class="flex-1 border border-dashed border-border p-16 text-center text-sm text-muted-foreground">
          هیچ محصولی یافت نشد
        </div>
      </div>
    </template>

    <!-- ── TREE VIEW ── -->
    <template v-else-if="viewMode === 'tree'">
      <div class="border border-border divide-y divide-border">
        <div v-for="col in kanbanColumns" :key="col.id">
          <div
            class="flex items-center gap-3 px-5 py-3.5 cursor-pointer hover:bg-accent/30 bg-muted/20"
            @click="toggleGroup(col.id)"
          >
            <ChevronDown :class="['h-4 w-4 text-muted-foreground transition-transform shrink-0', expandedGroups.has(col.id) ? '' : '-rotate-90']" />
            <FolderOpen class="h-4 w-4 text-maroon shrink-0" />
            <span class="text-sm font-medium">{{ col.name }}</span>
            <span class="mr-auto text-xs text-muted-foreground border border-border px-1.5 py-0.5 bg-background">{{ col.products.length }} محصول</span>
          </div>
          <div v-if="expandedGroups.has(col.id)" class="divide-y divide-border/40">
            <div
              v-for="p in col.products"
              :key="p.id"
              :class="['flex items-center gap-4 px-5 py-3 pr-14 hover:bg-accent/20 transition-colors', hidden.has(p.id) ? 'opacity-40' : '']"
            >
              <img v-if="p.image" :src="p.image" alt="" class="h-9 w-9 object-cover shrink-0" />
              <div v-else class="h-9 w-9 bg-muted shrink-0" />
              <div class="flex-1 min-w-0">
                <div class="text-sm font-medium truncate">{{ p.name }}</div>
                <div class="text-xs text-muted-foreground">{{ catName(p.categoryId) }}{{ p.subCategoryId ? ' · ' + subCatName(p.subCategoryId) : '' }}</div>
              </div>
              <div class="text-sm text-maroon shrink-0">{{ formatPrice(p.price) }}</div>
              <div class="flex gap-1 shrink-0">
                <button @click="openEdit(p)" class="p-1.5 hover:bg-accent text-muted-foreground hover:text-foreground" title="ویرایش">
                  <Layers class="h-3.5 w-3.5" />
                </button>
                <button @click="toggleHide(p.id)" :class="['p-1.5 hover:bg-accent', hidden.has(p.id) ? 'text-maroon' : 'text-muted-foreground hover:text-foreground']">
                  <EyeOff v-if="hidden.has(p.id)" class="h-3.5 w-3.5" />
                  <Eye v-else class="h-3.5 w-3.5" />
                </button>
                <button @click="remove(p.id)" class="p-1.5 hover:bg-accent text-muted-foreground hover:text-maroon">
                  <Trash2 class="h-3.5 w-3.5" />
                </button>
              </div>
            </div>
          </div>
        </div>
        <div v-if="kanbanColumns.length === 0" class="p-16 text-center text-sm text-muted-foreground">
          هیچ محصولی یافت نشد
        </div>
      </div>
    </template>

    <!-- ── REPORT VIEW ── -->
    <template v-else-if="viewMode === 'report'">
      <div class="space-y-6 max-w-4xl">
        <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div
            v-for="stat in [
              { label: 'کل محصولات', value: reportStats.total },
              { label: 'میانگین قیمت', value: formatPrice(reportStats.avgPrice) },
              { label: 'بیشترین قیمت', value: formatPrice(reportStats.maxPrice) },
            ]"
            :key="stat.label"
            class="border border-border p-5"
          >
            <div class="text-xs uppercase tracking-widest text-muted-foreground">{{ stat.label }}</div>
            <div class="mt-2 text-2xl font-light text-maroon">{{ stat.value }}</div>
          </div>
        </div>
        <div v-if="reportStats.byCategory.length > 0" class="border border-border p-6">
          <div class="text-xs uppercase tracking-widest text-muted-foreground mb-5">دسته‌های اصلی</div>
          <div class="space-y-4">
            <div v-for="c in reportStats.byCategory" :key="c.name" class="flex items-center gap-4">
              <span class="text-sm w-28 truncate">{{ c.icon }} {{ c.name }}</span>
              <div class="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                <div class="h-full bg-maroon rounded-full transition-all" :style="`width:${c.max ? (c.count/c.max*100) : 0}%`" />
              </div>
              <span class="text-xs text-muted-foreground w-6 text-left">{{ c.count }}</span>
            </div>
          </div>
        </div>
        <div v-if="reportStats.bySubCat.length > 0" class="border border-border p-6">
          <div class="text-xs uppercase tracking-widest text-muted-foreground mb-5">زیردسته‌ها</div>
          <div class="space-y-4">
            <div v-for="s in reportStats.bySubCat" :key="s.name" class="flex items-center gap-4">
              <span class="text-sm w-28 truncate">{{ s.name }}</span>
              <div class="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                <div class="h-full bg-maroon rounded-full transition-all" :style="`width:${s.max ? (s.count/s.max*100) : 0}%`" />
              </div>
              <span class="text-xs text-muted-foreground w-6 text-left">{{ s.count }}</span>
            </div>
          </div>
        </div>
        <div class="border border-border p-6">
          <div class="text-xs uppercase tracking-widest text-muted-foreground mb-5">مقایسه قیمت محصولات</div>
          <div class="space-y-2.5">
            <div v-for="p in [...list].sort((a,b) => b.price - a.price)" :key="p.id" class="flex items-center gap-3">
              <span class="text-xs w-32 truncate">{{ p.name }}</span>
              <div class="flex-1 h-1.5 bg-muted rounded-full overflow-hidden">
                <div class="h-full bg-maroon/70 rounded-full" :style="`width:${(p.price/reportStats.maxPrice*100)}%`" />
              </div>
              <span class="text-xs text-maroon w-24 text-left">{{ formatPrice(p.price) }}</span>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Drawer (full edit) -->
    <template v-if="editState.mode !== 'closed'">
      <div class="fixed inset-0 z-40 bg-foreground/40 backdrop-blur-sm" @click="editState = { mode: 'closed' }" />
      <aside class="fixed bottom-0 left-0 top-0 z-50 flex w-full max-w-2xl flex-col border-l border-maroon/30 bg-background">
        <header class="flex items-center justify-between border-b border-border p-5">
          <div>
            <div class="flex items-center gap-2">
              <div class="text-xs uppercase tracking-widest text-maroon">{{ editState.mode === "edit" ? "ویرایش" : "ایجاد" }}</div>
              <span v-if="selectedRootCat" class="rounded border border-border px-2 py-0.5 text-xs text-muted-foreground">
                {{ selectedRootCat.icon }} {{ selectedRootCat.name }}
              </span>
            </div>
            <h2 class="mt-1 text-xl font-light">{{ editState.mode === "edit" ? form.name : "محصول جدید" }}</h2>
          </div>
          <button type="button" @click="editState = { mode: 'closed' }" class="p-2 hover:bg-accent">
            <X class="h-4 w-4" />
          </button>
        </header>

        <!-- Template picker -->
        <div v-if="templatesStore.templates.length > 0" class="border-b border-border bg-muted/30 px-5 py-3">
          <div class="flex items-center gap-3">
            <Layers class="h-4 w-4 shrink-0 text-maroon" />
            <select
              :value="form.templateId ?? ''"
              @change="(e) => { const v = e.target.value; if (v) applyTemplate(v); else { form.templateId = undefined; form.customAttributes = {}; } }"
              class="flex-1 border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon"
            >
              <option value="">بدون قالب — تنظیم دستی</option>
              <option v-for="t in templatesStore.templates" :key="t.id" :value="t.id">{{ t.name }}</option>
            </select>
            <span v-if="form.templateId" class="text-xs text-maroon shrink-0">✓ قالب اعمال شد</span>
          </div>
        </div>

        <!-- Tabs -->
        <div class="flex border-b border-border overflow-x-auto">
          <button
            v-for="t in activeTabs"
            :key="t.id"
            type="button"
            @click="drawerTab = t.id"
            :class="[
              'shrink-0 flex flex-1 items-center justify-center px-4 py-3 text-xs transition-colors',
              drawerTab === t.id ? 'border-b-2 border-maroon text-maroon' : 'text-muted-foreground hover:text-foreground',
            ]"
          >
            {{ t.label }}
          </button>
        </div>

        <form @submit="submitForm" class="flex flex-1 flex-col overflow-y-auto">
          <div class="space-y-5 p-5">

            <!-- ── Basic tab ── -->
            <template v-if="drawerTab === 'basic'">
              <label class="block">
                <span class="field-label">نام محصول *</span>
                <input required v-model="form.name" class="field-input" />
              </label>
              <!-- Category selectors -->
              <div class="grid grid-cols-2 gap-4">
                <label class="block">
                  <span class="field-label">دسته اصلی *</span>
                  <select required v-model="form.categoryId" class="field-input" @change="form.subCategoryId = ''">
                    <option value="">— انتخاب دسته</option>
                    <option v-for="c in categoriesStore.roots" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
                  </select>
                </label>
                <label class="block">
                  <span class="field-label">زیردسته</span>
                  <select v-model="form.subCategoryId" class="field-input">
                    <option value="">— انتخاب زیردسته</option>
                    <option v-for="s in selectedCatChildren" :key="s.id" :value="s.id">{{ s.icon }} {{ s.name }}</option>
                  </select>
                </label>
              </div>
              <!-- Dynamic attributes from category schema -->
              <template v-if="selectedCatAttrs.length > 0">
                <div class="border-t border-border pt-4 mt-2">
                  <div class="text-xs uppercase tracking-widest text-muted-foreground mb-3">ویژگی‌های دسته‌بندی</div>
                  <div class="grid grid-cols-2 gap-4">
                    <label v-for="attr in selectedCatAttrs" :key="attr.key" class="block">
                      <span class="field-label">{{ attr.label }}</span>
                      <select v-if="attr.type === 'select' && attr.options?.length" v-model="form.attrs[attr.key]" class="field-input">
                        <option value="">— انتخاب</option>
                        <option v-for="opt in attr.options" :key="opt" :value="opt">{{ opt }}</option>
                      </select>
                      <input v-else-if="attr.type === 'number'" type="number" v-model.number="form.attrs[attr.key]" class="field-input" />
                      <input v-else v-model="form.attrs[attr.key]" class="field-input" />
                    </label>
                  </div>
                </div>
              </template>
              <div class="grid grid-cols-2 gap-4">
                <label class="block">
                  <span class="field-label">قیمت پایه (تومان) *</span>
                  <input required type="number" v-model.number="form.price" class="field-input" />
                </label>
                <label class="block">
                  <span class="field-label">یادداشت‌های طعم / برند</span>
                  <input v-model="notesText" placeholder="جدا شده با ،" class="field-input" />
                </label>
              </div>
              <label class="block">
                <span class="field-label">توضیحات</span>
                <textarea v-model="form.description" rows="3" class="field-input resize-none" />
              </label>
            </template>

            <!-- ── Media tab ── -->
            <template v-if="drawerTab === 'media'">
              <ImageUploader v-model="form.image" label="تصویر اصلی" />
              <div>
                <div class="mb-4 flex items-center justify-between">
                  <span class="text-xs uppercase tracking-widest text-maroon">گالری تصاویر ({{ form.gallery.length }})</span>
                  <button type="button" @click="addGalleryImg" class="text-xs text-maroon hover:underline">+ افزودن</button>
                </div>
                <div class="space-y-3">
                  <div v-for="(img, i) in form.gallery" :key="i" class="flex items-start gap-2">
                    <div class="flex-1">
                      <ImageUploader :model-value="img" label="" @update:model-value="setGalleryImg(i, $event)" />
                    </div>
                    <button type="button" @click="removeGalleryImg(i)" class="text-muted-foreground hover:text-maroon mt-1"><X class="h-4 w-4" /></button>
                  </div>
                </div>
              </div>
            </template>

            <!-- ── Variants tab (only if category hasVariants) ── -->
            <template v-if="drawerTab === 'variants'">
              <div>
                <div class="mb-4 flex items-center justify-between">
                  <span class="text-xs uppercase tracking-widest text-maroon">{{ selectedRootCat?.variantLabel || 'واریانت‌ها' }} ({{ form.weights?.length }})</span>
                  <button type="button" @click="addWeight" class="text-xs text-maroon hover:underline">+ افزودن</button>
                </div>
                <div class="space-y-2">
                  <div v-for="(w, i) in form.weights" :key="i" class="grid grid-cols-[1fr_120px_32px] items-center gap-2">
                    <input v-model="w.label" placeholder="مثلاً: ۲۵۰ گرم" class="field-input" />
                    <input type="number" step="0.05" v-model.number="w.multiplier" class="field-input" />
                    <button type="button" @click="removeWeight(i)" class="text-muted-foreground hover:text-maroon"><Trash2 class="h-4 w-4" /></button>
                  </div>
                </div>
              </div>
              <label v-if="selectedCatHasGrinds" class="block">
                <span class="field-label">انواع آسیاب (با ، جدا کنید)</span>
                <input v-model="grindsText" class="field-input" />
              </label>
            </template>

            <!-- ── Specs tab ── -->
            <template v-if="drawerTab === 'specs'">
              <div class="mb-4 flex items-center justify-between">
                <span class="text-xs uppercase tracking-widest text-maroon">مشخصات فنی</span>
                <button type="button" @click="addSpec" class="text-xs text-maroon hover:underline">+ افزودن</button>
              </div>
              <div class="space-y-3">
                <div v-for="(spec, i) in form.specs" :key="i" class="grid grid-cols-[1fr_1fr_32px] items-center gap-2">
                  <input v-model="spec.label" placeholder="مثلاً: ظرفیت" class="field-input" />
                  <input v-model="spec.value" placeholder="مثلاً: ۳۵۰ میلی‌لیتر" class="field-input" />
                  <button type="button" @click="removeSpec(i)" class="text-muted-foreground hover:text-maroon"><Trash2 class="h-4 w-4" /></button>
                </div>
                <div v-if="!form.specs?.length" class="text-center text-xs text-muted-foreground py-6 border border-dashed border-border">کلیک کنید و مشخصات اضافه کنید</div>
              </div>
            </template>

            <!-- ── FAQs tab ── -->
            <template v-if="drawerTab === 'faqs'">
              <div class="mb-4 flex items-start justify-between gap-3">
                <div>
                  <span class="text-xs uppercase tracking-widest text-maroon">سوالات تخصصی محصول</span>
                  <p class="mt-1 text-xs text-muted-foreground leading-5">
                    این سوالات فقط برای این محصول نمایش داده می‌شوند — بالاتر از سوالات عمومی.
                  </p>
                </div>
                <button type="button" @click="addFaq" class="shrink-0 text-xs text-maroon hover:underline whitespace-nowrap">+ افزودن سوال</button>
              </div>
              <div class="space-y-4">
                <div v-for="(faq, i) in form.productFaqs" :key="i" class="border border-border p-4 space-y-3">
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-muted-foreground">سوال {{ i + 1 }}</span>
                    <button type="button" @click="removeFaq(i)" class="text-maroon hover:opacity-70">
                      <Trash2 class="h-3.5 w-3.5" />
                    </button>
                  </div>
                  <label class="block">
                    <span class="field-label">سوال</span>
                    <input v-model="faq.q" placeholder="سوال را اینجا بنویسید..." class="field-input" />
                  </label>
                  <label class="block">
                    <span class="field-label">پاسخ</span>
                    <textarea v-model="faq.a" rows="3" placeholder="پاسخ کامل را اینجا بنویسید..." class="field-input resize-none" />
                  </label>
                </div>
              </div>
              <div v-if="!form.productFaqs?.length" class="border border-dashed border-border p-10 text-center text-xs text-muted-foreground">
                سوال تخصصی ندارد. با کلیک «+ افزودن سوال» اضافه کنید.
              </div>
            </template>

          </div>

          <footer class="mt-auto flex items-center justify-end gap-3 border-t border-border bg-muted/30 p-5">
            <button type="button" @click="editState = { mode: 'closed' }" class="border border-border px-5 py-2.5 text-sm hover:bg-accent">انصراف</button>
            <button type="submit" class="bg-maroon px-6 py-2.5 text-sm text-maroon-foreground hover:opacity-90">
              {{ editState.mode === "edit" ? "ذخیره تغییرات" : "ایجاد محصول" }}
            </button>
          </footer>
        </form>
      </aside>
    </template>
  </div>
</template>

<style scoped>
.field-label {
  display: block;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--muted-foreground);
}
.field-input {
  display: block;
  width: 100%;
  border: 1px solid var(--color-border);
  background-color: var(--color-background);
  padding: 0.625rem 0.75rem;
  font-size: 0.875rem;
  outline: none;
  margin-top: 0.375rem;
}
.field-input:focus { border-color: var(--color-maroon); }
</style>
