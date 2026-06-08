<script setup>
import { ref, computed, watch } from "vue";
import { SlidersHorizontal, X, ChevronDown } from "lucide-vue-next";
import TheLayout from "@/components/site/TheLayout.vue";
import SectionHeader from "@/components/SectionHeader.vue";
import ProductCard from "@/components/ProductCard.vue";
import { products } from "@/lib/data.js";
import { useCategoriesStore } from "@/stores/categories.js";

const categoriesStore = useCategoriesStore();

const allPrices = products.map((p) => p.price);
const maxPossible = Math.max(...allPrices, 1);
const minPossible = Math.min(...allPrices, 0);

const activeTab = ref(categoriesStore.roots[0]?.id || "");
const open = ref(false);
const sortBy = ref("default");
const priceMin = ref(minPossible);
const priceMax = ref(maxPossible);
const selectedAttrs = ref({});

const sortOptions = [
  { value: "default", label: "پیش‌فرض" },
  { value: "price_asc", label: "ارزان‌ترین" },
  { value: "price_desc", label: "گران‌ترین" },
  { value: "name_asc", label: "نام (الف تا ی)" },
];

const currentRootCat = computed(() =>
  categoriesStore.roots.find((r) => r.id === activeTab.value)
);

const currentSubCats = computed(() =>
  activeTab.value ? categoriesStore.children(activeTab.value) : []
);

const selectedSubCat = ref("");

watch(activeTab, () => {
  selectedSubCat.value = "";
  selectedAttrs.value = {};
  open.value = false;
  priceMin.value = minPossible;
  priceMax.value = maxPossible;
});

function toggle(obj, key, val) {
  if (!obj[key]) obj[key] = [];
  const arr = obj[key];
  const idx = arr.indexOf(val);
  if (idx !== -1) arr.splice(idx, 1); else arr.push(val);
}

function sortList(list) {
  const copy = [...list];
  if (sortBy.value === "price_asc") return copy.sort((a, b) => a.price - b.price);
  if (sortBy.value === "price_desc") return copy.sort((a, b) => b.price - a.price);
  if (sortBy.value === "name_asc") return copy.sort((a, b) => a.name.localeCompare(b.name, "fa"));
  return copy;
}

const tabProducts = computed(() =>
  products.filter((p) => p.categoryId === activeTab.value)
);

const filtered = computed(() => {
  const base = tabProducts.value.filter((p) => {
    const subOk = !selectedSubCat.value || p.subCategoryId === selectedSubCat.value;
    const priceOk = p.price >= priceMin.value && p.price <= priceMax.value;
    const attrsOk = Object.entries(selectedAttrs.value).every(([key, vals]) => {
      if (!vals || vals.length === 0) return true;
      const pVal = p.attrs?.[key];
      return pVal && vals.includes(pVal);
    });
    return subOk && priceOk && attrsOk;
  });
  return sortList(base);
});

const activeCount = computed(() => {
  let n = selectedSubCat.value ? 1 : 0;
  if (priceMin.value > minPossible || priceMax.value < maxPossible) n++;
  Object.values(selectedAttrs.value).forEach((arr) => { n += (arr || []).length; });
  return n;
});

function clearAll() {
  selectedSubCat.value = "";
  selectedAttrs.value = {};
  priceMin.value = minPossible;
  priceMax.value = maxPossible;
  sortBy.value = "default";
}

function switchTab(id) {
  activeTab.value = id;
  clearAll();
}

function formatPriceShort(n) {
  if (n >= 1000000) return (n / 1000000).toFixed(1).replace(".0", "") + "م";
  if (n >= 1000) return Math.round(n / 1000) + "ه";
  return String(n);
}

function getAttrValues(key) {
  return [...new Set(tabProducts.value.map((p) => p.attrs?.[key]).filter(Boolean))];
}
</script>

<template>
  <TheLayout>
    <div class="border-b border-border">
      <SectionHeader title="محصولات" tag="کاتالوگ" />
      <p class="px-[5vw] pb-6 text-sm text-muted-foreground max-w-xl">
        مجموعه‌ای از محصولات منتخب نوار. هر انتخاب داستانی دارد.
      </p>
      <!-- Tabs (one per root category) -->
      <div class="flex border-t border-border px-[5vw]">
        <button
          v-for="cat in categoriesStore.roots"
          :key="cat.id"
          type="button"
          @click="switchTab(cat.id)"
          :class="['px-6 py-4 text-sm transition-colors font-[Vazirmatn]', activeTab === cat.id ? 'border-b-2 border-maroon text-maroon' : 'text-muted-foreground hover:text-foreground']"
        >
          {{ cat.icon }} {{ cat.name }}
        </button>
      </div>
    </div>

    <section>
      <div class="px-[5vw] py-6">
        <!-- Filter + Sort Bar -->
        <div class="flex flex-wrap items-center gap-3 border-b border-[#E8E4DE] pb-6">
          <button
            type="button"
            @click="open = !open"
            :class="['flex items-center gap-2 border px-5 py-2.5 text-sm transition-colors font-[Vazirmatn]',
              open || activeCount > 0 ? 'border-maroon bg-maroon text-white' : 'border-[#E8E4DE] hover:border-maroon']"
          >
            <SlidersHorizontal class="h-4 w-4" />
            فیلتر
            <span v-if="activeCount > 0" class="flex h-5 w-5 items-center justify-center rounded-full bg-white text-xs text-maroon">
              {{ activeCount }}
            </span>
          </button>

          <!-- Sort dropdown -->
          <div class="relative font-[Vazirmatn]">
            <select v-model="sortBy"
              class="appearance-none border border-[#E8E4DE] bg-background py-2.5 pr-4 pl-8 text-sm outline-none focus:border-maroon hover:border-maroon transition-colors cursor-pointer">
              <option v-for="s in sortOptions" :key="s.value" :value="s.value">{{ s.label }}</option>
            </select>
            <ChevronDown class="pointer-events-none absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-muted-foreground" />
          </div>

          <!-- Active filter pills -->
          <button v-if="selectedSubCat" type="button" @click="selectedSubCat = ''"
            class="flex items-center gap-1.5 border border-maroon/50 bg-maroon/5 px-3 py-1.5 text-xs text-maroon font-[Vazirmatn]">
            زیردسته: {{ categoriesStore.getById(selectedSubCat)?.name }}
            <X class="h-3 w-3" />
          </button>
          <template v-for="(vals, key) in selectedAttrs" :key="key">
            <button v-for="val in (vals || [])" :key="val" type="button" @click="toggle(selectedAttrs, key, val)"
              class="flex items-center gap-1.5 border border-maroon/50 bg-maroon/5 px-3 py-1.5 text-xs text-maroon font-[Vazirmatn]">
              {{ currentRootCat?.attributes?.find(a => a.key === key)?.label || key }}: {{ val }}
              <X class="h-3 w-3" />
            </button>
          </template>
          <button v-if="priceMin > minPossible || priceMax < maxPossible" type="button"
            @click="priceMin = minPossible; priceMax = maxPossible"
            class="flex items-center gap-1.5 border border-maroon/50 bg-maroon/5 px-3 py-1.5 text-xs text-maroon font-[Vazirmatn]">
            قیمت: {{ formatPriceShort(priceMin) }} – {{ formatPriceShort(priceMax) }}
            <X class="h-3 w-3" />
          </button>

          <button v-if="activeCount > 0 || sortBy !== 'default'" type="button" @click="clearAll"
            class="text-xs text-muted-foreground hover:text-maroon font-[Vazirmatn]">
            پاک کردن همه
          </button>

          <div class="mr-auto text-sm text-muted-foreground font-[Vazirmatn]">
            {{ filtered.length }} محصول
          </div>
        </div>

        <!-- Filter Panel -->
        <div v-if="open" class="border-b border-[#E8E4DE] bg-[#FAFAF8] py-8">
          <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
            <!-- Sub-category -->
            <div v-if="currentSubCats.length > 0">
              <div class="mb-4 text-xs uppercase tracking-widest text-maroon font-[Vazirmatn]">زیردسته</div>
              <div class="flex flex-col gap-2.5">
                <label v-for="sub in currentSubCats" :key="sub.id" class="flex cursor-pointer items-center gap-3 text-sm font-[Vazirmatn]">
                  <button type="button" @click="selectedSubCat = selectedSubCat === sub.id ? '' : sub.id"
                    :class="['h-4 w-4 border transition-colors shrink-0', selectedSubCat === sub.id ? 'border-maroon bg-maroon' : 'border-[#E8E4DE] hover:border-maroon']" />
                  {{ sub.icon }} {{ sub.name }}
                </label>
              </div>
            </div>

            <!-- Dynamic attribute filters from category schema -->
            <div v-for="attr in (currentRootCat?.attributes || [])" :key="attr.key">
              <div class="mb-4 text-xs uppercase tracking-widest text-maroon font-[Vazirmatn]">{{ attr.label }}</div>
              <div class="flex flex-col gap-2.5">
                <label v-for="val in getAttrValues(attr.key)" :key="val" class="flex cursor-pointer items-center gap-3 text-sm font-[Vazirmatn]">
                  <button type="button" @click="toggle(selectedAttrs, attr.key, val)"
                    :class="['h-4 w-4 border transition-colors shrink-0', (selectedAttrs[attr.key] || []).includes(val) ? 'border-maroon bg-maroon' : 'border-[#E8E4DE] hover:border-maroon']" />
                  {{ val }}
                </label>
                <span v-if="getAttrValues(attr.key).length === 0" class="text-xs text-muted-foreground">ارزشی ثبت نشده</span>
              </div>
            </div>

            <!-- Price Range -->
            <div>
              <div class="mb-4 text-xs uppercase tracking-widest text-maroon font-[Vazirmatn]">بازه قیمت (تومان)</div>
              <div class="space-y-3">
                <div>
                  <label class="text-xs text-muted-foreground font-[Vazirmatn]">از</label>
                  <input type="range" v-model.number="priceMin"
                    :min="minPossible" :max="priceMax - 10000" step="10000"
                    class="mt-1 w-full accent-maroon" />
                  <div class="mt-1 text-xs text-maroon font-[Vazirmatn]">{{ priceMin.toLocaleString("fa-IR") }}</div>
                </div>
                <div>
                  <label class="text-xs text-muted-foreground font-[Vazirmatn]">تا</label>
                  <input type="range" v-model.number="priceMax"
                    :min="priceMin + 10000" :max="maxPossible" step="10000"
                    class="mt-1 w-full accent-maroon" />
                  <div class="mt-1 text-xs text-maroon font-[Vazirmatn]">{{ priceMax.toLocaleString("fa-IR") }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Products Grid -->
        <div v-if="filtered.length === 0" class="py-24 text-center text-muted-foreground font-[Vazirmatn]">
          <p class="text-lg">محصولی با این فیلترها پیدا نشد.</p>
          <button type="button" @click="clearAll" class="mt-4 text-sm text-maroon hover:underline">پاک کردن فیلترها</button>
        </div>
        <div v-else class="products-grid">
          <ProductCard v-for="p in filtered" :key="p.id" :product="p" />
        </div>
      </div>
    </section>
  </TheLayout>
</template>

<style scoped>
.products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2.5rem 1.5rem;
  padding: 2rem 0 5rem;
}
@media (max-width: 768px) {
  .products-grid { grid-template-columns: repeat(2, 1fr); gap: 1.5rem 1rem; }
}
</style>
