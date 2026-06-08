<script setup>
import { computed } from "vue";
import { RouterLink } from 'vue-router';
import { useLayoutStore } from "@/stores/layout.js";

defineProps({
  image:    { type: String, default: null },
  title:    { type: String, default: '' },
  subtitle: { type: String, default: '' },
});

const layoutStore = useLayoutStore();
const variant = computed(() => layoutStore.heroVariant);
</script>

<template>
  <!-- ── Variant 1: Overlay ──────────────────────────── -->
  <section v-if="variant === 1" class="hero" :class="{ 'hero--has-image': !!image }">
    <div v-if="image" class="hero__media">
      <img :src="image" :alt="title" class="hero__img" />
      <div class="hero__overlay" />
    </div>
    <div class="hero__content" :class="{ 'hero__content--over-image': !!image }">
      <p class="hero__eyebrow">مجموعه ۱۴۰۳</p>
      <h1 class="hero__title">{{ title }}</h1>
      <p v-if="subtitle" class="hero__subtitle">{{ subtitle }}</p>
      <RouterLink to="/products" class="hero__cta">
        <span>مشاهده محصولات</span>
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M12 8H4M8 4L4 8L8 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </RouterLink>
    </div>
  </section>

  <!-- ── Variant 2: Split ───────────────────────────── -->
  <section v-else-if="variant === 2" class="hero-split" dir="rtl">
    <div class="hero-split__text">
      <p class="hero-split__eyebrow">مجموعه ۱۴۰۳</p>
      <h1 class="hero-split__title">{{ title }}</h1>
      <p v-if="subtitle" class="hero-split__sub">{{ subtitle }}</p>
      <RouterLink to="/products" class="hero-split__cta">
        <span>مشاهده محصولات</span>
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M12 8H4M8 4L4 8L8 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </RouterLink>
    </div>
    <div class="hero-split__media">
      <img v-if="image" :src="image" :alt="title" class="hero-split__img" />
      <div v-else class="hero-split__placeholder" />
    </div>
  </section>

  <!-- ── Variant 3: Diagonal ───────────────────────── -->
  <section v-else class="hero-diag" :class="{ 'hero-diag--has-image': !!image }">
    <div v-if="image" class="hero-diag__media">
      <img :src="image" :alt="title" class="hero-diag__img" />
    </div>
    <div class="hero-diag__shade" />
    <div class="hero-diag__content">
      <p class="hero-diag__eyebrow">مجموعه ۱۴۰۳</p>
      <h1 class="hero-diag__title">{{ title }}</h1>
      <p v-if="subtitle" class="hero-diag__sub">{{ subtitle }}</p>
      <RouterLink to="/products" class="hero-diag__cta">
        مشاهده محصولات
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M12 8H4M8 4L4 8L8 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </RouterLink>
    </div>
    <div class="hero-diag__slice" />
  </section>
</template>

<style scoped>
.hero { position: relative; min-height: 72vh; display: flex; align-items: flex-end; background-color: #F5F3F0; overflow: hidden; border-bottom: 1px solid #E8E4DE; }
.hero--has-image { background-color: #1a1a1a; }
.hero__media { position: absolute; inset: 0; }
.hero__img { width: 100%; height: 100%; object-fit: cover; opacity: 0.75; }
.hero__overlay { position: absolute; inset: 0; background: linear-gradient(to top, rgba(10,10,10,0.65) 0%, transparent 55%); }
.hero__content { position: relative; z-index: 1; padding: 4rem 5vw; max-width: 640px; }
.hero__content--over-image .hero__eyebrow,
.hero__content--over-image .hero__title,
.hero__content--over-image .hero__subtitle { color: #fff; }
.hero__eyebrow { font-size: 0.75rem; letter-spacing: 0.18em; text-transform: uppercase; color: #7a7166; margin-bottom: 1rem; }
.hero__title { font-size: clamp(2.4rem, 6vw, 4.5rem); font-weight: 300; color: #111; line-height: 1.15; margin: 0 0 1rem; letter-spacing: -0.02em; }
.hero__subtitle { font-size: 1rem; color: #6b6560; line-height: 1.7; margin-bottom: 2.5rem; max-width: 420px; font-weight: 300; }
.hero__cta { display: inline-flex; align-items: center; gap: 0.6rem; font-size: 0.875rem; letter-spacing: 0.06em; color: #800000; text-decoration: none; border-bottom: 1px solid #800000; padding-bottom: 2px; transition: gap 0.25s ease; }
.hero__cta:hover { gap: 1rem; }
.hero__content--over-image .hero__cta { color: #fff; border-bottom-color: rgba(255,255,255,0.6); }

.hero-split { display: grid; grid-template-columns: 1fr 1fr; min-height: 72vh; overflow: hidden; }
@media (max-width: 768px) { .hero-split { grid-template-columns: 1fr; min-height: auto; } .hero-split__media { height: 50vw; min-height: 260px; } }
.hero-split__text { display: flex; flex-direction: column; justify-content: center; padding: 5rem 5vw; background-color: #F5F3F0; border-bottom: 1px solid #E8E4DE; }
.hero-split__media { position: relative; overflow: hidden; }
.hero-split__img { width: 100%; height: 100%; object-fit: cover; }
.hero-split__placeholder { width: 100%; height: 100%; background: linear-gradient(135deg, #E8E4DE, #D5CFC8); }
.hero-split__eyebrow { font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase; color: #7a7166; margin-bottom: 1.25rem; }
.hero-split__title { font-size: clamp(2rem, 4vw, 3.5rem); font-weight: 300; color: #111; line-height: 1.2; margin: 0 0 1rem; letter-spacing: -0.02em; }
.hero-split__sub { font-size: 0.95rem; color: #6b6560; line-height: 1.75; margin-bottom: 2.5rem; max-width: 380px; font-weight: 300; }
.hero-split__cta { display: inline-flex; align-items: center; gap: 0.6rem; font-size: 0.875rem; letter-spacing: 0.06em; color: #800000; text-decoration: none; border-bottom: 1px solid #800000; padding-bottom: 2px; transition: gap 0.25s ease; width: fit-content; }
.hero-split__cta:hover { gap: 1rem; }
.hero-split__media::before { content: ''; position: absolute; inset: 0; background: linear-gradient(to left, transparent 70%, #F5F3F0 100%); z-index: 1; }

.hero-diag { position: relative; min-height: 72vh; display: flex; align-items: flex-end; overflow: hidden; background-color: #1a1a1a; }
.hero-diag__media { position: absolute; inset: 0; }
.hero-diag__img { width: 100%; height: 100%; object-fit: cover; opacity: 0.5; }
.hero-diag__shade { position: absolute; inset: 0; background: linear-gradient(120deg, rgba(10,10,10,0.82) 40%, rgba(10,10,10,0.2) 100%); }
.hero-diag__content { position: relative; z-index: 2; padding: 4rem 5vw; max-width: 580px; color: #fff; }
.hero-diag__eyebrow { font-size: 0.7rem; letter-spacing: 0.22em; text-transform: uppercase; color: rgba(255,255,255,0.5); margin-bottom: 1.25rem; }
.hero-diag__title { font-size: clamp(2.4rem, 6vw, 4.5rem); font-weight: 300; color: #fff; line-height: 1.15; margin: 0 0 1rem; letter-spacing: -0.02em; }
.hero-diag__sub { font-size: 1rem; color: rgba(255,255,255,0.65); line-height: 1.7; margin-bottom: 2.5rem; max-width: 420px; font-weight: 300; }
.hero-diag__cta { display: inline-flex; align-items: center; gap: 0.6rem; font-size: 0.875rem; letter-spacing: 0.06em; color: #fff; text-decoration: none; border-bottom: 1px solid rgba(255,255,255,0.45); padding-bottom: 2px; transition: gap 0.25s ease; }
.hero-diag__cta:hover { gap: 1rem; border-bottom-color: #fff; }
.hero-diag__slice { position: absolute; top: 0; bottom: 0; right: 0; width: 45%; background: transparent; clip-path: polygon(30% 0, 100% 0, 100% 100%, 0% 100%); z-index: 1; pointer-events: none; }
</style>
