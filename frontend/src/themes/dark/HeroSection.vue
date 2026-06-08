<script setup>
import { RouterLink } from 'vue-router';
defineProps({
  image:    { type: String, default: null },
  title:    { type: String, default: '' },
  subtitle: { type: String, default: '' },
  eyebrow:  { type: String, default: 'مجموعه ۱۴۰۳' },
  ctaLabel: { type: String, default: 'مشاهده محصولات' },
});
</script>

<template>
  <section class="dk-hero">
    <div v-if="image" class="dk-hero__media">
      <img :src="image" :alt="title" class="dk-hero__img" />
    </div>
    <div class="dk-hero__shade" />
    <div class="dk-hero__glow" />
    <div class="dk-hero__content">
      <p class="dk-hero__eyebrow">{{ eyebrow }}</p>
      <h1 class="dk-hero__title">{{ title }}</h1>
      <p v-if="subtitle" class="dk-hero__sub">{{ subtitle }}</p>
      <RouterLink to="/products" class="dk-hero__cta">
        {{ ctaLabel }}
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M12 8H4M8 4L4 8L8 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </RouterLink>
    </div>
  </section>
</template>

<style scoped>
.dk-hero {
  position: relative; min-height: 80vh;
  display: flex; align-items: flex-end;
  overflow: hidden; background-color: #0d0d0d;
}
.dk-hero__media { position: absolute; inset: 0; }
.dk-hero__img { width: 100%; height: 100%; object-fit: cover; opacity: 0.35; filter: grayscale(0.3) brightness(0.7); }
.dk-hero__shade {
  position: absolute; inset: 0;
  background: linear-gradient(to top, rgba(5,5,5,0.92) 0%, rgba(5,5,5,0.4) 50%, rgba(5,5,5,0.15) 100%);
}
.dk-hero__glow {
  position: absolute; inset: 0;
  background: radial-gradient(ellipse 60% 40% at 20% 90%, rgba(201,146,63,0.12), transparent 60%);
  pointer-events: none;
}
.dk-hero__content {
  position: relative; z-index: 2;
  padding: 4rem 5vw; max-width: 640px; color: #fff;
}
.dk-hero__eyebrow {
  font-size: 0.72rem; letter-spacing: 0.22em; text-transform: uppercase;
  color: #C9923F; margin-bottom: 1rem; font-weight: 500;
}
.dk-hero__title {
  font-size: clamp(2.4rem, 6vw, 4.5rem); font-weight: 300;
  color: rgba(255,255,255,0.93); line-height: 1.15;
  margin: 0 0 1rem; letter-spacing: -0.02em;
}
.dk-hero__sub {
  font-size: 1rem; color: rgba(255,255,255,0.5); line-height: 1.75;
  margin-bottom: 2.5rem; max-width: 420px; font-weight: 300;
}
.dk-hero__cta {
  display: inline-flex; align-items: center; gap: 0.6rem;
  padding: 0.7rem 1.5rem;
  background: #C9923F; color: #0d0d0d;
  font-size: 0.875rem; font-weight: 700;
  text-decoration: none; border-radius: 4px;
  transition: all 0.2s;
  box-shadow: 0 4px 20px rgba(201,146,63,0.35);
}
.dk-hero__cta:hover { background: #dba44f; box-shadow: 0 8px 28px rgba(201,146,63,0.45); }
</style>
