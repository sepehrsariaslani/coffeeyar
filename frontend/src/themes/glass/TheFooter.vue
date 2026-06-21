<script setup>
import { RouterLink } from "vue-router";
import { Instagram, Send, MapPin, Phone, Mail } from "lucide-vue-next";
import { useSiteSettingsStore } from "@/stores/siteSettings.js";
const s = useSiteSettingsStore().settings;
</script>

<template>
  <footer class="gl-footer" dir="rtl">
    <div class="gl-footer__inner">
      <div class="gl-footer__brand">
        <div class="gl-footer__logo">{{ s.shopName || 'نـوار' }}<span class="gl-footer__dot">.</span></div>
        <p class="gl-footer__desc">{{ s.description }}</p>
        <div class="gl-footer__contact">
          <a v-if="s.phone" :href="`tel:${s.phone}`" class="gl-footer__contact-item"><Phone class="h-3.5 w-3.5" /> {{ s.phone }}</a>
          <a v-if="s.email" :href="`mailto:${s.email}`" class="gl-footer__contact-item"><Mail class="h-3.5 w-3.5" /> {{ s.email }}</a>
        </div>
        <div class="gl-footer__social">
          <a :href="s.instagram || '#'" class="gl-social-btn"><Instagram class="h-4 w-4" /></a>
          <a :href="s.telegram || '#'" class="gl-social-btn"><Send class="h-4 w-4" /></a>
        </div>
      </div>

      <div class="gl-footer__links-col">
        <h4 class="gl-footer__col-title">پیمایش</h4>
        <nav class="gl-footer__nav">
          <RouterLink to="/products" class="gl-footer__link">محصولات</RouterLink>
          <RouterLink to="/about" class="gl-footer__link">درباره ما</RouterLink>
          <RouterLink to="/blog" class="gl-footer__link">بلاگ</RouterLink>
          <RouterLink to="/faq" class="gl-footer__link">سوالات</RouterLink>
          <RouterLink to="/tracking" class="gl-footer__link">پیگیری سفارش</RouterLink>
          <RouterLink to="/contact" class="gl-footer__link">تماس با ما</RouterLink>
        </nav>
      </div>
    </div>

    <div class="gl-footer__bottom">
      <span>© {{ new Date().getFullYear() }} {{ s.shopName || 'نوار' }}</span>
    </div>
  </footer>
</template>

<style scoped>
.gl-footer {
  background: rgba(255,255,255,0.35);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border-top: 1px solid rgba(255,255,255,0.55);
  margin-bottom: 4rem;
}
@media (min-width: 768px) { .gl-footer { margin-bottom: 0; } }
.gl-footer__inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 3rem 2rem;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 3rem;
}
@media (max-width: 640px) { .gl-footer__inner { grid-template-columns: 1fr; } }
.gl-footer__logo { font-size: 1.3rem; font-weight: 600; color: #18103a; margin-bottom: 0.5rem; }
.gl-footer__dot { color: oklch(0.46 0.22 278); }
.gl-footer__desc { font-size: 0.82rem; color: rgba(20,10,60,0.55); line-height: 1.75; max-width: 280px; margin-bottom: 1rem; }
.gl-footer__contact { display: flex; flex-direction: column; gap: 0.4rem; margin-bottom: 1rem; }
.gl-footer__contact-item { display: flex; align-items: center; gap: 0.5rem; font-size: 0.78rem; color: rgba(20,10,60,0.55); text-decoration: none; transition: color 0.2s; }
.gl-footer__contact-item:hover { color: oklch(0.46 0.22 278); }
.gl-footer__social { display: flex; gap: 0.5rem; }
.gl-social-btn {
  display: flex; align-items: center; justify-content: center;
  width: 34px; height: 34px;
  background: rgba(255,255,255,0.5);
  border: 1px solid rgba(255,255,255,0.7);
  border-radius: 50%;
  color: rgba(20,10,60,0.6);
  text-decoration: none;
  transition: all 0.2s;
}
.gl-social-btn:hover { background: rgba(255,255,255,0.75); color: oklch(0.46 0.22 278); }
.gl-footer__col-title { font-size: 0.68rem; letter-spacing: 0.15em; text-transform: uppercase; color: rgba(20,10,60,0.4); margin-bottom: 1rem; }
.gl-footer__nav { display: flex; flex-direction: column; gap: 0.55rem; }
.gl-footer__link { font-size: 0.82rem; color: rgba(20,10,60,0.6); text-decoration: none; transition: color 0.2s; }
.gl-footer__link:hover { color: oklch(0.38 0.20 278); }
.gl-footer__bottom {
  border-top: 1px solid rgba(255,255,255,0.5);
  padding: 0.9rem 2rem;
  text-align: center;
  font-size: 0.72rem;
  color: rgba(20,10,60,0.4);
  max-width: 1280px;
  margin: 0 auto;
}
</style>
