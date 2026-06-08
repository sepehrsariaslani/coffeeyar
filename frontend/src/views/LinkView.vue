<script setup>
import { ref, onMounted } from "vue";
import { useSiteSettingsStore } from "@/stores/siteSettings.js";

const settingsStore = useSiteSettingsStore();
const copied = ref(false);

function copyPhone() {
  const phone = settingsStore.settings.phone || "";
  navigator.clipboard.writeText(phone).then(() => {
    copied.value = true;
    setTimeout(() => { copied.value = false; }, 2000);
  });
}

const links = ref([
  { label: "فروشگاه آنلاین", url: "/", icon: "store" },
  { label: "منوی محصولات", url: "/products", icon: "menu" },
  { label: "قهوه‌های ویژه", url: "/products?featured=true", icon: "star" },
  { label: "درباره ما", url: "/about", icon: "info" },
  { label: "سوالات متداول", url: "/faq", icon: "help" },
  { label: "وبلاگ", url: "/blog", icon: "article" },
  { label: "تماس با ما", url: "/contact", icon: "call" },
]);

onMounted(() => {
  settingsStore.fetchSettings();
});
</script>

<template>
  <div class="link-page">
    <div class="link-page__inner">
      <!-- Avatar/Logo -->
      <div class="link-page__logo">
        <svg viewBox="0 0 64 64" fill="none" class="link-page__logo-svg">
          <rect x="8" y="16" width="44" height="34" rx="4" stroke="currentColor" stroke-width="2.5" fill="none"/>
          <path d="M52 24h4a4 4 0 0 1 0 8h-4" stroke="currentColor" stroke-width="2.5" fill="none"/>
        </svg>
      </div>

      <!-- Shop Name -->
      <h1 class="link-page__title">{{ settingsStore.settings.shopName || "فروشگاه" }}</h1>
      <p v-if="settingsStore.settings.description" class="link-page__desc">{{ settingsStore.settings.description }}</p>

      <!-- Phone -->
      <button v-if="settingsStore.settings.phone" class="link-page__btn link-page__btn--phone" @click="copyPhone">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        <span>{{ settingsStore.settings.phone }}</span>
        <span class="link-page__copy-badge" :class="{ visible: copied }">کپی شد</span>
      </button>

      <!-- Social Links -->
      <div v-if="settingsStore.settings.instagram || settingsStore.settings.telegram" class="link-page__social">
        <a v-if="settingsStore.settings.instagram" :href="settingsStore.settings.instagram" target="_blank" rel="noopener" class="link-page__social-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
          <span>اینستاگرام</span>
        </a>
        <a v-if="settingsStore.settings.telegram" :href="settingsStore.settings.telegram" target="_blank" rel="noopener" class="link-page__social-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2L.5 10l7.5 3 3 7.5 10.5-18.5z"/><path d="M11 14l7-7"/></svg>
          <span>تلگرام</span>
        </a>
      </div>

      <!-- Divider -->
      <div class="link-page__divider"></div>

      <!-- Quick Links -->
      <a
        v-for="link in links"
        :key="link.label"
        :href="link.url"
        class="link-page__link"
      >
        <span>{{ link.label }}</span>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
      </a>

      <!-- Footer -->
      <p class="link-page__footer">طراحی و توسعه توسط نوار</p>
    </div>
  </div>
</template>

<style scoped>
.link-page {
  min-height: 100dvh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--background, #f9f6f1);
  padding: 2rem 1rem;
  font-family: "Vazirmatn", Tahoma, sans-serif;
}

.link-page__inner {
  width: 100%;
  max-width: 380px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.link-page__logo {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: 2px solid var(--border, #e5e5e5);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--maroon, #7A2232);
  margin-bottom: 0.5rem;
}

.link-page__logo-svg {
  width: 36px;
  height: 36px;
}

.link-page__title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--foreground, #111);
  margin: 0;
}

.link-page__desc {
  font-size: 0.8rem;
  color: var(--muted-foreground, #666);
  text-align: center;
  line-height: 1.6;
  margin: 0;
}

.link-page__btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border, #e5e5e5);
  border-radius: 8px;
  background: var(--card, #fff);
  color: var(--foreground, #111);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.15s;
  position: relative;
  font-family: inherit;
}

.link-page__btn:hover {
  border-color: var(--maroon, #7A2232);
  background: color-mix(in srgb, var(--maroon, #7A2232) 5%, transparent);
}

.link-page__copy-badge {
  position: absolute;
  left: 50%;
  top: -28px;
  transform: translateX(-50%);
  background: var(--maroon, #7A2232);
  color: #fff;
  font-size: 0.7rem;
  padding: 2px 10px;
  border-radius: 6px;
  opacity: 0;
  transition: opacity 0.2s;
  pointer-events: none;
}

.link-page__copy-badge.visible {
  opacity: 1;
}

.link-page__social {
  display: flex;
  gap: 0.5rem;
  width: 100%;
}

.link-page__social-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.65rem;
  border: 1px solid var(--border, #e5e5e5);
  border-radius: 8px;
  background: var(--card, #fff);
  color: var(--foreground, #111);
  font-size: 0.8rem;
  text-decoration: none;
  transition: all 0.15s;
  font-family: inherit;
}

.link-page__social-btn:hover {
  border-color: var(--maroon, #7A2232);
}

.link-page__divider {
  width: 100%;
  height: 1px;
  background: var(--border, #e5e5e5);
  margin: 0.5rem 0;
}

.link-page__link {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.8rem 1rem;
  border: 1px solid var(--border, #e5e5e5);
  border-radius: 8px;
  background: var(--card, #fff);
  color: var(--foreground, #111);
  font-size: 0.9rem;
  text-decoration: none;
  transition: all 0.15s;
  font-family: inherit;
}

.link-page__link:hover {
  border-color: var(--maroon, #7A2232);
  transform: translateY(-1px);
}

.link-page__footer {
  font-size: 0.7rem;
  color: var(--muted-foreground, #aaa);
  margin-top: 0.5rem;
}
</style>
