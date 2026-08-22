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
    radial-gradient(ellipse 85% 70% at 8% 4%, oklch(0.78 0.08 48 / 0.48) 0%, transparent 58%),
    radial-gradient(ellipse 75% 70% at 94% 88%, oklch(0.78 0.06 125 / 0.38) 0%, transparent 56%),
    radial-gradient(ellipse 65% 55% at 62% 14%, oklch(0.92 0.045 82 / 0.72) 0%, transparent 56%),
    linear-gradient(135deg, #eee8df 0%, #e5ddd2 48%, #ebe7df 100%);
  background-attachment: fixed;
}
</style>
