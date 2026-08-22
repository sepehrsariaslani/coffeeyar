<script setup>
import TheHeader from "@/components/site/TheHeaderResolver.vue";
import TheFooter from "@/components/site/TheFooterResolver.vue";
import MobileBottomNav from "@/components/site/MobileBottomNav.vue";
import StickyCategoryBar from "@/components/site/StickyCategoryBar.vue";
</script>

<template>
  <div class="gl-layout">
    <TheHeader />
    <StickyCategoryBar />
    <main class="flex-1 pb-16 md:pb-0 relative z-0">
      <slot />
    </main>
    <TheFooter />
    <MobileBottomNav />
  </div>
</template>

<style scoped>
.gl-layout {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  background:
    radial-gradient(ellipse 80% 60% at 5% 5%,   oklch(0.72 0.20 280 / 0.9), transparent 55%),
    radial-gradient(ellipse 70% 60% at 95% 85%,  oklch(0.68 0.22 340 / 0.9), transparent 50%),
    radial-gradient(ellipse 55% 55% at 65% 20%,  oklch(0.74 0.16 200 / 0.8), transparent 50%),
    radial-gradient(ellipse 45% 50% at 25% 80%,  oklch(0.75 0.14 160 / 0.8), transparent 50%),
    radial-gradient(ellipse 60% 40% at 80% 30%,  oklch(0.70 0.18 310 / 0.7), transparent 50%),
    oklch(0.80 0.06 270);
  background-attachment: fixed;
}
</style>
