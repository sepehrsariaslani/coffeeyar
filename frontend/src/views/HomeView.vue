<script setup>
import { ref, computed, onMounted } from "vue";
import { RouterLink } from "vue-router";
import TheLayout from "@/components/site/TheLayout.vue";
import HeroSection from "@/components/HeroSection.vue";
import FeaturedGrid from "@/components/FeaturedGrid.vue";
import SectionHeader from "@/components/SectionHeader.vue";
import ProductCard from "@/components/ProductCard.vue";
import BrandsMarquee from "@/components/BrandsMarquee.vue";
import BlogCard from "@/components/BlogCard.vue";
import { useProductsStore } from "@/stores/products.js";
import { usePostsStore } from "@/stores/posts.js";
import { useCategoriesStore } from "@/stores/categories.js";
import { useContentStore } from "@/stores/content.js";
import { useSeo } from "@/composables/useSeo.js";
import heroImg from "@/assets/hero-coffee.jpg";

useSeo({
  title: "نوار — قهوه تخصصی",
  description: "دانه‌های تک‌خاستگاه از مزارع شناخته‌شده. تازه برشته‌شده در کارگاه کوچک ما. ارسال به سراسر ایران.",
});

const productsStore = useProductsStore();
const postsStore = usePostsStore();
const categoriesStore = useCategoriesStore();
const contentStore = useContentStore();

const activeCategory = ref("all");

const coffeeProducts = computed(() => productsStore.products);
const featuredProducts = computed(() => productsStore.products.filter((p) => p.is_featured));

const filtered = computed(() =>
  activeCategory.value === "all"
    ? coffeeProducts.value
    : coffeeProducts.value.filter((p) => p.category_slug === activeCategory.value)
);

const recentPosts = computed(() => postsStore.getPublished().slice(0, 3));

const categories = computed(() => [
  { label: "همه", value: "all" },
  ...categoriesStore.roots.map((c) => ({ label: c.name, value: c.slug })),
]);

onMounted(async () => {
  await Promise.all([
    productsStore.fetchProducts({ page_size: 12 }),
    postsStore.fetchPosts(),
    categoriesStore.fetchCategories(),
  ]);
});
</script>

<template>
  <TheLayout>
    <!-- Hero -->
    <HeroSection
      :image="heroImg"
      :title="contentStore.content.home.heroTitle"
      :subtitle="contentStore.content.home.heroSubtitle"
    />

    <!-- Brands Marquee -->
    <BrandsMarquee />

    <!-- Categories Section -->
    <section class="border-b border-border">
      <SectionHeader title="دسته‌بندی‌ها" tag="گروه‌های محصول" />
      <div class="px-[5vw] pb-12">
        <div v-if="categoriesStore.roots.length" class="grid grid-cols-2 gap-3 md:grid-cols-4">
          <RouterLink
            v-for="cat in categoriesStore.roots"
            :key="cat.id"
            :to="`/products?category=${cat.slug}`"
            class="group relative border border-border bg-muted/20 p-5 hover:border-maroon hover:bg-maroon/5 transition-all duration-200"
          >
            <div class="text-2xl mb-3">{{ cat.icon }}</div>
            <div class="font-medium text-sm leading-snug">{{ cat.name }}</div>
            <div class="mt-1.5 text-xs text-muted-foreground line-clamp-2 leading-relaxed">{{ cat.description }}</div>
            <div class="mt-4 flex items-center gap-1 text-xs text-muted-foreground group-hover:text-maroon transition-colors">
              <span>مشاهده</span>
              <svg width="12" height="12" viewBox="0 0 16 16" fill="none" class="shrink-0">
                <path d="M12 8H4M8 4L4 8L8 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </RouterLink>
        </div>
        <div v-else-if="categoriesStore.loading" class="py-12 text-center text-sm text-muted-foreground">در حال بارگذاری...</div>
        <div v-else class="border border-dashed border-border py-12 text-center text-sm text-muted-foreground">
          هنوز دسته‌بندی‌ای تعریف نشده است.
        </div>
      </div>
    </section>

    <!-- Featured grid -->
    <div v-if="featuredProducts.length" class="border-b border-border">
      <SectionHeader title="محصولات ویژه" tag="منتخب" to="/products" />
      <FeaturedGrid :items="featuredProducts" />
    </div>

    <!-- Products with category tabs -->
    <section class="border-b border-border">
      <SectionHeader title="همه محصولات" tag="کاتالوگ" to="/products" link-label="مشاهده کامل" />

      <div class="px-[5vw]">
        <div class="flex items-center gap-1 border-b border-[#E8E4DE] pt-4">
          <button
            v-for="c in categories"
            :key="c.value"
            type="button"
            @click="activeCategory = c.value"
            :class="[
              'px-5 py-3 text-sm transition-colors font-[Vazirmatn]',
              activeCategory === c.value
                ? 'border-b-2 border-maroon text-maroon'
                : 'text-muted-foreground hover:text-foreground',
            ]"
          >
            {{ c.label }}
          </button>
        </div>
      </div>

      <div class="product-listing">
        <div v-if="productsStore.loading" class="py-20 text-center text-muted-foreground">در حال بارگذاری محصولات...</div>
        <div v-else-if="filtered.length === 0" class="py-20 text-center text-muted-foreground">
          محصولی در این دسته‌بندی وجود ندارد.
        </div>
        <div v-else class="product-listing__grid">
          <ProductCard v-for="p in filtered.slice(0, 8)" :key="p.id" :product="p" />
        </div>
      </div>
    </section>

    <!-- Blog Section -->
    <section v-if="recentPosts.length" class="border-b border-border">
      <SectionHeader title="آخرین مقالات" tag="بلاگ" to="/blog" link-label="همه مقالات" />
      <div class="px-[5vw] pb-14">
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          <BlogCard v-for="post in recentPosts" :key="post.slug" :post="post" />
        </div>
      </div>
    </section>

    <!-- Manifesto -->
    <section v-if="contentStore.content.about.mission" class="border-b border-border bg-foreground text-background">
      <div class="mx-auto max-w-4xl px-6 py-32 text-center">
        <p class="text-2xl font-light leading-relaxed md:text-4xl">
          {{ contentStore.content.about.mission }}
        </p>
        <div class="mt-8 text-xs uppercase tracking-[0.3em] opacity-60">{{ contentStore.content.about.vision }}</div>
      </div>
    </section>

    <!-- Three pillars / Values -->
    <section v-if="contentStore.content.about.values.length">
      <div class="mx-auto grid max-w-7xl gap-px bg-border md:grid-cols-3">
        <div
          v-for="(x, xi) in contentStore.content.about.values"
          :key="xi"
          class="bg-background p-12"
        >
          <div class="text-xs text-maroon">{{ String(xi + 1).padStart(2, '۰') }}</div>
          <h3 class="mt-4 text-xl font-medium">{{ x.title }}</h3>
          <p class="mt-3 text-sm leading-7 text-muted-foreground">{{ x.description }}</p>
        </div>
      </div>
    </section>
  </TheLayout>
</template>

<style scoped>
.product-listing {
  padding: 2rem 5vw 5rem;
}
.product-listing__grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2.5rem 1.5rem;
}
@media (max-width: 1024px) {
  .product-listing__grid { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 768px) {
  .product-listing__grid { grid-template-columns: repeat(2, 1fr); gap: 1.5rem 1rem; }
}
</style>
