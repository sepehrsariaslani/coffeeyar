<script setup>
import { computed } from "vue";
import { useRoute, RouterLink } from "vue-router";
import TheLayout from "@/components/site/TheLayout.vue";
import { posts } from "@/lib/data.js";

const route = useRoute();
const post = computed(() => posts.find((p) => p.slug === route.params.slug));
</script>

<template>
  <TheLayout>
    <div v-if="!post" class="mx-auto max-w-2xl px-6 py-32 text-center">
      <h1 class="text-3xl">مقاله پیدا نشد</h1>
      <RouterLink to="/blog" class="mt-6 inline-block text-maroon">بازگشت به بلاگ</RouterLink>
    </div>

    <article v-else class="mx-auto max-w-3xl px-6 py-20 md:py-28">
      <RouterLink to="/blog" class="text-xs text-muted-foreground hover:text-maroon">← همه مقالات</RouterLink>
      <div class="mt-8 flex items-center gap-4 text-xs text-muted-foreground">
        <span>{{ post.date }}</span>
        <span class="h-px w-8 bg-border" />
        <span>{{ post.readTime }} مطالعه</span>
      </div>
      <h1 class="mt-4 text-4xl font-light leading-tight md:text-5xl">{{ post.title }}</h1>
      <p class="mt-6 text-lg leading-8 text-muted-foreground">{{ post.excerpt }}</p>
      <div class="mt-12 space-y-6 leading-9">
        <p>{{ post.body }}</p>
        <p>
          قهوه فقط یک نوشیدنی نیست؛ آیینی است که هر روز تکرار می‌شود. شناخت دانه، توجه به دما،
          صبر برای دم‌آوری — هر کدام بخشی از تجربه‌ای هستند که نوار سعی می‌کند به شما هدیه کند.
        </p>
        <p>
          در مقاله‌های بعدی به جزئیات بیشتری از روش‌های دم‌آوری، نسبت‌ها و تجهیزات خواهیم پرداخت.
        </p>
      </div>
    </article>
  </TheLayout>
</template>
