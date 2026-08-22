<script setup>
import { ref, computed, watch } from "vue";
import { useRoute, RouterLink } from "vue-router";
import { ChevronDown, Star } from "lucide-vue-next";
import TheLayout from "@/components/site/TheLayout.vue";
import FlavorTriangle from "@/components/site/FlavorTriangle.vue";
import ProfileChart from "@/components/site/ProfileChart.vue";
import { useProductProfilesStore } from "@/stores/productProfiles.js";
import AppSelect from "@/components/AppSelect.vue";
import ProductGallery from "@/components/ProductGallery.vue";
import ProductCard from "@/components/ProductCard.vue";
import SectionHeader from "@/components/SectionHeader.vue";
import { useProductsStore } from "@/stores/products.js";
import { useCartStore } from "@/stores/cart.js";
import { useReviewsStore } from "@/stores/reviews.js";
import { useWishlistStore } from "@/stores/wishlist.js";
import { toFa } from "@/lib/utils.js";
import { useSeo } from "@/composables/useSeo.js";
import { useJsonLd } from "@/composables/useJsonLd.js";
import { useProductGlobalFaqsStore } from "@/stores/productGlobalFaqs.js";

function formatPrice(n) {
  if (!n) return "۰";
  return n.toLocaleString("fa-IR");
}

const route = useRoute();
const cartStore = useCartStore();
const reviewsStore = useReviewsStore();
const wishlistStore = useWishlistStore();
const profilesStore = useProductProfilesStore();
const productsStore = useProductsStore();

const productAssignment = computed(() =>
  product.value ? profilesStore.getAssignment(product.value.id) : null
);
const productProfile = computed(() =>
  productAssignment.value ? profilesStore.getProfile(productAssignment.value.profileId) : null
);

const product = computed(() => productsStore.currentProduct);

useSeo({
  title: computed(() => product.value?.name || product.value?.title),
  description: computed(() => product.value?.description?.slice(0, 155)),
  image: computed(() => product.value?.image),
});

const reviews = computed(() => reviewsStore.getReviews(route.params.id));
const avgRating = computed(() => reviewsStore.averageRating(route.params.id));

useJsonLd(() => {
  const p = product.value;
  if (!p) return null;
  const availability =
    p.stock === "out_of_stock"
      ? "https://schema.org/OutOfStock"
      : p.stock === "low_stock"
      ? "https://schema.org/LimitedAvailability"
      : "https://schema.org/InStock";
  const schema = {
    "@context": "https://schema.org/",
    "@type": "Product",
    name: p.name,
    description: p.description,
    image: p.gallery || [p.image],
    sku: p.id,
    brand: { "@type": "Brand", name: p.brand || "نوار" },
    offers: {
      "@type": "Offer",
      url: window.location.href,
      priceCurrency: "IRR",
      price: p.price * 10,
      availability,
      itemCondition: "https://schema.org/NewCondition",
    },
  };
  const avg = avgRating.value;
  const count = reviews.value.length;
  if (avg > 0 && count > 0) {
    schema.aggregateRating = {
      "@type": "AggregateRating",
      ratingValue: avg,
      reviewCount: count,
      bestRating: 5,
      worstRating: 1,
    };
  }
  return schema;
});

const reviewForm = ref({ name: "", rating: 5, text: "" });
const reviewSubmitted = ref(false);
const hoverStar = ref(0);

function submitReview() {
  if (!reviewForm.value.name.trim() || !reviewForm.value.text.trim()) return;
  reviewsStore.addReview(route.params.id, reviewForm.value);
  reviewForm.value = { name: "", rating: 5, text: "" };
  reviewSubmitted.value = true;
  setTimeout(() => (reviewSubmitted.value = false), 3000);
}

const isAccessory = computed(() => {
  const p = product.value;
  if (!p) return false;
  const slug = p.category_slug || "";
  const name = p.category_name || "";
  return !slug.includes("coffee") && !name.includes("قهوه") && (slug.includes("accessor") || slug.includes("equipment") || slug.includes("brewing") || p.type === "accessory");
});

const globalFaqsStore = useProductGlobalFaqsStore();
const globalFaqs = computed(() =>
  globalFaqsStore.getFaqsForType(isAccessory.value ? "accessory" : "coffee")
);

async function loadProduct(slug) {
  if (!slug || slug === "undefined") {
    productsStore.currentProduct = null;
    return;
  }

  await productsStore.fetchProduct(slug);
  await reviewsStore.fetchReviews(slug);
}

// The same component instance is reused when moving from one product to
// another, so react to the route param instead of relying on mount only.
watch(() => route.params.id, loadProduct, { immediate: true });

const related = computed(() =>
  productsStore.products
    .filter((p) => p.id !== productsStore.currentProduct?.id && p.category === product.value?.category)
    .slice(0, 4)
);

const selectedWeight = ref(0);
const selectedGrind = ref(0);
const activeImg = ref(0);
const openAcc = ref(null);
const added = ref(false);
const qty = ref(1);

const inlinePanelOpen = ref(false);
const inlineProfileId = ref("");
const inlineRatings = ref({});
const inlineSaved = ref(false);

const inlineProfile = computed(() =>
  inlineProfileId.value ? profilesStore.getProfile(inlineProfileId.value) : null
);

watch(inlineProfileId, (pid) => {
  if (!pid) { inlineRatings.value = {}; return; }
  const profile = profilesStore.getProfile(pid);
  if (!profile) return;
  const existing = productAssignment.value?.profileId === pid ? productAssignment.value.ratings : {};
  const fresh = {};
  profile.traits.forEach((t) => { fresh[t.id] = existing[t.id] ?? 5; });
  inlineRatings.value = fresh;
});

watch(inlinePanelOpen, (open) => {
  if (!open) return;
  const a = productAssignment.value;
  if (a) {
    inlineProfileId.value = a.profileId;
  }
});

function saveInlineAssignment() {
  if (!product.value || !inlineProfileId.value) return;
  profilesStore.setAssignment(product.value.id, inlineProfileId.value, inlineRatings.value);
  inlineSaved.value = true;
  setTimeout(() => { inlineSaved.value = false; inlinePanelOpen.value = false; }, 1500);
}

function removeInlineAssignment() {
  if (!product.value) return;
  profilesStore.removeAssignment(product.value.id);
  inlineProfileId.value = "";
  inlineRatings.value = {};
}

const variants = computed(() => product.value?.variants || []);
const grinds = computed(() => {
  const p = product.value;
  if (!p) return [];
  if (p.grinds?.length) return p.grinds;
  if (p.category_slug === "coffee") return ["دانه کامل", "اسپرسو", "موکاپات", "فرنچ پرس", "V60"];
  return [];
});
const gallery = computed(() => {
  const p = product.value;
  if (!p) return [];
  if (p.gallery?.length) return p.gallery;
  if (p.image) return [p.image];
  return [];
});
const stockStatus = computed(() => {
  const qty = product.value?.stock_qty ?? 0;
  if (qty <= 0) return "out_of_stock";
  if (qty <= 5) return "low_stock";
  return "in_stock";
});

const price = computed(() => {
  if (!product.value) return 0;
  if (variants.value.length && variants.value[selectedWeight.value]) {
    return variants.value[selectedWeight.value].price_toman || product.value.effective_price_toman || product.value.price_toman || 0;
  }
  return product.value.effective_price_toman || product.value.price_toman || 0;
});

function addToCart() {
  if (!product.value) return;
  const variant = variants.value[selectedWeight.value];
  cartStore.add({
    productId: product.value.id,
    name: product.value.name,
    image: product.value.image || product.value.gallery?.[0] || "",
    weight: variant?.label || "۱ عدد",
    grind: grinds.value[selectedGrind.value] || product.value.category_name || "",
    unitPrice: price.value,
    qty: qty.value,
  });
  added.value = true;
  setTimeout(() => (added.value = false), 2000);
}
</script>

<template>
  <TheLayout>
    <div v-if="productsStore.loading" class="mx-auto max-w-2xl px-6 py-32 text-center text-muted-foreground">
      در حال بارگذاری...
    </div>
    <div v-else-if="!product" class="mx-auto max-w-2xl px-6 py-32 text-center">
      <h1 class="text-3xl">محصول پیدا نشد</h1>
      <RouterLink to="/products" class="mt-6 inline-block text-maroon">بازگشت به محصولات</RouterLink>
    </div>

    <template v-else>
      <!-- Breadcrumb -->
      <nav class="px-[5vw] py-4 flex items-center gap-2 border-b border-[#E8E4DE] text-xs font-[Vazirmatn]">
        <RouterLink to="/" class="text-[#9e9890] hover:text-foreground transition-colors">خانه</RouterLink>
        <span class="text-[#C8C2BA]">·</span>
        <RouterLink to="/products" class="text-[#9e9890] hover:text-foreground transition-colors">محصولات</RouterLink>
        <span class="text-[#C8C2BA]">·</span>
        <span class="text-[#555]">{{ product.name }}</span>
      </nav>

      <!-- Product Main -->
      <section class="border-b border-border">
        <div class="mx-auto grid max-w-7xl gap-0 md:grid-cols-2">
          <!-- Gallery -->
          <div class="border-b border-border p-6 md:border-b-0 md:border-l md:p-0">
            <div class="flex flex-col gap-3 md:flex-row-reverse">
              <div class="flex-1 md:p-6">
                <ProductGallery
                  :image="gallery[activeImg] || product.image || ''"
                  :alt="product.name"
                  :badge="product.category_name"
                />
              </div>
            </div>
          </div>

          <!-- Info -->
          <div class="flex flex-col justify-center px-6 py-12 md:px-12 md:py-16">
            <div class="flex items-center gap-3 mb-4">
              <span class="text-xs uppercase tracking-[0.2em] text-maroon font-[Vazirmatn]">{{ product.category_name }}</span>
            </div>

            <h1 class="text-4xl font-light leading-tight mb-4">{{ product.name }}</h1>
            <p class="leading-7 text-muted-foreground mb-4">{{ product.description || product.short_description }}</p>

            <!-- Notes/tags -->
            <div v-if="product.notes?.length" class="flex flex-wrap gap-2 mb-6">
              <span
                v-for="note in product.notes" :key="note"
                class="border border-[#E8E4DE] px-3 py-1 text-xs text-muted-foreground font-[Vazirmatn]"
              >{{ note }}</span>
            </div>

            <div class="price-row">
              <span class="price-row__amount">{{ formatPrice(price) }}</span>
              <span class="price-row__unit">تومان</span>
            </div>

            <!-- Grind selector -->
            <div v-if="grinds.length" class="mt-5">
              <div class="picker-label">نوع آسیاب</div>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="(g, idx) in grinds" :key="g"
                  type="button" @click="selectedGrind = idx"
                  :class="['picker-chip', selectedGrind === idx ? 'picker-chip--active' : '']"
                >
                  {{ g }}
                </button>
              </div>
            </div>

            <!-- Qty selector -->
            <div class="mt-5">
              <div class="picker-label">تعداد</div>
              <div class="flex items-center gap-3">
                <button type="button" @click="qty = Math.max(1, qty - 1)"
                  class="flex h-10 w-10 items-center justify-center border border-[#E8E4DE] text-lg hover:border-maroon">−</button>
                <span class="min-w-[2rem] text-center font-[Vazirmatn]">{{ qty }}</span>
                <button type="button" @click="qty++"
                  class="flex h-10 w-10 items-center justify-center border border-[#E8E4DE] text-lg hover:border-maroon">+</button>
              </div>
            </div>

            <!-- Stock indicator -->
            <div class="mt-6 flex items-center gap-2 font-[Vazirmatn]">
              <template v-if="stockStatus === 'in_stock'">
                <span class="h-2 w-2 rounded-full bg-green-500 shrink-0"></span>
                <span class="text-xs text-green-700">موجود در انبار</span>
                <span v-if="product.stock_qty" class="text-xs text-muted-foreground">({{ product.stock_qty.toLocaleString('fa-IR') }} عدد)</span>
              </template>
              <template v-else-if="stockStatus === 'low_stock'">
                <span class="h-2 w-2 rounded-full bg-amber-500 shrink-0 animate-pulse"></span>
                <span class="text-xs text-amber-700 font-medium">موجودی محدود</span>
              </template>
              <template v-else>
                <span class="h-2 w-2 rounded-full bg-red-400 shrink-0"></span>
                <span class="text-xs text-red-600">ناموجود — به‌زودی موجود می‌شود</span>
              </template>
            </div>

            <div class="mt-8 flex gap-3">
              <button
                type="button" @click="addToCart"
                :disabled="stockStatus === 'out_of_stock'"
                :class="['add-btn flex-1', added ? 'add-btn--done' : '', stockStatus === 'out_of_stock' ? 'opacity-50 cursor-not-allowed' : '']"
              >
                {{ stockStatus === 'out_of_stock' ? 'ناموجود' : added ? '✓ به سبد اضافه شد' : 'افزودن به سبد خرید' }}
              </button>
              <button
                type="button"
                @click="wishlistStore.toggle(product.id)"
                :class="[
                  'flex h-[52px] w-[52px] shrink-0 items-center justify-center border transition-all duration-200',
                  wishlistStore.isWishlisted(product.id)
                    ? 'border-maroon bg-maroon text-white'
                    : 'border-border bg-background hover:border-maroon hover:text-maroon'
                ]"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" :fill="wishlistStore.isWishlisted(product.id) ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
                </svg>
              </button>
            </div>

            <RouterLink to="/cart" class="mt-3 block text-center text-xs text-muted-foreground hover:text-maroon font-[Vazirmatn]">
              مشاهده سبد خرید →
            </RouterLink>
          </div>
        </div>
      </section>

      <!-- Global FAQs -->
      <section v-if="globalFaqs.length" class="border-b border-border">
        <div class="mx-auto max-w-4xl px-6 py-12">
          <div v-for="faq in globalFaqs" :key="faq.id" class="border-b border-[#E8E4DE]">
            <button type="button" @click="openAcc = openAcc === faq.id ? null : faq.id"
              class="flex w-full cursor-pointer items-center justify-between py-5 text-right">
              <ChevronDown :class="['h-4 w-4 transition-transform text-muted-foreground', openAcc === faq.id ? 'rotate-180' : '']" />
              <span class="text-base font-[Vazirmatn]">{{ faq.title }}</span>
            </button>
            <div v-if="openAcc === faq.id" class="pb-5 pr-8 text-sm leading-7 text-muted-foreground font-[Vazirmatn] whitespace-pre-line">{{ faq.content }}</div>
          </div>
        </div>
      </section>

      <!-- Reviews section -->
      <section class="border-t border-border">
        <div class="mx-auto max-w-7xl px-6 py-12">
          <div class="flex items-start justify-between gap-4 mb-8">
            <div>
              <span class="text-xs uppercase tracking-[0.3em] text-maroon">نظرات مشتریان</span>
              <h2 class="mt-2 text-2xl font-light">دیدگاه‌ها</h2>
            </div>
          </div>
          <div class="grid gap-10 lg:grid-cols-[1fr_360px]">
            <div>
              <div v-if="reviews.length === 0" class="border border-dashed border-border py-12 text-center text-sm text-muted-foreground">
                هنوز نظری ثبت نشده. اولین نفر باشید!
              </div>
            </div>
            <div class="border border-border bg-muted/20 p-6">
              <div class="text-xs uppercase tracking-widest text-maroon mb-4">نظر شما</div>
              <form @submit.prevent="submitReview" class="space-y-4">
                <div>
                  <label class="block text-xs uppercase tracking-widest text-muted-foreground mb-1.5">امتیاز</label>
                  <div class="flex gap-1">
                    <button v-for="i in 5" :key="i" type="button"
                      @mouseenter="hoverStar = i" @mouseleave="hoverStar = 0" @click="reviewForm.rating = i">
                      <Star class="h-6 w-6 transition-colors" :class="i <= (hoverStar || reviewForm.rating) ? 'fill-maroon text-maroon' : 'text-border hover:text-maroon/50'" />
                    </button>
                  </div>
                </div>
                <div>
                  <label class="block text-xs uppercase tracking-widest text-muted-foreground mb-1.5">نام شما</label>
                  <input v-model="reviewForm.name" required placeholder="علی محمدی" class="w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
                </div>
                <div>
                  <label class="block text-xs uppercase tracking-widest text-muted-foreground mb-1.5">نظر</label>
                  <textarea v-model="reviewForm.text" required rows="4" placeholder="تجربه شما از این محصول..." class="w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon resize-none" />
                </div>
                <button type="submit" class="w-full bg-maroon py-3 text-sm text-white hover:opacity-90 transition-opacity">ثبت نظر</button>
              </form>
            </div>
          </div>
        </div>
      </section>

      <!-- Related products -->
      <section v-if="related.length">
        <SectionHeader title="محصولات مرتبط" tag="ممکن است بپسندید" />
        <div class="related-grid">
          <ProductCard v-for="p in related" :key="p.id" :product="p" />
        </div>
      </section>
    </template>
  </TheLayout>
</template>

<style scoped>
.price-row {
  display: flex;
  align-items: baseline;
  gap: 0.4rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid #E8E4DE;
}
.price-row__amount {
  font-family: 'Vazirmatn', sans-serif;
  font-size: 2rem;
  font-weight: 400;
  color: #111;
  letter-spacing: -0.02em;
}
.price-row__unit {
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.85rem;
  color: #9e9890;
}
.picker-label {
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.7rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #9e9890;
  margin-bottom: 0.6rem;
}
.picker-chip {
  border: 1px solid #E8E4DE;
  background-color: #FAFAF8;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.85rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  color: #222;
  transition: border-color 0.2s, background-color 0.2s;
}
.picker-chip:hover { border-color: #bbb5ad; background-color: #F5F3F0; }
.picker-chip--active { border-color: #800000; background-color: #fff; color: #800000; }
.add-btn {
  width: 100%; padding: 1rem; text-align: center;
  font-family: 'Vazirmatn', sans-serif; font-size: 0.9rem; font-weight: 400;
  background-color: #800000; color: #fff; border: none; cursor: pointer; transition: opacity 0.2s;
}
.add-btn:hover { opacity: 0.88; }
.add-btn--done { background-color: #5a0000; }
.related-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px;
  background-color: #E8E4DE; border-top: 1px solid #E8E4DE; padding: 0;
}
@media (max-width: 1024px) { .related-grid { grid-template-columns: repeat(2, 1fr); } }
</style>
