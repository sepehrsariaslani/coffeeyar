<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useRoute } from "vue-router";
import { SlidersHorizontal, X, ChevronDown } from "lucide-vue-next";
import TheLayout from "@/components/site/TheLayout.vue";
import SectionHeader from "@/components/SectionHeader.vue";
import ProductCard from "@/components/ProductCard.vue";
import { useProductsStore } from "@/stores/products.js";
import { useCategoriesStore } from "@/stores/categories.js";

const route = useRoute();
const productsStore = useProductsStore();
const categoriesStore = useCategoriesStore();

const activeTab = ref("");
const open = ref(false);
const sortBy = ref("default");
const selectedSubCat = ref("");

const sortOptions = [
  { value: "default", label: "پیش‌فرض" },
  { value: "price_asc", label: "ارزان‌ترین" },
  { value: "price_desc", label: "گران‌ترین" },
  { value: "newest", label: "جدیدترین" },
];

const currentRootCat = computed(() =>
  categoriesStore.roots.find((r) => r.id === activeTab.value)
);

const currentSubCats = computed(() =>
  activeTab.value ? categoriesStore.children(activeTab.value) : []
);

watch(activeTab, () => {
  selectedSubCat.value = "";
  open.value = false;
  loadProducts();
});

watch(sortBy, loadProducts);
watch(selectedSubCat, loadProducts);

async function loadProducts() {
  const cat = selectedSubCat.value
    ? categoriesStore.getById(selectedSubCat.value)
    : currentRootCat.value;
  await productsStore.fetchProducts({
    category_slug: cat?.slug || "",
    sort: sortBy.value,
    page_size: 48,
  });
}

const activeCount = computed(() => {
  let n = selectedSubCat.value ? 1 : 0;
  return n;
});

function clearAll() {
  selectedSubCat.value = "";
  sortBy.value = "default";
  loadProducts();
}

function switchTab(id) {
  activeTab.value = id;
  clearAll();
}

onMounted(async () => {
  await categoriesStore.fetchCategories();
  const catSlug = route.query.category || "";
  if (catSlug) {
    const cat = categoriesStore.getBySlug(catSlug);
    if (cat) activeTab.value = cat.parent_id ? cat.parent_id : cat.id;
  } else if (categoriesStore.roots.length) {
    activeTab.value = categoriesStore.roots[0]?.id || "";
  }
  await loadProducts();
});
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
            v-if="currentSubCats.length"
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

          <button v-if="activeCount > 0 || sortBy !== 'default'" type="button" @click="clearAll"
            class="text-xs text-muted-foreground hover:text-maroon font-[Vazirmatn]">
            پاک کردن همه
          </button>

          <div class="mr-auto text-sm text-muted-foreground font-[Vazirmatn]">
            {{ productsStore.total }} محصول
          </div>
        </div>

        <!-- Filter Panel -->
        <div v-if="open && currentSubCats.length" class="border-b border-[#E8E4DE] bg-[#FAFAF8] py-8">
          <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
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
          </div>
        </div>

        <!-- Loading -->
        <div v-if="productsStore.loading" class="py-24 text-center text-muted-foreground font-[Vazirmatn]">
          در حال بارگذاری محصولات...
        </div>
        <!-- Empty -->
        <div v-else-if="productsStore.products.length === 0" class="py-24 text-center text-muted-foreground font-[Vazirmatn]">
          <p class="text-lg">محصولی با این فیلترها پیدا نشد.</p>
          <button type="button" @click="clearAll" class="mt-4 text-sm text-maroon hover:underline">پاک کردن فیلترها</button>
        </div>
        <!-- Products Grid -->
        <div v-else class="products-grid">
          <ProductCard v-for="p in productsStore.products" :key="p.id" :product="p" />
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
