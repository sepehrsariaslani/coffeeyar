<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
onMounted(() => {
  router.replace("/admin/appearance");
});
</script>

<template>
  <div class="min-h-screen flex items-center justify-center" dir="rtl">
    <p class="text-muted-foreground text-sm">در حال انتقال...</p>
  </div>
</template>
