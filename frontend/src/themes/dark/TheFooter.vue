<script setup>
import { RouterLink } from "vue-router";
import { Instagram, Send, Phone, Mail, MapPin } from "lucide-vue-next";
import { useSiteSettingsStore } from "@/stores/siteSettings.js";
const s = useSiteSettingsStore().settings;
</script>

<template>
  <footer class="dk-footer" dir="rtl">
    <div class="dk-footer__inner">
      <div class="dk-footer__brand">
        <div class="dk-footer__logo">{{ s.shopName || 'نـوار' }}<span class="dk-footer__dot">.</span></div>
        <p class="dk-footer__desc">{{ s.description }}</p>
        <div class="dk-footer__contact">
          <a v-if="s.phone" :href="`tel:${s.phone}`" class="dk-footer__contact-item"><Phone class="h-3.5 w-3.5" />{{ s.phone }}</a>
          <a v-if="s.email" :href="`mailto:${s.email}`" class="dk-footer__contact-item"><Mail class="h-3.5 w-3.5" />{{ s.email }}</a>
          <span v-if="s.address" class="dk-footer__contact-item"><MapPin class="h-3.5 w-3.5 shrink-0" />{{ s.address }}</span>
        </div>
        <div class="dk-footer__social">
          <a :href="s.instagram || '#'" class="dk-social"><Instagram class="h-4 w-4" /></a>
          <a :href="s.telegram || '#'" class="dk-social"><Send class="h-4 w-4" /></a>
        </div>
      </div>
      <div class="dk-footer__col">
        <h4 class="dk-footer__col-title">پیمایش</h4>
        <nav class="dk-footer__nav">
          <RouterLink to="/products" class="dk-footer__link">محصولات</RouterLink>
          <RouterLink to="/about" class="dk-footer__link">درباره ما</RouterLink>
          <RouterLink to="/blog" class="dk-footer__link">بلاگ</RouterLink>
          <RouterLink to="/faq" class="dk-footer__link">سوالات</RouterLink>
          <RouterLink to="/tracking" class="dk-footer__link">پیگیری سفارش</RouterLink>
          <RouterLink to="/contact" class="dk-footer__link">تماس با ما</RouterLink>
        </nav>
      </div>
    </div>
    <div class="dk-footer__bottom">
      <span>© {{ new Date().getFullYear() }} {{ s.shopName || 'نوار' }}. تمام حقوق محفوظ است.</span>
    </div>
  </footer>
</template>

<style scoped>
.dk-footer { background-color: #0a0a0a; border-top: 1px solid rgba(255,255,255,0.07); margin-bottom: 4rem; color: rgba(255,255,255,0.65); }
@media (min-width: 768px) { .dk-footer { margin-bottom: 0; } }
.dk-footer__inner { max-width: 1280px; margin: 0 auto; padding: 3rem 2rem; display: grid; grid-template-columns: 1fr auto; gap: 3rem; }
@media (max-width: 640px) { .dk-footer__inner { grid-template-columns: 1fr; } }
.dk-footer__logo { font-size: 1.3rem; font-weight: 500; color: rgba(255,255,255,0.85); margin-bottom: 0.5rem; }
.dk-footer__dot { color: #C9923F; }
.dk-footer__desc { font-size: 0.82rem; color: rgba(255,255,255,0.35); line-height: 1.75; max-width: 280px; margin-bottom: 1rem; }
.dk-footer__contact { display: flex; flex-direction: column; gap: 0.4rem; margin-bottom: 1rem; }
.dk-footer__contact-item { display: flex; align-items: center; gap: 0.5rem; font-size: 0.78rem; color: rgba(255,255,255,0.35); text-decoration: none; transition: color 0.2s; }
.dk-footer__contact-item:hover { color: #C9923F; }
.dk-footer__social { display: flex; gap: 0.5rem; }
.dk-social { display: flex; align-items: center; justify-content: center; width: 34px; height: 34px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.10); border-radius: 50%; color: rgba(255,255,255,0.4); text-decoration: none; transition: all 0.2s; }
.dk-social:hover { background: rgba(255,255,255,0.08); color: #C9923F; }
.dk-footer__col-title { font-size: 0.65rem; letter-spacing: 0.18em; text-transform: uppercase; color: rgba(255,255,255,0.25); margin-bottom: 1rem; }
.dk-footer__nav { display: flex; flex-direction: column; gap: 0.6rem; }
.dk-footer__link { font-size: 0.82rem; color: rgba(255,255,255,0.4); text-decoration: none; transition: color 0.2s; }
.dk-footer__link:hover { color: rgba(255,255,255,0.85); }
.dk-footer__bottom { border-top: 1px solid rgba(255,255,255,0.06); padding: 0.9rem 2rem; text-align: center; font-size: 0.72rem; color: rgba(255,255,255,0.2); max-width: 1280px; margin: 0 auto; }
</style>
