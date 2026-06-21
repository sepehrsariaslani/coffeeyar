<script setup>
import { computed } from "vue";
import { RouterLink } from "vue-router";
import { Instagram, Send, MapPin, Phone, Mail } from "lucide-vue-next";
import { useSiteSettingsStore } from "@/stores/siteSettings.js";
import { useLayoutStore } from "@/stores/layout.js";
import { useNavigationStore } from "@/stores/navigation.js";

const siteSettings = useSiteSettingsStore();
const layoutStore = useLayoutStore();
const navStore = useNavigationStore();
const variant = computed(() => layoutStore.footerVariant);

// Footer links from API navigation
const footerLinks = computed(() => {
  if (navStore.footerLinks && navStore.footerLinks.length) {
    return navStore.footerLinks;
  }
  // Fallback defaults
  return [
    { label: "محصولات", to: "/products" },
    { label: "درباره ما", to: "/about" },
    { label: "بلاگ", to: "/blog" },
    { label: "سوالات متداول", to: "/faq" },
    { label: "پیگیری سفارش", to: "/tracking" },
    { label: "تماس با ما", to: "/contact" },
    { label: "قوانین سایت", to: "/policies" },
  ];
});

/**
 * Normalized settings — the API returns snake_case fields
 * (shop_name, enamad_code, …) while the template uses camelCase.
 * This computed bridges both shapes so the footer always shows real data.
 */
const s = computed(() => {
  const x = siteSettings.settings || {};
  return {
    ...x,
    shopName: x.shop_name || x.shopName || "نوار",
    description: x.description || "",
    phone: x.phone || "",
    email: x.email || "",
    address: x.address || "",
    instagram: x.instagram || "",
    telegram: x.telegram || "",
    enamadCode: x.enamad_code || x.enamadCode || "",
    zarinpalEnabled: x.payment_online ?? x.zarinpalEnabled ?? false,
    zarinpalMerchantId: x.zarinpal_merchant_id || x.zarinpalMerchantId || "",
  };
});
</script>

<template>

  <!-- ── Variant 1: Classic 4-col ──────────────────── -->
  <footer v-if="variant === 1" class="border-t border-border mb-16 md:mb-0" dir="rtl">
    <div class="mx-auto max-w-7xl px-6 py-14 grid gap-10 md:grid-cols-4">

      <div class="md:col-span-2">
        <div class="text-lg font-medium">{{ s.shopName || 'نـوار' }}<span class="text-maroon">.</span></div>
        <p class="mt-3 max-w-sm text-sm leading-7 text-muted-foreground">{{ s.description }}</p>
        <div class="mt-5 flex flex-wrap gap-4 text-xs text-muted-foreground">
          <a v-if="s.phone" :href="`tel:${s.phone}`" class="flex items-center gap-1.5 hover:text-maroon">
            <Phone class="h-3.5 w-3.5" /> {{ s.phone }}
          </a>
          <a v-if="s.email" :href="`mailto:${s.email}`" class="flex items-center gap-1.5 hover:text-maroon">
            <Mail class="h-3.5 w-3.5" /> {{ s.email }}
          </a>
          <span v-if="s.address" class="flex items-center gap-1.5">
            <MapPin class="h-3.5 w-3.5 shrink-0" /> {{ s.address }}
          </span>
        </div>
      </div>

      <div>
        <h4 class="mb-4 text-xs uppercase tracking-widest text-muted-foreground">پیمایش</h4>
        <ul class="space-y-2.5 text-sm">
          <li v-for="link in footerLinks" :key="link.to || link.route">
            <RouterLink :to="link.to || link.route" class="hover:text-maroon transition-colors">{{ link.label }}</RouterLink>
          </li>
        </ul>
      </div>

      <div>
        <h4 class="mb-4 text-xs uppercase tracking-widest text-muted-foreground">دنبال کنید</h4>
        <div class="flex gap-4">
          <a :href="s.instagram || '#'" aria-label="اینستاگرام" class="hover:text-maroon transition-colors" :target="s.instagram && s.instagram !== '#' ? '_blank' : undefined">
            <Instagram class="h-5 w-5" />
          </a>
          <a :href="s.telegram || '#'" aria-label="تلگرام" class="hover:text-maroon transition-colors" :target="s.telegram && s.telegram !== '#' ? '_blank' : undefined">
            <Send class="h-5 w-5" />
          </a>
        </div>
        <div class="mt-6 space-y-3">
          <div v-if="s.enamadCode">
            <div class="text-[10px] uppercase tracking-widest text-muted-foreground mb-2">نماد اعتماد</div>
            <div v-html="s.enamadCode" class="inline-block [&>a>img]:max-h-16" />
          </div>
          <div v-else class="border border-dashed border-border p-3 text-center">
            <div class="text-[10px] text-muted-foreground leading-5">
              نماد اینماد<br/>
              <RouterLink to="/admin/site-settings" class="text-maroon hover:underline">از پنل تنظیم کنید</RouterLink>
            </div>
          </div>
          <div v-if="s.zarinpalEnabled && s.zarinpalMerchantId" class="flex items-center gap-2 border border-border px-3 py-2">
            <div class="h-7 w-7 bg-[#5a0db0] flex items-center justify-center text-white text-[10px] font-bold">Z</div>
            <div class="text-xs text-muted-foreground leading-4">پرداخت امن<br/><span class="text-foreground">زرین‌پال</span></div>
          </div>
        </div>
      </div>
    </div>

    <div class="border-t border-border">
      <div class="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-6 py-5 text-xs text-muted-foreground">
        <span>© {{ new Date().getFullYear() }} {{ s.shopName || 'نوار' }}. تمام حقوق محفوظ است.</span>
        <div class="flex items-center gap-4">
          <RouterLink v-for="link in footerLinks.slice(0, 4)" :key="link.to || link.route" :to="link.to || link.route" class="hover:text-maroon">{{ link.label }}</RouterLink>
        </div>
      </div>
    </div>
  </footer>

  <!-- ── Variant 2: Centered Minimal ───────────────── -->
  <footer v-else-if="variant === 2" class="border-t border-border mb-16 md:mb-0" dir="rtl">
    <div class="mx-auto max-w-2xl px-6 py-16 text-center">
      <div class="text-2xl font-light tracking-wide mb-2">
        {{ s.shopName || 'نـوار' }}<span class="text-maroon">.</span>
      </div>
      <p class="text-sm text-muted-foreground leading-7 mb-8 max-w-md mx-auto">{{ s.description }}</p>

      <nav class="flex flex-wrap justify-center gap-x-8 gap-y-3 text-sm mb-8">
        <RouterLink v-for="link in footerLinks" :key="link.to || link.route" :to="link.to || link.route" class="hover:text-maroon transition-colors">{{ link.label }}</RouterLink>
      </nav>

      <div class="flex justify-center gap-5 mb-10">
        <a :href="s.instagram || '#'" class="hover:text-maroon transition-colors" :target="s.instagram && s.instagram !== '#' ? '_blank' : undefined">
          <Instagram class="h-5 w-5" />
        </a>
        <a :href="s.telegram || '#'" class="hover:text-maroon transition-colors" :target="s.telegram && s.telegram !== '#' ? '_blank' : undefined">
          <Send class="h-5 w-5" />
        </a>
      </div>

      <div class="border-t border-border pt-6 text-xs text-muted-foreground">
        © {{ new Date().getFullYear() }} {{ s.shopName || 'نوار' }}. تمام حقوق محفوظ است.
      </div>
    </div>
  </footer>

  <!-- ── Variant 3: Dark Full ───────────────────────── -->
  <footer v-else class="footer-dark mb-16 md:mb-0" dir="rtl">
    <div class="mx-auto max-w-7xl px-6 py-16 grid gap-12 md:grid-cols-3">

      <div>
        <div class="text-xl font-light text-white mb-3">
          {{ s.shopName || 'نـوار' }}<span class="text-maroon" style="color:#D4956A">.</span>
        </div>
        <p class="text-sm leading-7 text-white/50 mb-6 max-w-xs">{{ s.description }}</p>
        <div class="flex gap-4">
          <a :href="s.instagram || '#'" class="footer-dark__social" :target="s.instagram && s.instagram !== '#' ? '_blank' : undefined">
            <Instagram class="h-4.5 w-4.5" />
          </a>
          <a :href="s.telegram || '#'" class="footer-dark__social" :target="s.telegram && s.telegram !== '#' ? '_blank' : undefined">
            <Send class="h-4.5 w-4.5" />
          </a>
        </div>
      </div>

      <div>
        <h4 class="mb-5 text-[10px] uppercase tracking-widest text-white/35">پیمایش</h4>
        <ul class="space-y-3 text-sm">
          <li v-for="link in footerLinks" :key="link.to || link.route">
            <RouterLink :to="link.to || link.route" class="footer-dark__link">{{ link.label }}</RouterLink>
          </li>
        </ul>
      </div>

      <div>
        <h4 class="mb-5 text-[10px] uppercase tracking-widest text-white/35">تماس</h4>
        <div class="space-y-3 text-sm text-white/50">
          <a v-if="s.phone" :href="`tel:${s.phone}`" class="footer-dark__link flex items-center gap-2">
            <Phone class="h-3.5 w-3.5" /> {{ s.phone }}
          </a>
          <a v-if="s.email" :href="`mailto:${s.email}`" class="footer-dark__link flex items-center gap-2">
            <Mail class="h-3.5 w-3.5" /> {{ s.email }}
          </a>
          <span v-if="s.address" class="flex items-center gap-2">
            <MapPin class="h-3.5 w-3.5 shrink-0" /> {{ s.address }}
          </span>
        </div>
      </div>
    </div>

    <div class="border-t border-white/10">
      <div class="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-6 py-5 text-xs text-white/30">
        <span>© {{ new Date().getFullYear() }} {{ s.shopName || 'نوار' }}. تمام حقوق محفوظ است.</span>
        <div class="flex items-center gap-4">
          <RouterLink to="/contact" class="hover:text-white/70 transition-colors">تماس با ما</RouterLink>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer-dark {
  background-color: #111;
  color: rgba(255,255,255,0.7);
}
.footer-dark__link {
  color: rgba(255,255,255,0.55);
  text-decoration: none;
  transition: color 0.2s;
}
.footer-dark__link:hover { color: rgba(255,255,255,0.9); }
.footer-dark__social {
  color: rgba(255,255,255,0.4);
  transition: color 0.2s;
}
.footer-dark__social:hover { color: rgba(255,255,255,0.9); }
</style>
