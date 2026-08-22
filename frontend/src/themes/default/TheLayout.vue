<script setup>
import TheHeader from "@/components/site/TheHeaderResolver.vue";
import TheFooter from "@/components/site/TheFooterResolver.vue";
import MobileBottomNav from "@/components/site/MobileBottomNav.vue";
import StickyCategoryBar from "@/components/site/StickyCategoryBar.vue";
</script>

<template>
  <div class="flex min-h-screen flex-col bg-background">
    <TheHeader />
    <StickyCategoryBar />
    <main class="flex-1 pb-16 md:pb-0">
      <slot />
    </main>
    <TheFooter />
    <MobileBottomNav />
  </div>
</template>
