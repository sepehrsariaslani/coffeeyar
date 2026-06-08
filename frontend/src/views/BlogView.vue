<script setup>
import { ref, computed, onMounted } from "vue";
import { RouterLink } from "vue-router";
import { Rss, Clock } from "lucide-vue-next";
import TheLayout from "@/components/site/TheLayout.vue";
import BlogCard from "@/components/BlogCard.vue";
import { usePostsStore } from "@/stores/posts.js";
import { useSeo } from "@/composables/useSeo.js";

useSeo({ title: "بلاگ — نوار", description: "از هنر دم‌آوری تا داستان مزارع — همه چیز درباره‌ی قهوه." });

const postsStore = usePostsStore();
const activeTab = ref("همه");
const tabs = ["همه", "دم‌آوری", "آموزش", "عمومی"];

const allPosts = computed(() => postsStore.getPublished());

const filtered = computed(() =>
  activeTab.value === "همه" ? allPosts.value : allPosts.value.filter((p) => p.category === activeTab.value)
);

const featuredPost = computed(() => filtered.value[0]);
const restPosts = computed(() => filtered.value.slice(1));

const brewingMethods = [
  { slug: "french-press-guide", icon: "🇫🇷", label: "فرنچ پرس", desc: "پُربدنه و غنی", time: "۴ دقیقه" },
  { slug: "art-of-pour-over", icon: "☕", label: "V60", desc: "شفاف و ظریف", time: "۳ دقیقه" },
  { slug: "single-origin-vs-blend", icon: "🇮🇹", label: "موکاپات", desc: "قوی و ایتالیایی", time: "۵ دقیقه" },
  { slug: "french-press-guide", icon: "🧊", label: "کلد برو", desc: "سرد و ملایم", time: "۱۲ ساعت" },
];

onMounted(() => postsStore.fetchPosts());
</script>

<template>
  <TheLayout>
    <!-- Hero -->
    <section class="border-b border-border bg-muted/20">
      <div class="mx-auto max-w-7xl px-6 py-20 md:py-28">
        <div class="flex items-start justify-between flex-wrap gap-6">
          <div>
            <div class="flex items-center gap-2 mb-4">
              <Rss class="h-4 w-4 text-maroon" />
              <span class="text-xs uppercase tracking-[0.3em] text-maroon">یادداشت‌ها</span>
            </div>
            <h1 class="text-4xl font-light md:text-6xl leading-tight">بلاگ</h1>
            <p class="mt-4 max-w-xl text-muted-foreground leading-7">از هنر دم‌آوری تا داستان مزارع — همه چیز درباره‌ی قهوه.</p>
          </div>
          <div class="flex items-center gap-3 self-end text-sm text-muted-foreground">
            <Clock class="h-4 w-4" />
            <span>{{ allPosts.length }} مقاله</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Tabs -->
    <div class="border-b border-border px-6">
      <div class="mx-auto max-w-7xl flex gap-0">
        <button v-for="tab in tabs" :key="tab" type="button" @click="activeTab = tab"
          :class="['px-5 py-4 text-sm font-[Vazirmatn] transition-colors', activeTab === tab ? 'border-b-2 border-maroon text-maroon' : 'text-muted-foreground hover:text-foreground']">
          {{ tab }}
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="postsStore.loading" class="py-24 text-center text-muted-foreground">در حال بارگذاری...</div>

    <!-- Posts -->
    <div v-else-if="filtered.length" class="mx-auto max-w-7xl px-6 py-16">
      <!-- Featured post -->
      <RouterLink v-if="featuredPost" :to="`/blog/${featuredPost.slug}`"
        class="group mb-12 grid gap-8 border border-border bg-muted/10 p-6 md:grid-cols-2 hover:border-maroon transition-colors">
        <div v-if="featuredPost.cover_image || featuredPost.coverImage" class="overflow-hidden">
          <img :src="featuredPost.cover_image || featuredPost.coverImage" :alt="featuredPost.title"
            class="h-64 w-full object-cover transition-transform duration-500 group-hover:scale-105" />
        </div>
        <div class="flex flex-col justify-center">
          <div class="mb-3 text-xs uppercase tracking-widest text-maroon">{{ featuredPost.category }}</div>
          <h2 class="text-2xl font-medium group-hover:text-maroon transition-colors">{{ featuredPost.title }}</h2>
          <p class="mt-3 text-sm leading-relaxed text-muted-foreground">{{ featuredPost.excerpt }}</p>
          <div class="mt-6 flex items-center gap-4 text-xs text-muted-foreground">
            <span>{{ featuredPost.author }}</span>
            <span>{{ featuredPost.read_time || featuredPost.readTime }}</span>
          </div>
        </div>
      </RouterLink>

      <!-- Rest of posts -->
      <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <BlogCard v-for="post in restPosts" :key="post.slug" :post="post" />
      </div>
    </div>

    <div v-else class="py-24 text-center text-muted-foreground">مطلبی در این دسته پیدا نشد.</div>

    <!-- Brewing methods -->
    <section class="border-t border-border bg-muted/20">
      <div class="mx-auto max-w-7xl px-6 py-16">
        <h2 class="mb-8 text-xl font-medium">روش‌های دم‌آوری</h2>
        <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <RouterLink v-for="m in brewingMethods" :key="m.label" :to="`/blog/${m.slug}`"
            class="group border border-border p-5 hover:border-maroon transition-colors">
            <div class="text-2xl mb-3">{{ m.icon }}</div>
            <div class="font-medium text-sm">{{ m.label }}</div>
            <div class="mt-1 text-xs text-muted-foreground">{{ m.desc }}</div>
            <div class="mt-3 text-xs text-muted-foreground">⏱ {{ m.time }}</div>
          </RouterLink>
        </div>
      </div>
    </section>
  </TheLayout>
</template>
