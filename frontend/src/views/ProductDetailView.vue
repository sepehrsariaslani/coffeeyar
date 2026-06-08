<script setup>
import { ref, computed, watch } from "vue";
import { useRoute, RouterLink } from "vue-router";
import { ChevronDown, Coffee, Leaf, Truck, Package, Star } from "lucide-vue-next";
import TheLayout from "@/components/site/TheLayout.vue";
import FlavorTriangle from "@/components/site/FlavorTriangle.vue";
import ProfileChart from "@/components/site/ProfileChart.vue";
import { useProductProfilesStore } from "@/stores/productProfiles.js";
import AppSelect from "@/components/AppSelect.vue";
import ProductGallery from "@/components/ProductGallery.vue";
import ProductCard from "@/components/ProductCard.vue";
import SectionHeader from "@/components/SectionHeader.vue";
import { products, formatPrice } from "@/lib/data.js";
import { useCartStore } from "@/stores/cart.js";
import { useReviewsStore } from "@/stores/reviews.js";
import { useWishlistStore } from "@/stores/wishlist.js";
import { toFa } from "@/lib/utils.js";
import { useSeo } from "@/composables/useSeo.js";
import { useJsonLd } from "@/composables/useJsonLd.js";
import { useProductGlobalFaqsStore } from "@/stores/productGlobalFaqs.js";

const route = useRoute();
const cartStore = useCartStore();
const reviewsStore = useReviewsStore();
const wishlistStore = useWishlistStore();
const profilesStore = useProductProfilesStore();

const productAssignment = computed(() =>
  product.value ? profilesStore.getAssignment(product.value.id) : null
);
const productProfile = computed(() =>
  productAssignment.value ? profilesStore.getProfile(productAssignment.value.profileId) : null
);

const product = computed(() =>
  products.find((p) => p.id === route.params.id)
);

useSeo({
  title: computed(() => product.value?.name),
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

const isAccessory = computed(() => product.value?.type === "accessory");

const globalFaqsStore = useProductGlobalFaqsStore();
const globalFaqs = computed(() =>
  globalFaqsStore.getFaqsForType(isAccessory.value ? "accessory" : "coffee")
);

const related = computed(() =>
  products
    .filter((p) => p.id !== route.params.id && p.type === product.value?.type)
    .slice(0, 4)
);

const selectedWeight = ref(0);
const selectedGrind = ref(0);
const activeImg = ref(0);
const openAcc = ref(null);
const added = ref(false);
const qty = ref(1);

/* ── Inline profile assignment panel ── */
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

const price = computed(() => {
  if (!product.value) return 0;
  if (isAccessory.value) return product.value.price;
  return Math.round(
    product.value.price * product.value.weights[selectedWeight.value].multiplier
  );
});

function addToCart() {
  if (!product.value) return;
  if (isAccessory.value) {
    cartStore.add({
      productId: product.value.id,
      name: product.value.name,
      image: product.value.image,
      weight: "۱ عدد",
      grind: product.value.category || "اکسسوری",
      unitPrice: product.value.price,
      qty: qty.value,
    });
  } else {
    cartStore.add({
      productId: product.value.id,
      name: product.value.name,
      image: product.value.image,
      weight: product.value.weights[selectedWeight.value].label,
      grind: product.value.grinds[selectedGrind.value],
      unitPrice: price.value,
      qty: 1,
    });
  }
  added.value = true;
  setTimeout(() => (added.value = false), 2000);
}
</script>

<template>
  <TheLayout>
    <div v-if="!product" class="mx-auto max-w-2xl px-6 py-32 text-center">
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
        <RouterLink
          v-if="isAccessory"
          to="/products"
          @click.prevent="$router.push({ path: '/products', query: { tab: 'accessories' } })"
          class="text-[#9e9890] hover:text-foreground transition-colors"
        >اکسسوری</RouterLink>
        <span v-if="isAccessory" class="text-[#C8C2BA]">·</span>
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
                  :image="product.gallery[activeImg] || product.image"
                  :alt="product.name"
                  :badge="isAccessory ? product.category : product.roast"
                />
              </div>
              <div v-if="product.gallery?.length > 1" class="flex gap-2 md:flex-col md:justify-start md:py-6 md:pr-0 md:pl-6">
                <button
                  v-for="(img, idx) in product.gallery"
                  :key="idx"
                  type="button"
                  @click="activeImg = idx"
                  class="thumb-btn"
                  :class="activeImg === idx ? 'thumb-btn--active' : ''"
                >
                  <img :src="img" :alt="`تصویر ${idx + 1}`" class="h-full w-full object-cover" />
                </button>
              </div>
            </div>
          </div>

          <!-- Info -->
          <div class="flex flex-col justify-center px-6 py-12 md:px-12 md:py-16">
            <!-- Accessory header -->
            <template v-if="isAccessory">
              <div class="flex items-center gap-3 mb-4">
                <span class="text-xs uppercase tracking-[0.2em] text-maroon font-[Vazirmatn]">{{ product.category }}</span>
                <span class="h-px w-6 bg-[#E8E4DE]" />
                <span class="text-xs text-muted-foreground font-[Vazirmatn]">{{ product.brand }}</span>
              </div>
              <h1 class="text-4xl font-light leading-tight mb-4">{{ product.name }}</h1>
              <p class="leading-7 text-muted-foreground mb-6">{{ product.description }}</p>

              <div class="price-row">
                <span class="price-row__amount">{{ formatPrice(price) }}</span>
              </div>

              <!-- Qty selector -->
              <div class="mt-8">
                <div class="picker-label">تعداد</div>
                <div class="flex items-center gap-3">
                  <button type="button" @click="qty = Math.max(1, qty - 1)"
                    class="flex h-10 w-10 items-center justify-center border border-[#E8E4DE] text-lg hover:border-maroon">−</button>
                  <span class="min-w-[2rem] text-center font-[Vazirmatn]">{{ qty }}</span>
                  <button type="button" @click="qty++"
                    class="flex h-10 w-10 items-center justify-center border border-[#E8E4DE] text-lg hover:border-maroon">+</button>
                </div>
              </div>
            </template>

            <!-- Coffee header -->
            <template v-else>
              <div class="flex items-center gap-3 mb-4">
                <span class="text-xs uppercase tracking-[0.2em] text-maroon font-[Vazirmatn]">{{ product.origin }}</span>
                <span class="h-px w-6 bg-[#E8E4DE]" />
                <span class="text-xs text-muted-foreground font-[Vazirmatn]">فرآوری {{ product.process }}</span>
              </div>

              <h1 class="text-4xl font-light leading-tight mb-4">{{ product.name }}</h1>
              <p class="leading-7 text-muted-foreground mb-4">{{ product.description }}</p>

              <div class="flex flex-wrap gap-2 mb-6">
                <span
                  v-for="note in product.notes" :key="note"
                  class="border border-[#E8E4DE] px-3 py-1 text-xs text-muted-foreground font-[Vazirmatn]"
                >
                  {{ note }}
                </span>
              </div>

              <div class="price-row">
                <span class="price-row__amount">{{ formatPrice(price) }}</span>
                <span class="price-row__unit">تومان</span>
              </div>

              <!-- Weight selector -->
              <div class="mt-8">
                <div class="picker-label">وزن</div>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="(w, idx) in product.weights" :key="w.label"
                    type="button" @click="selectedWeight = idx"
                    :class="['picker-chip', selectedWeight === idx ? 'picker-chip--active' : '']"
                  >
                    {{ w.label }}
                  </button>
                </div>
              </div>

              <!-- Grind selector -->
              <div class="mt-5">
                <div class="picker-label">نوع آسیاب</div>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="(g, idx) in product.grinds" :key="g"
                    type="button" @click="selectedGrind = idx"
                    :class="['picker-chip', selectedGrind === idx ? 'picker-chip--active' : '']"
                  >
                    {{ g }}
                  </button>
                </div>
              </div>
            </template>

            <!-- Stock indicator -->
            <div class="mt-6 flex items-center gap-2 font-[Vazirmatn]">
              <template v-if="product.stock === 'in_stock'">
                <span class="h-2 w-2 rounded-full bg-green-500 shrink-0"></span>
                <span class="text-xs text-green-700">موجود در انبار</span>
                <span v-if="product.stockCount" class="text-xs text-muted-foreground">({{ product.stockCount.toLocaleString('fa-IR') }} عدد)</span>
              </template>
              <template v-else-if="product.stock === 'low_stock'">
                <span class="h-2 w-2 rounded-full bg-amber-500 shrink-0 animate-pulse"></span>
                <span class="text-xs text-amber-700 font-medium">موجودی محدود</span>
                <span v-if="product.stockCount" class="text-xs text-muted-foreground">(فقط {{ product.stockCount.toLocaleString('fa-IR') }} عدد باقی مانده)</span>
              </template>
              <template v-else-if="product.stock === 'out_of_stock'">
                <span class="h-2 w-2 rounded-full bg-red-400 shrink-0"></span>
                <span class="text-xs text-red-600">ناموجود — به‌زودی موجود می‌شود</span>
              </template>
            </div>

            <div class="mt-8 flex gap-3">
              <button
                type="button" @click="addToCart"
                :disabled="product.stock === 'out_of_stock'"
                :class="['add-btn flex-1', added ? 'add-btn--done' : '', product.stock === 'out_of_stock' ? 'opacity-50 cursor-not-allowed' : '']"
              >
                {{ product.stock === 'out_of_stock' ? 'ناموجود' : added ? '✓ به سبد اضافه شد' : 'افزودن به سبد خرید' }}
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
                :title="wishlistStore.isWishlisted(product.id) ? 'حذف از علاقه‌مندی‌ها' : 'افزودن به علاقه‌مندی‌ها'"
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

      <!-- Accessory Specs -->
      <template v-if="isAccessory">
        <section class="border-b border-border">
          <div class="mx-auto max-w-7xl px-6 py-16">
            <span class="text-xs uppercase tracking-[0.3em] text-maroon">مشخصات فنی</span>
            <div class="mt-8 grid gap-px bg-[#E8E4DE] sm:grid-cols-2 lg:grid-cols-3">
              <div
                v-for="spec in product.specs"
                :key="spec.label"
                class="bg-background p-6 text-center"
              >
                <div class="text-xs uppercase tracking-widest text-maroon font-[Vazirmatn]">{{ spec.label }}</div>
                <div class="mt-3 text-lg font-light">{{ spec.value }}</div>
              </div>
            </div>
          </div>
        </section>

        <!-- Accessory FAQs — product-specific + global -->
        <section v-if="product.productFaqs?.length || globalFaqs.length" class="border-b border-border">
          <div class="mx-auto max-w-4xl px-6 py-12">
            <!-- product-specific FAQs -->
            <template v-if="product.productFaqs?.length">
              <div class="mb-1 text-[10px] uppercase tracking-widest text-maroon pb-2">سوالات تخصصی</div>
              <div
                v-for="(faq, i) in product.productFaqs"
                :key="'pf-' + i"
                class="border-b border-[#E8E4DE]"
              >
                <button
                  type="button"
                  @click="openAcc = openAcc === 'pf-' + i ? null : 'pf-' + i"
                  class="flex w-full cursor-pointer items-center justify-between py-5 text-right"
                >
                  <ChevronDown :class="['h-4 w-4 transition-transform text-muted-foreground', openAcc === 'pf-' + i ? 'rotate-180' : '']" />
                  <span class="text-base font-[Vazirmatn]">{{ faq.q }}</span>
                </button>
                <div v-if="openAcc === 'pf-' + i" class="pb-5 pr-8 text-sm leading-7 text-muted-foreground font-[Vazirmatn] whitespace-pre-line">{{ faq.a }}</div>
              </div>
              <div v-if="globalFaqs.length" class="pt-2" />
            </template>
            <!-- global FAQs -->
            <div
              v-for="faq in globalFaqs"
              :key="faq.id"
              class="border-b border-[#E8E4DE]"
            >
              <button
                type="button"
                @click="openAcc = openAcc === faq.id ? null : faq.id"
                class="flex w-full cursor-pointer items-center justify-between py-5 text-right"
              >
                <ChevronDown :class="['h-4 w-4 transition-transform text-muted-foreground', openAcc === faq.id ? 'rotate-180' : '']" />
                <span class="text-base font-[Vazirmatn]">{{ faq.title }}</span>
              </button>
              <div v-if="openAcc === faq.id" class="pb-5 pr-8 text-sm leading-7 text-muted-foreground font-[Vazirmatn] whitespace-pre-line">{{ faq.content }}</div>
            </div>
          </div>
        </section>
      </template>

      <!-- Coffee-specific sections -->
      <template v-else>
        <!-- Profile Chart (from store) or fallback FlavorTriangle -->
        <section v-if="productProfile && productAssignment" class="border-b border-border bg-[#FAFAF8]">
          <div class="mx-auto grid max-w-7xl items-center gap-12 px-6 py-16 md:grid-cols-2">
            <div>
              <span class="text-xs uppercase tracking-[0.3em] text-maroon font-[Vazirmatn]">نمودار ویژگی‌ها</span>
              <h2 class="mt-3 text-3xl font-light md:text-4xl">{{ productProfile.name }}</h2>
              <p class="mt-4 max-w-md leading-8 text-muted-foreground">
                این نمودار ویژگی‌های کلیدی این محصول را نشان می‌دهد.
              </p>
              <dl class="mt-8 grid gap-4" :style="`grid-template-columns: repeat(${Math.min(productProfile.traits.length, 3)}, 1fr)`">
                <div
                  v-for="t in productProfile.traits"
                  :key="t.id"
                  class="border-t-2 border-maroon pt-3"
                >
                  <dt class="text-xs text-muted-foreground font-[Vazirmatn]">{{ t.name }}</dt>
                  <dd class="mt-1 text-2xl font-light text-maroon">
                    {{ toFa(productAssignment.ratings[t.id] ?? 0) }}<span class="text-sm text-muted-foreground">/۱۰</span>
                  </dd>
                </div>
              </dl>
            </div>
            <div class="flex justify-center">
              <ProfileChart :traits="productProfile.traits" :ratings="productAssignment.ratings" />
            </div>
          </div>
        </section>

        <!-- Fallback: hardcoded FlavorTriangle if no profile assigned but product has flavor data -->
        <section v-else-if="product.flavor" class="border-b border-border bg-[#FAFAF8]">
          <div class="mx-auto grid max-w-7xl items-center gap-12 px-6 py-16 md:grid-cols-2">
            <div>
              <span class="text-xs uppercase tracking-[0.3em] text-maroon font-[Vazirmatn]">مثلث طعم</span>
              <h2 class="mt-3 text-3xl font-light md:text-4xl">پروفایل چشایی</h2>
              <p class="mt-4 max-w-md leading-8 text-muted-foreground">
                این نمودار نسبت سه ویژگی کلیدی فنجان شما را نشان می‌دهد.
              </p>
              <dl class="mt-8 grid grid-cols-3 gap-4">
                <div
                  v-for="m in [
                    { l: 'تلخی', v: product.flavor.bitterness },
                    { l: 'اسیدیته', v: product.flavor.acidity },
                    { l: 'عطر', v: product.flavor.aroma },
                  ]"
                  :key="m.l"
                  class="border-t-2 border-maroon pt-3"
                >
                  <dt class="text-xs text-muted-foreground font-[Vazirmatn]">{{ m.l }}</dt>
                  <dd class="mt-1 text-2xl font-light text-maroon">
                    {{ toFa(m.v) }}<span class="text-sm text-muted-foreground">/۱۰</span>
                  </dd>
                </div>
              </dl>
            </div>
            <div class="flex justify-center">
              <FlavorTriangle :flavor="product.flavor" />
            </div>
          </div>
        </section>

        <!-- Specs grid — dynamic if product has specs array, otherwise fallback -->
        <section class="border-b border-border">
          <template v-if="product.specs?.length">
            <div class="mx-auto max-w-7xl px-6 py-16">
              <span class="text-xs uppercase tracking-[0.3em] text-maroon">مشخصات فنی</span>
              <div class="mt-8 grid gap-px bg-[#E8E4DE] sm:grid-cols-2 lg:grid-cols-3">
                <div
                  v-for="spec in product.specs"
                  :key="spec.label"
                  class="bg-background p-6 text-center"
                >
                  <div class="text-xs uppercase tracking-widest text-maroon font-[Vazirmatn]">{{ spec.label }}</div>
                  <div class="mt-3 text-lg font-light">{{ spec.value }}</div>
                </div>
              </div>
            </div>
          </template>
          <template v-else>
            <div class="mx-auto grid max-w-7xl gap-px bg-[#E8E4DE] md:grid-cols-3">
              <div
                v-for="s in [
                  { l: 'خاستگاه', v: product.origin },
                  { l: 'فرآوری', v: product.process },
                  { l: 'اسیدیته', v: `${toFa(product.flavor.acidity)} / ۱۰` },
                  ...Object.entries(product.customAttributes ?? {}).map(([l, v]) => ({ l, v })),
                ].slice(0, 6)"
                :key="s.l"
                class="bg-background p-8 text-center"
              >
                <div class="text-xs uppercase tracking-widest text-maroon font-[Vazirmatn]">{{ s.l }}</div>
                <div class="mt-3 text-xl font-light">{{ s.v }}</div>
              </div>
            </div>
          </template>
        </section>

        <!-- Coffee FAQs — product-specific + global -->
        <section v-if="product.productFaqs?.length || globalFaqs.length" class="border-b border-border">
          <div class="mx-auto max-w-4xl px-6 py-12">
            <!-- product-specific FAQs -->
            <template v-if="product.productFaqs?.length">
              <div class="mb-1 text-[10px] uppercase tracking-widest text-maroon pb-2">سوالات تخصصی</div>
              <div
                v-for="(faq, i) in product.productFaqs"
                :key="'pf-' + i"
                class="border-b border-[#E8E4DE]"
              >
                <button
                  type="button"
                  @click="openAcc = openAcc === 'pf-' + i ? null : 'pf-' + i"
                  class="flex w-full cursor-pointer items-center justify-between py-5 text-right"
                >
                  <ChevronDown :class="['h-4 w-4 transition-transform text-muted-foreground', openAcc === 'pf-' + i ? 'rotate-180' : '']" />
                  <span class="text-base font-[Vazirmatn]">{{ faq.q }}</span>
                </button>
                <div v-if="openAcc === 'pf-' + i" class="pb-5 pr-8 text-sm leading-7 text-muted-foreground font-[Vazirmatn] whitespace-pre-line">{{ faq.a }}</div>
              </div>
              <div v-if="globalFaqs.length" class="pt-2" />
            </template>
            <!-- global FAQs -->
            <div
              v-for="faq in globalFaqs"
              :key="faq.id"
              class="border-b border-[#E8E4DE]"
            >
              <button
                type="button"
                @click="openAcc = openAcc === faq.id ? null : faq.id"
                class="flex w-full cursor-pointer items-center justify-between py-5 text-right"
              >
                <ChevronDown :class="['h-4 w-4 transition-transform text-muted-foreground', openAcc === faq.id ? 'rotate-180' : '']" />
                <span class="text-base font-[Vazirmatn]">{{ faq.title }}</span>
              </button>
              <div v-if="openAcc === faq.id" class="pb-5 pr-8 text-sm leading-7 text-muted-foreground font-[Vazirmatn] whitespace-pre-line">{{ faq.content }}</div>
            </div>
          </div>
        </section>
      </template>

      <!-- Reviews section -->
      <section class="border-t border-border">
        <div class="mx-auto max-w-7xl px-6 py-12">
          <div class="flex items-start justify-between gap-4 mb-8">
            <div>
              <span class="text-xs uppercase tracking-[0.3em] text-maroon">نظرات مشتریان</span>
              <h2 class="mt-2 text-2xl font-light">دیدگاه‌ها</h2>
            </div>
            <div v-if="reviews.length" class="flex flex-col items-center gap-1 border border-border px-5 py-3">
              <div class="text-3xl font-light">{{ avgRating }}</div>
              <div class="flex gap-0.5">
                <Star
                  v-for="i in 5"
                  :key="i"
                  class="h-4 w-4"
                  :class="i <= Math.round(avgRating) ? 'fill-maroon text-maroon' : 'text-border'"
                />
              </div>
              <div class="text-xs text-muted-foreground">{{ toFa(reviews.length) }} نظر</div>
            </div>
          </div>

          <div class="grid gap-10 lg:grid-cols-[1fr_360px]">
            <!-- Reviews list -->
            <div>
              <div v-if="reviews.length === 0" class="border border-dashed border-border py-12 text-center text-sm text-muted-foreground">
                هنوز نظری ثبت نشده. اولین نفر باشید!
              </div>
              <div v-else class="space-y-6">
                <div
                  v-for="r in reviews"
                  :key="r.id"
                  class="border-b border-border pb-6 last:border-0"
                >
                  <div class="flex items-start justify-between gap-4">
                    <div class="flex items-center gap-3">
                      <div class="flex h-9 w-9 items-center justify-center rounded-full bg-maroon/10 text-sm font-medium text-maroon">
                        {{ r.name.slice(0, 1) }}
                      </div>
                      <div>
                        <div class="text-sm font-medium">{{ r.name }}</div>
                        <div class="text-xs text-muted-foreground">{{ r.date }}</div>
                      </div>
                    </div>
                    <div class="flex gap-0.5 shrink-0">
                      <Star
                        v-for="i in 5"
                        :key="i"
                        class="h-3.5 w-3.5"
                        :class="i <= r.rating ? 'fill-maroon text-maroon' : 'text-border'"
                      />
                    </div>
                  </div>
                  <p class="mt-3 text-sm leading-7 text-muted-foreground">{{ r.text }}</p>
                </div>
              </div>
            </div>

            <!-- Review form -->
            <div class="border border-border bg-muted/20 p-6">
              <div class="text-xs uppercase tracking-widest text-maroon mb-4">نظر شما</div>
              <div
                v-if="reviewSubmitted"
                class="mb-4 border border-maroon/30 bg-maroon/5 px-4 py-3 text-sm text-maroon"
              >
                نظر شما با موفقیت ثبت شد.
              </div>
              <form @submit.prevent="submitReview" class="space-y-4">
                <div>
                  <label class="block text-xs uppercase tracking-widest text-muted-foreground mb-1.5">امتیاز</label>
                  <div class="flex gap-1">
                    <button
                      v-for="i in 5"
                      :key="i"
                      type="button"
                      @mouseenter="hoverStar = i"
                      @mouseleave="hoverStar = 0"
                      @click="reviewForm.rating = i"
                    >
                      <Star
                        class="h-6 w-6 transition-colors"
                        :class="i <= (hoverStar || reviewForm.rating) ? 'fill-maroon text-maroon' : 'text-border hover:text-maroon/50'"
                      />
                    </button>
                  </div>
                </div>
                <div>
                  <label class="block text-xs uppercase tracking-widest text-muted-foreground mb-1.5">نام شما</label>
                  <input
                    v-model="reviewForm.name"
                    required
                    placeholder="علی محمدی"
                    class="w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon"
                  />
                </div>
                <div>
                  <label class="block text-xs uppercase tracking-widest text-muted-foreground mb-1.5">نظر</label>
                  <textarea
                    v-model="reviewForm.text"
                    required
                    rows="4"
                    placeholder="تجربه شما از این محصول..."
                    class="w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon resize-none"
                  />
                </div>
                <button
                  type="submit"
                  class="w-full bg-maroon py-3 text-sm text-white hover:opacity-90 transition-opacity"
                >
                  ثبت نظر
                </button>
              </form>
            </div>
          </div>
        </div>
      </section>

      <!-- ── Admin: Inline Profile Assignment ── -->
      <section class="border-t border-border bg-[#F8F6F3]">
        <div class="mx-auto max-w-7xl px-6 py-6">
          <button
            type="button"
            @click="inlinePanelOpen = !inlinePanelOpen"
            class="inline-flex items-center gap-2 text-xs text-muted-foreground hover:text-foreground transition-colors"
          >
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" class="shrink-0">
              <circle cx="7" cy="7" r="6" stroke="currentColor" stroke-width="1.2"/>
              <path d="M5 7h4M7 5v4" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
            </svg>
            <span>{{ productProfile ? `پروفایل: ${productProfile.name}` : 'تخصیص پروفایل محصول' }}</span>
            <svg
              :class="['w-3 h-3 transition-transform text-muted-foreground', inlinePanelOpen ? 'rotate-180' : '']"
              viewBox="0 0 12 12" fill="none"
            >
              <path d="M2 4L6 8L10 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </button>

          <div v-if="inlinePanelOpen" class="mt-6 grid gap-8 md:grid-cols-2 border border-border bg-background p-6">
            <div class="space-y-5">
              <div>
                <label class="block text-[10px] uppercase tracking-[0.2em] text-muted-foreground mb-2">پروفایل ویژگی</label>
                <AppSelect
                  v-model="inlineProfileId"
                  :options="profilesStore.profiles.map(p => ({ label: p.name, value: p.id }))"
                  placeholder="انتخاب پروفایل…"
                  :clearable="true"
                />
              </div>

              <template v-if="inlineProfile">
                <div class="space-y-4">
                  <p class="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">امتیاز ویژگی‌ها</p>
                  <div v-for="t in inlineProfile.traits" :key="t.id" class="space-y-1">
                    <div class="flex justify-between text-sm">
                      <span class="font-[Vazirmatn]">{{ t.name }}</span>
                      <span class="text-maroon font-medium font-[Vazirmatn]">{{ toFa(inlineRatings[t.id] ?? 0) }} / ۱۰</span>
                    </div>
                    <input
                      type="range" min="0" max="10" step="0.5"
                      v-model.number="inlineRatings[t.id]"
                      class="w-full h-1.5 accent-maroon"
                    />
                    <div class="flex justify-between text-[10px] text-muted-foreground font-[Vazirmatn]">
                      <span>۰</span><span>۵</span><span>۱۰</span>
                    </div>
                  </div>
                </div>

                <div class="flex gap-3 pt-1">
                  <button
                    @click="saveInlineAssignment"
                    class="flex-1 py-2.5 text-xs text-center transition-all font-[Vazirmatn]"
                    :class="inlineSaved ? 'bg-green-700 text-white' : 'bg-foreground text-background hover:opacity-80'"
                  >
                    {{ inlineSaved ? '✓ ذخیره شد' : 'ذخیره پروفایل' }}
                  </button>
                  <button
                    v-if="productAssignment"
                    @click="removeInlineAssignment"
                    class="px-4 py-2.5 text-xs border border-border text-muted-foreground hover:text-red-600 hover:border-red-200 transition-colors"
                  >حذف</button>
                </div>
              </template>

              <div v-else-if="!inlineProfileId" class="text-sm text-muted-foreground font-[Vazirmatn] py-4 border border-dashed border-border text-center">
                یک پروفایل انتخاب کنید تا ویژگی‌ها نمایش داده شوند.
              </div>
            </div>

            <!-- Live preview -->
            <div class="flex flex-col items-center justify-center border border-border bg-[#FAFAF8] p-4">
              <template v-if="inlineProfile && Object.keys(inlineRatings).length">
                <p class="text-[10px] uppercase tracking-widest text-muted-foreground mb-3">پیش‌نمایش</p>
                <ProfileChart :traits="inlineProfile.traits" :ratings="inlineRatings" />
              </template>
              <div v-else class="text-sm text-muted-foreground font-[Vazirmatn] text-center py-8">
                پیش‌نمایش نمودار اینجا نشان داده می‌شود
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Related products -->
      <section>
        <SectionHeader :title="isAccessory ? 'اکسسوری‌های مرتبط' : 'محصولات مرتبط'" tag="ممکن است بپسندید" />
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

.picker-chip:hover {
  border-color: #bbb5ad;
  background-color: #F5F3F0;
}

.picker-chip--active {
  border-color: #800000;
  background-color: #fff;
  color: #800000;
}

.add-btn {
  width: 100%;
  padding: 1rem;
  text-align: center;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.9rem;
  font-weight: 400;
  background-color: #800000;
  color: #fff;
  border: none;
  cursor: pointer;
  transition: opacity 0.2s;
}

.add-btn:hover {
  opacity: 0.88;
}

.add-btn--done {
  background-color: #5a0000;
}

.thumb-btn {
  width: 64px;
  height: 64px;
  flex-shrink: 0;
  overflow: hidden;
  border: 2px solid transparent;
  transition: border-color 0.2s;
  cursor: pointer;
}

.thumb-btn:hover {
  border-color: rgba(128, 0, 0, 0.4);
}

.thumb-btn--active {
  border-color: #800000;
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background-color: #E8E4DE;
  border-top: 1px solid #E8E4DE;
  padding: 0;
}

@media (max-width: 1024px) {
  .related-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
