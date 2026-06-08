<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, RouterLink } from "vue-router";
import TheLayout from "@/components/site/TheLayout.vue";
import { usePostsStore } from "@/stores/posts.js";
import { useSeo } from "@/composables/useSeo.js";

const route = useRoute();
const postsStore = usePostsStore();

const post = computed(() => postsStore.getBySlug(route.params.slug));

useSeo({
  title: computed(() => post.value?.title || "مقاله"),
  description: computed(() => post.value?.excerpt?.slice(0, 155) || ""),
  image: computed(() => post.value?.cover_image || post.value?.coverImage || ""),
});

onMounted(async () => {
  if (!postsStore.posts.length) await postsStore.fetchPosts();
});
</script>

<template>
  <TheLayout>
    <div v-if="postsStore.loading" class="mx-auto max-w-2xl px-6 py-32 text-center text-muted-foreground">
      در حال بارگذاری...
    </div>
    <div v-else-if="!post" class="mx-auto max-w-2xl px-6 py-32 text-center">
      <h1 class="text-3xl">مقاله پیدا نشد</h1>
      <RouterLink to="/blog" class="mt-6 inline-block text-maroon">بازگشت به بلاگ</RouterLink>
    </div>

    <article v-else class="mx-auto max-w-3xl px-6 py-20 md:py-28">
      <RouterLink to="/blog" class="text-xs text-muted-foreground hover:text-maroon">← همه مقالات</RouterLink>

      <div v-if="post.cover_image || post.coverImage" class="mt-8 overflow-hidden">
        <img :src="post.cover_image || post.coverImage" :alt="post.title" class="w-full h-64 object-cover md:h-96" />
      </div>

      <div class="mt-8 flex items-center gap-4 text-xs text-muted-foreground">
        <span>{{ post.date || post.published_at?.slice(0, 10) }}</span>
        <span class="h-px w-8 bg-border" />
        <span>{{ post.read_time || post.readTime }} مطالعه</span>
        <span v-if="post.author" class="h-px w-8 bg-border" />
        <span v-if="post.author">{{ post.author }}</span>
      </div>
      <h1 class="mt-4 text-4xl font-light leading-tight md:text-5xl">{{ post.title }}</h1>
      <p class="mt-6 text-lg leading-8 text-muted-foreground">{{ post.excerpt }}</p>

      <div class="mt-12 space-y-6 leading-9 text-foreground/80 whitespace-pre-line">
        <p>{{ post.body || post.content }}</p>
        <p>
          قهوه فقط یک نوشیدنی نیست؛ آیینی است که هر روز تکرار می‌شود. شناخت دانه، توجه به دما،
          صبر برای دم‌آوری — هر کدام بخشی از تجربه‌ای هستند که نوار سعی می‌کند به شما هدیه کند.
        </p>
        <p>
          در مقاله‌های بعدی به جزئیات بیشتری از روش‌های دم‌آوری، نسبت‌ها و تجهیزات خواهیم پرداخت.
        </p>
      </div>

      <div class="mt-16 border-t border-border pt-8">
        <RouterLink to="/blog" class="text-sm text-maroon hover:underline">← بازگشت به همه مقالات</RouterLink>
      </div>
    </article>
  </TheLayout>
</template>
