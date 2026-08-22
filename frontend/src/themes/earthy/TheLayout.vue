<script setup>
import TheHeader from "@/components/site/TheHeaderResolver.vue";
import TheFooter from "@/components/site/TheFooterResolver.vue";
import MobileBottomNav from "@/components/site/MobileBottomNav.vue";
import StickyCategoryBar from "@/components/site/StickyCategoryBar.vue";
</script>

<template>
  <div class="ea-layout">
    <TheHeader />
    <StickyCategoryBar />
    <main class="flex-1 pb-16 md:pb-0">
      <slot />
    </main>
    <TheFooter />
    <MobileBottomNav />
  </div>
</template>

<style scoped>
.ea-layout {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  background-color: #F5F0E8;
  color: #2d2416;
}
</style>
