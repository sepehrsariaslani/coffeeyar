<script setup>
import TheHeader from "./TheHeader.vue";
import TheFooter from "./TheFooter.vue";
import MobileBottomNav from "@/components/site/MobileBottomNav.vue";
</script>

<template>
  <div class="ea-layout">
    <TheHeader />
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
