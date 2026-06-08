<script setup>
import { ref, computed } from "vue";
import { RouterLink } from "vue-router";
import { Coffee, Rss, Clock, ArrowLeft } from "lucide-vue-next";
import TheLayout from "@/components/site/TheLayout.vue";
import BlogCard from "@/components/BlogCard.vue";
import { posts } from "@/lib/data.js";
import { useSeo } from "@/composables/useSeo.js";

useSeo({ title: "بلاگ — نوار", description: "از هنر دم‌آوری تا داستان مزارع — همه چیز درباره‌ی قهوه." });

const tabs = ["همه", "عمومی", "روش دم‌آوری"];
const activeTab = ref("همه");

const filtered = computed(() =>
  activeTab.value === "همه" ? posts : posts.filter((p) => p.category === activeTab.value)
);
const featuredPost = computed(() => filtered.value[0]);
const restPosts    = computed(() => filtered.value.slice(1));

const brewingMethods = [
  { slug: "brew-french-press", icon: "🇫🇷", label: "فرنچ پرس",  desc: "پُربدنه و غنی",    time: "۴ دقیقه" },
  { slug: "brew-v60",          icon: "☕",   label: "V60",         desc: "شفاف و ظریف",      time: "۳ دقیقه" },
  { slug: "brew-moka-pot",     icon: "🇮🇹", label: "موکاپات",   desc: "قوی و ایتالیایی",   time: "۵ دقیقه" },
  { slug: "brew-cold-brew",    icon: "🧊",   label: "کلد برو",   desc: "سرد و ملایم",       time: "۱۲ ساعت" },
];

const brewingPosts = posts.filter((p) => p.category === "روش دم‌آوری");
</script>

<template>
  <TheLayout>
    <!-- ── Hero ─────────────────────────────────────── -->
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
            <span>{{ posts.length }} مقاله</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Brewing Methods ───────────────────────────── -->
    <section class="border-b border-border">
      <div class="mx-auto max-w-7xl px-6 py-12">
        <div class="flex items-center justify-between mb-8">
          <div class="flex items-center gap-2">
            <Coffee class="h-4 w-4 text-maroon" />
            <span class="text-xs uppercase tracking-[0.3em] text-maroon">راهنمای دم‌آوری</span>
          </div>
          <RouterLink to="/blog" @click="activeTab = 'روش دم‌آوری'" class="flex items-center gap-1.5 text-xs text-maroon hover:opacity-70 transition-opacity">
            همه روش‌ها <ArrowLeft class="h-3.5 w-3.5" />
          </RouterLink>
        </div>
        <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <RouterLink
            v-for="m in brewingMethods" :key="m.slug"
            :to="brewingPosts.find(p => p.slug === m.slug) ? `/blog/${m.slug}` : '/blog'"
            class="group border border-border bg-background p-6 transition-all hover:border-maroon hover:bg-maroon/3"
          >
            <div class="text-3xl mb-4 transition-transform group-hover:scale-110 duration-200">{{ m.icon }}</div>
            <div class="font-medium text-sm group-hover:text-maroon transition-colors">{{ m.label }}</div>
            <div class="mt-1 text-xs text-muted-foreground">{{ m.desc }}</div>
            <div class="mt-4 flex items-center justify-between">
              <span class="text-xs text-muted-foreground/60">{{ m.time }}</span>
              <span class="text-xs text-maroon opacity-0 group-hover:opacity-100 transition-opacity">بخوانید ←</span>
            </div>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- ── Tab Filter ────────────────────────────────── -->
    <section>
      <div class="mx-auto max-w-7xl px-6">
        <div class="flex items-center justify-between border-b border-border pt-10">
          <div class="flex gap-0">
            <button
              v-for="t in tabs" :key="t" type="button" @click="activeTab = t"
              :class="['px-5 py-3 text-sm transition-colors', activeTab === t ? 'border-b-2 border-maroon text-maroon font-medium' : 'text-muted-foreground hover:text-foreground']"
            >{{ t }}</button>
          </div>
          <span class="text-xs text-muted-foreground pb-3">{{ filtered.length }} مقاله</span>
        </div>
      </div>
    </section>

    <!-- ── Content ───────────────────────────────────── -->
    <section class="mx-auto max-w-7xl px-6 py-10 pb-20">

      <!-- Featured post -->
      <div v-if="featuredPost" class="mb-8">
        <div class="flex items-center gap-2 mb-4">
          <div class="h-px flex-1 bg-border" />
          <span class="text-[10px] uppercase tracking-widest text-maroon">پیشنهاد ما</span>
          <div class="h-px flex-1 bg-border" />
        </div>
        <BlogCard :post="featuredPost" :featured="true" />
      </div>

      <!-- Grid -->
      <div v-if="restPosts.length" class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <BlogCard v-for="post in restPosts" :key="post.slug" :post="post" />
      </div>

      <p v-if="!filtered.length" class="py-20 text-center text-muted-foreground">
        مقاله‌ای در این دسته پیدا نشد.
      </p>
    </section>
  </TheLayout>
</template>
