<script setup>
import { RouterLink } from "vue-router";
import TheLayout from "@/components/site/TheLayout.vue";
</script>

<template>
  <TheLayout>
    <div class="mx-auto max-w-2xl px-6 py-32 text-center">
      <div class="text-6xl font-light text-maroon">۴۰۴</div>
      <h1 class="mt-4 text-3xl font-light">صفحه پیدا نشد</h1>
      <p class="mt-4 text-muted-foreground">صفحه‌ای که دنبالش می‌گشتید وجود ندارد.</p>
      <RouterLink to="/" class="mt-8 inline-block bg-foreground px-6 py-3 text-sm text-background hover:opacity-80">
        بازگشت به خانه
      </RouterLink>
    </div>
  </TheLayout>
</template>
