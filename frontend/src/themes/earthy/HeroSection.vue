<script setup>
import { RouterLink } from 'vue-router';
defineProps({ image: { type: String, default: null }, title: { type: String, default: '' }, subtitle: { type: String, default: '' }, eyebrow: { type: String, default: 'مجموعه ۱۴۰۳' }, ctaLabel: { type: String, default: 'مشاهده محصولات' } });
</script>

<template>
  <section class="ea-hero">
    <div v-if="image" class="ea-hero__media">
      <img :src="image" :alt="title" class="ea-hero__img" />
      <div class="ea-hero__overlay" />
    </div>
    <div v-else class="ea-hero__media ea-hero__media--empty" />
    <div class="ea-hero__content">
      <p class="ea-hero__eyebrow">{{ eyebrow }}</p>
      <h1 class="ea-hero__title">{{ title }}</h1>
      <p v-if="subtitle" class="ea-hero__sub">{{ subtitle }}</p>
      <RouterLink to="/products" class="ea-hero__cta">
        {{ ctaLabel }}
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M12 8H4M8 4L4 8L8 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </RouterLink>
    </div>
    <div class="ea-hero__wave" />
  </section>
</template>

<style scoped>
.ea-hero { position: relative; min-height: 78vh; display: flex; align-items: flex-end; overflow: hidden; background-color: #3b2e1e; }
.ea-hero__media { position: absolute; inset: 0; }
.ea-hero__media--empty { background: linear-gradient(160deg, #4a3728 0%, #2d2010 100%); }
.ea-hero__img { width: 100%; height: 100%; object-fit: cover; opacity: 0.5; filter: saturate(0.7) brightness(0.75); }
.ea-hero__overlay { position: absolute; inset: 0; background: linear-gradient(to top, rgba(20,12,5,0.85) 0%, rgba(20,12,5,0.25) 60%, transparent 100%); }
.ea-hero__content { position: relative; z-index: 2; padding: 4rem 5vw; max-width: 620px; }
.ea-hero__eyebrow { font-size: 0.72rem; letter-spacing: 0.22em; text-transform: uppercase; color: #a8c5a0; margin-bottom: 1rem; font-weight: 500; }
.ea-hero__title { font-size: clamp(2.4rem, 6vw, 4.5rem); font-weight: 300; color: rgba(255,245,230,0.95); line-height: 1.15; margin: 0 0 1rem; letter-spacing: -0.02em; }
.ea-hero__sub { font-size: 1rem; color: rgba(255,245,230,0.55); line-height: 1.75; margin-bottom: 2.5rem; max-width: 420px; font-weight: 300; }
.ea-hero__cta { display: inline-flex; align-items: center; gap: 0.6rem; padding: 0.7rem 1.5rem; background: #4a7c59; color: #fff; font-size: 0.875rem; font-weight: 600; text-decoration: none; border-radius: 9999px; transition: all 0.2s; box-shadow: 0 4px 16px rgba(74,124,89,0.4); }
.ea-hero__cta:hover { background: #3d6b4a; gap: 0.9rem; }
.ea-hero__wave {
  position: absolute; bottom: 0; left: 0; right: 0; height: 80px;
  background: #F5F0E8;
  clip-path: ellipse(55% 100% at 50% 100%);
  pointer-events: none; z-index: 1;
}
</style>
