<script setup>
import TheHeader from "./TheHeader.vue";
import TheFooter from "./TheFooter.vue";
import MobileBottomNav from "@/components/site/MobileBottomNav.vue";
</script>

<template>
  <div class="dk-layout">
    <TheHeader />
    <main class="flex-1 pb-16 md:pb-0">
      <slot />
    </main>
    <TheFooter />
    <MobileBottomNav />
  </div>
</template>

<style scoped>
.dk-layout {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  background-color: #0d0d0d;
  color: rgba(255,255,255,0.82);
}
</style>
