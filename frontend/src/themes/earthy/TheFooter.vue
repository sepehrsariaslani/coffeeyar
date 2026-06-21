<script setup>
import { RouterLink } from "vue-router";
import { Instagram, Send, Phone, Mail, MapPin } from "lucide-vue-next";
import { useSiteSettingsStore } from "@/stores/siteSettings.js";
const s = useSiteSettingsStore().settings;
</script>

<template>
  <footer class="ea-footer" dir="rtl">
    <div class="ea-footer__inner">
      <div class="ea-footer__brand">
        <div class="ea-footer__logo">🌿 {{ s.shopName || 'نـوار' }}<span class="ea-footer__dot">.</span></div>
        <p class="ea-footer__desc">{{ s.description }}</p>
        <div class="ea-footer__contact">
          <a v-if="s.phone" :href="`tel:${s.phone}`" class="ea-footer__contact-item"><Phone class="h-3.5 w-3.5" />{{ s.phone }}</a>
          <a v-if="s.email" :href="`mailto:${s.email}`" class="ea-footer__contact-item"><Mail class="h-3.5 w-3.5" />{{ s.email }}</a>
          <span v-if="s.address" class="ea-footer__contact-item"><MapPin class="h-3.5 w-3.5 shrink-0" />{{ s.address }}</span>
        </div>
        <div class="ea-footer__social">
          <a :href="s.instagram || '#'" class="ea-social"><Instagram class="h-4 w-4" /></a>
          <a :href="s.telegram || '#'" class="ea-social"><Send class="h-4 w-4" /></a>
        </div>
      </div>
      <div class="ea-footer__col">
        <h4 class="ea-footer__col-title">پیمایش</h4>
        <nav class="ea-footer__nav">
          <RouterLink to="/products" class="ea-footer__link">محصولات</RouterLink>
          <RouterLink to="/about" class="ea-footer__link">درباره ما</RouterLink>
          <RouterLink to="/blog" class="ea-footer__link">بلاگ</RouterLink>
          <RouterLink to="/faq" class="ea-footer__link">سوالات</RouterLink>
          <RouterLink to="/tracking" class="ea-footer__link">پیگیری سفارش</RouterLink>
          <RouterLink to="/contact" class="ea-footer__link">تماس با ما</RouterLink>
        </nav>
      </div>
    </div>
    <div class="ea-footer__bottom">
      <span>© {{ new Date().getFullYear() }} {{ s.shopName || 'نوار' }}. تمام حقوق محفوظ است.</span>
    </div>
  </footer>
</template>

<style scoped>
.ea-footer { background-color: #EDE5D6; border-top: 1.5px solid #D6CBB8; margin-bottom: 4rem; }
@media (min-width: 768px) { .ea-footer { margin-bottom: 0; } }
.ea-footer__inner { max-width: 1280px; margin: 0 auto; padding: 3rem 2rem; display: grid; grid-template-columns: 1fr auto; gap: 3rem; }
@media (max-width: 640px) { .ea-footer__inner { grid-template-columns: 1fr; } }
.ea-footer__logo { font-size: 1.25rem; font-weight: 600; color: #2d2416; margin-bottom: 0.5rem; }
.ea-footer__dot { color: #4a7c59; }
.ea-footer__desc { font-size: 0.82rem; color: #7a6852; line-height: 1.75; max-width: 280px; margin-bottom: 1rem; }
.ea-footer__contact { display: flex; flex-direction: column; gap: 0.4rem; margin-bottom: 1rem; }
.ea-footer__contact-item { display: flex; align-items: center; gap: 0.5rem; font-size: 0.78rem; color: #7a6852; text-decoration: none; transition: color 0.2s; }
.ea-footer__contact-item:hover { color: #4a7c59; }
.ea-footer__social { display: flex; gap: 0.5rem; }
.ea-social { display: flex; align-items: center; justify-content: center; width: 34px; height: 34px; background: #F5F0E8; border: 1.5px solid #D6CBB8; border-radius: 50%; color: #7a6852; text-decoration: none; transition: all 0.2s; }
.ea-social:hover { background: #4a7c59; color: white; border-color: #4a7c59; }
.ea-footer__col-title { font-size: 0.68rem; letter-spacing: 0.15em; text-transform: uppercase; color: #9e8a72; margin-bottom: 1rem; }
.ea-footer__nav { display: flex; flex-direction: column; gap: 0.55rem; }
.ea-footer__link { font-size: 0.82rem; color: #7a6852; text-decoration: none; transition: color 0.2s; }
.ea-footer__link:hover { color: #4a7c59; }
.ea-footer__bottom { border-top: 1.5px solid #D6CBB8; padding: 0.9rem 2rem; text-align: center; font-size: 0.72rem; color: #9e8a72; max-width: 1280px; margin: 0 auto; }
</style>
