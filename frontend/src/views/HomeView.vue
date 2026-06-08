<script setup>
import { ref, computed } from "vue";
import { RouterLink } from "vue-router";
import TheLayout from "@/components/site/TheLayout.vue";
import HeroSection from "@/components/HeroSection.vue";
import FeaturedGrid from "@/components/FeaturedGrid.vue";
import SectionHeader from "@/components/SectionHeader.vue";
import ProductCard from "@/components/ProductCard.vue";
import BrandsMarquee from "@/components/BrandsMarquee.vue";
import BlogCard from "@/components/BlogCard.vue";
import { products, posts } from "@/lib/data.js";
import { useGroupsStore } from "@/stores/groups.js";
import { useSeo } from "@/composables/useSeo.js";
import heroImg from "@/assets/hero-coffee.jpg";

useSeo({
  title: "نوار — قهوه تخصصی",
  description: "دانه‌های تک‌خاستگاه از مزارع شناخته‌شده. تازه برشته‌شده در کارگاه کوچک ما. ارسال به سراسر ایران.",
});

const groupsStore = useGroupsStore();
const coffeeProducts = products.filter((p) => p.type === "coffee");

const categories = [
  { label: "همه", value: "all" },
  { label: "رست روشن", value: "روشن" },
  { label: "رست متوسط", value: "متوسط" },
  { label: "رست تیره", value: "تیره" },
];

const activeCategory = ref("all");

const filtered = computed(() =>
  activeCategory.value === "all"
    ? coffeeProducts
    : coffeeProducts.filter((p) => p.roast === activeCategory.value)
);

const typeIcon = { coffee: "☕", accessory: "🫙", equipment: "⚙️", other: "📦" };
</script>

<template>
  <TheLayout>
    <!-- Hero -->
    <HeroSection
      :image="heroImg"
      title="قهوه‌ای که می‌خواستی."
      subtitle="ما دانه‌های تک‌خاستگاه را از مزارع شناخته‌شده تهیه می‌کنیم و در کارگاه کوچک خود تازه برشته می‌کنیم."
    />

    <!-- Brands Marquee -->
    <BrandsMarquee />

    <!-- Product Groups / Categories Section -->
    <section class="border-b border-border">
      <SectionHeader title="دسته‌بندی‌ها" tag="گروه‌های محصول" />
      <div class="px-[5vw] pb-12">
        <div v-if="groupsStore.groups.length" class="grid grid-cols-2 gap-3 md:grid-cols-4">
          <RouterLink
            v-for="g in groupsStore.groups"
            :key="g.id"
            to="/products"
            class="group relative border border-border bg-muted/20 p-5 hover:border-maroon hover:bg-maroon/5 transition-all duration-200"
          >
            <div class="text-2xl mb-3">{{ typeIcon[g.type] || "📦" }}</div>
            <div class="font-medium text-sm leading-snug">{{ g.name }}</div>
            <div class="mt-1.5 text-xs text-muted-foreground line-clamp-2 leading-relaxed">{{ g.description }}</div>
            <div class="mt-4 flex items-center gap-1 text-xs text-muted-foreground group-hover:text-maroon transition-colors">
              <span>مشاهده</span>
              <svg width="12" height="12" viewBox="0 0 16 16" fill="none" class="shrink-0">
                <path d="M12 8H4M8 4L4 8L8 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="mt-3 flex flex-wrap gap-1">
              <span v-if="g.attributes?.length" class="border border-border px-1.5 py-0.5 text-[10px] text-muted-foreground">{{ g.attributes.length }} ویژگی</span>
              <span v-if="g.weights?.length" class="border border-border px-1.5 py-0.5 text-[10px] text-muted-foreground">{{ g.weights.length }} وزن</span>
            </div>
          </RouterLink>
        </div>
        <div v-else class="border border-dashed border-border py-12 text-center text-sm text-muted-foreground">
          هنوز دسته‌بندی‌ای تعریف نشده است.
          <RouterLink to="/admin/groups" class="mr-1 text-maroon hover:underline">ایجاد دسته‌بندی</RouterLink>
        </div>
      </div>
    </section>

    <!-- Featured grid -->
    <div class="border-b border-border">
      <SectionHeader title="محصولات ویژه" tag="منتخب" to="/products" />
      <FeaturedGrid :items="coffeeProducts" />
    </div>

    <!-- Category tabs + product listing -->
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
        <div v-if="filtered.length === 0" class="py-20 text-center text-muted-foreground">
          محصولی در این دسته‌بندی وجود ندارد.
        </div>
        <div v-else class="product-listing__grid">
          <ProductCard v-for="p in filtered" :key="p.id" :product="p" />
        </div>
      </div>
    </section>

    <!-- Blog Section -->
    <section class="border-b border-border">
      <SectionHeader title="آخرین مقالات" tag="بلاگ" to="/blog" link-label="همه مقالات" />
      <div class="px-[5vw] pb-14">
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          <BlogCard v-for="post in posts.slice(0, 3)" :key="post.slug" :post="post" />
        </div>
      </div>
    </section>

    <!-- Manifesto -->
    <section class="border-b border-border bg-foreground text-background">
      <div class="mx-auto max-w-4xl px-6 py-32 text-center">
        <p class="text-2xl font-light leading-relaxed md:text-4xl">
          "قهوه‌ی خوب از <span class="text-maroon">صبر</span> ساخته می‌شود، نه از سرعت."
        </p>
        <div class="mt-8 text-xs uppercase tracking-[0.3em] opacity-60">فلسفه‌ی ما</div>
      </div>
    </section>

    <!-- Three pillars -->
    <section>
      <div class="mx-auto grid max-w-7xl gap-px bg-border md:grid-cols-3">
        <div
          v-for="x in [
            { n: '۰۱', t: 'منشأ شفاف', d: 'هر دانه تا مزرعه‌ی تولید قابل ردیابی است.' },
            { n: '۰۲', t: 'برشته‌ی تازه', d: 'حداکثر ۴۸ ساعت قبل از ارسال برشته می‌شود.' },
            { n: '۰۳', t: 'ارسال سریع', d: 'ارسال به سراسر ایران در کمتر از ۴۸ ساعت.' },
          ]"
          :key="x.n"
          class="bg-background p-12"
        >
          <div class="text-xs text-maroon">{{ x.n }}</div>
          <h3 class="mt-4 text-xl font-medium">{{ x.t }}</h3>
          <p class="mt-3 text-sm leading-7 text-muted-foreground">{{ x.d }}</p>
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
