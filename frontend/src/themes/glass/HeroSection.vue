<script setup>
import { RouterLink } from 'vue-router';
defineProps({
  image:    { type: String, default: null },
  title:    { type: String, default: '' },
  subtitle: { type: String, default: '' },
});
</script>

<template>
  <section class="gl-hero">
    <div v-if="image" class="gl-hero__media">
      <img :src="image" :alt="title" class="gl-hero__img" />
      <div class="gl-hero__img-overlay" />
    </div>
    <div v-else class="gl-hero__media gl-hero__media--empty" />

    <div class="gl-hero__content">
      <div class="gl-hero__panel">
        <p class="gl-hero__eyebrow">مجموعه ۱۴۰۳</p>
        <h1 class="gl-hero__title">{{ title }}</h1>
        <p v-if="subtitle" class="gl-hero__subtitle">{{ subtitle }}</p>
        <RouterLink to="/products" class="gl-hero__cta">
          مشاهده محصولات
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M12 8H4M8 4L4 8L8 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.gl-hero {
  position: relative;
  min-height: 82vh;
  display: flex;
  align-items: center;
  overflow: hidden;
}
.gl-hero__media {
  position: absolute;
  inset: 0;
}
.gl-hero__media--empty {
  background: transparent;
}
.gl-hero__img {
  width: 100%; height: 100%;
  object-fit: cover;
  opacity: 0.22;
  filter: blur(2px) saturate(0.6);
}
.gl-hero__img-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(135deg,
    rgba(120,80,255,0.15) 0%,
    rgba(255,100,180,0.10) 50%,
    rgba(80,200,200,0.10) 100%
  );
}
.gl-hero__content {
  position: relative;
  z-index: 2;
  width: 100%;
  padding: 3rem 5vw;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}
.gl-hero__panel {
  max-width: 560px;
  padding: 2.5rem 2.75rem;
  background: rgba(255,255,255,0.52);
  backdrop-filter: blur(32px) saturate(200%);
  -webkit-backdrop-filter: blur(32px) saturate(200%);
  border: 1px solid rgba(255,255,255,0.72);
  border-radius: 1.5rem;
  box-shadow:
    inset 0 2px 0 rgba(255,255,255,0.8),
    0 24px 64px rgba(100,60,220,0.14),
    0 4px 16px rgba(0,0,0,0.06);
}
.gl-hero__eyebrow {
  font-size: 0.72rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: oklch(0.46 0.22 278);
  margin-bottom: 1rem;
  font-weight: 500;
}
.gl-hero__title {
  font-size: clamp(2rem, 5vw, 3.8rem);
  font-weight: 300;
  color: #18103a;
  line-height: 1.18;
  margin: 0 0 1rem;
  letter-spacing: -0.02em;
}
.gl-hero__subtitle {
  font-size: 0.95rem;
  color: rgba(20,10,60,0.6);
  line-height: 1.75;
  margin-bottom: 2rem;
  max-width: 400px;
  font-weight: 300;
}
.gl-hero__cta {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.65rem 1.4rem;
  background: oklch(0.46 0.22 278);
  color: white;
  font-size: 0.85rem;
  font-weight: 500;
  text-decoration: none;
  border-radius: 9999px;
  box-shadow: 0 4px 16px rgba(100,60,220,0.35);
  transition: all 0.2s;
}
.gl-hero__cta:hover {
  opacity: 0.88;
  gap: 0.9rem;
  box-shadow: 0 8px 24px rgba(100,60,220,0.45);
}
</style>
