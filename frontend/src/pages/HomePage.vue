<template>
  <main class="home" dir="rtl">
    <!-- Hero -->
    <HeroSection
      :image="page?.hero_image"
      :title="page?.hero_title || page?.title || 'کلکسیون امسال'"
      :subtitle="page?.hero_subtitle"
    />

    <!-- Featured 4 tiles -->
    <template v-if="featured.length">
      <SectionHeader
        title="محصولات برگزیده"
        tag="ویژه"
        to="/all-products"
      />
      <FeaturedGrid :items="featured" />
    </template>

    <!-- All products -->
    <SectionHeader
      title="همه محصولات"
      to="/all-products"
    />
    <ProductGrid :items="products" />

    <!-- Editorial content -->
    <HomeContent :html="page?.body_html" />
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/utils/api'

import HeroSection from '@/components/HeroSection.vue'
import SectionHeader from '@/components/SectionHeader.vue'
import FeaturedGrid from '@/components/FeaturedGrid.vue'
import ProductGrid from '@/components/ProductGrid.vue'
import HomeContent from '@/components/HomeContent.vue'

const products = ref([])
const featured = ref([])
const page = ref(null)

onMounted(async () => {
  page.value = await api.getSitePage('home').catch(() => null)
  const filters = page.value?.featured_category ? { category: page.value.featured_category } : {}
  const res = await api.listProducts(filters, 'default', 1)
  products.value = res.items || []
  featured.value = (res.items || []).slice(0, 4)
})
</script>

<style>
/* ── Global tokens ── */
:root {
  --color-bg: #FAFAF8;
  --color-surface: #F5F3F0;
  --color-border: #E8E4DE;
  --color-text: #111111;
  --color-muted: #6b6560;
  --color-faint: #9e9890;
  --color-accent: #800000;   /* maroon — used sparingly */

  --font-persian: 'Vazirmatn', sans-serif;

  --page-h-pad: 5vw;
}

/* ── Import Vazirmatn (Persian) ── */
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@200;300;400;500&display=swap');

/* ── Base reset for this page ── */
.home {
  background-color: var(--color-bg);
  color: var(--color-text);
  min-height: 100vh;
  font-family: var(--font-persian);
  -webkit-font-smoothing: antialiased;
}

*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

img {
  display: block;
  max-width: 100%;
}

a {
  color: inherit;
}
</style>
