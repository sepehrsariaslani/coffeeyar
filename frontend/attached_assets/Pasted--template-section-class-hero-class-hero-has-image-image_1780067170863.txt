<template>
  <section class="hero" :class="{ 'hero--has-image': !!image }">
    <div v-if="image" class="hero__media">
      <img :src="image" :alt="title" class="hero__img" />
      <div class="hero__overlay" />
    </div>

    <div class="hero__content" :class="{ 'hero__content--over-image': !!image }">
      <p class="hero__eyebrow">کلکسیون جدید</p>
      <h1 class="hero__title">{{ title }}</h1>
      <p v-if="subtitle" class="hero__subtitle">{{ subtitle }}</p>
      <RouterLink to="/all-products" class="hero__cta">
        <span>مشاهده محصولات</span>
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M12 8H4M8 4L4 8L8 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </RouterLink>
    </div>
  </section>
</template>

<script setup>
defineProps({
  image: { type: String, default: null },
  title: { type: String, default: '' },
  subtitle: { type: String, default: '' },
})
</script>

<style scoped>
.hero {
  position: relative;
  min-height: 72vh;
  display: flex;
  align-items: flex-end;
  background-color: #F5F3F0;
  overflow: hidden;
  border-bottom: 1px solid #E8E4DE;
}

.hero--has-image {
  background-color: #1a1a1a;
}

.hero__media {
  position: absolute;
  inset: 0;
}

.hero__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.75;
}

.hero__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(10,10,10,0.65) 0%, transparent 55%);
}

.hero__content {
  position: relative;
  z-index: 1;
  padding: 4rem 5vw;
  max-width: 640px;
}

.hero__content--over-image .hero__eyebrow,
.hero__content--over-image .hero__title,
.hero__content--over-image .hero__subtitle {
  color: #fff;
}

.hero__eyebrow {
  font-size: 0.75rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #7a7166;
  margin-bottom: 1rem;
  font-family: 'Vazirmatn', sans-serif;
}

.hero__title {
  font-family: 'Vazirmatn', sans-serif;
  font-size: clamp(2.4rem, 6vw, 4.5rem);
  font-weight: 300;
  color: #111;
  line-height: 1.15;
  margin: 0 0 1rem;
  letter-spacing: -0.02em;
}

.hero__subtitle {
  font-size: 1rem;
  color: #6b6560;
  line-height: 1.7;
  margin-bottom: 2.5rem;
  max-width: 420px;
  font-family: 'Vazirmatn', sans-serif;
  font-weight: 300;
}

.hero__cta {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.875rem;
  letter-spacing: 0.06em;
  color: #800000;
  text-decoration: none;
  border-bottom: 1px solid #800000;
  padding-bottom: 2px;
  transition: gap 0.25s ease;
}

.hero__cta:hover {
  gap: 1rem;
}

.hero__content--over-image .hero__cta {
  color: #fff;
  border-bottom-color: rgba(255,255,255,0.6);
}
</style>
