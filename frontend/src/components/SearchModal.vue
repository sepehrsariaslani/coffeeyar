<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { Search, X, Package, FileText, ArrowLeft } from "lucide-vue-next";
import { products } from "@/lib/data.js";
import { usePostsStore } from "@/stores/posts.js";
import { useCategoriesStore } from "@/stores/categories.js";

const emit = defineEmits(["close"]);
const router = useRouter();
const postsStore = usePostsStore();
const categoriesStore = useCategoriesStore();
const query = ref("");
const inputRef = ref(null);

onMounted(() => setTimeout(() => inputRef.value?.focus(), 50));

function onKeydown(e) {
  if (e.key === "Escape") emit("close");
}
onMounted(() => document.addEventListener("keydown", onKeydown));
onUnmounted(() => document.removeEventListener("keydown", onKeydown));

const productResults = computed(() => {
  if (query.value.length < 2) return [];
  const q = query.value.toLowerCase();
  return products.filter((p) =>
    p.name.includes(q) ||
    (p.notes && p.notes.some((n) => n.includes(q))) ||
    (p.description && p.description.includes(q)) ||
    Object.values(p.attrs || {}).some((v) => String(v).includes(q))
  ).slice(0, 5);
});

const postResults = computed(() => {
  if (query.value.length < 2) return [];
  const q = query.value.toLowerCase();
  return postsStore.posts
    .filter((p) => p.status === "published" && (p.title.includes(q) || (p.excerpt && p.excerpt.includes(q))))
    .slice(0, 3);
});

const hasResults = computed(() => productResults.value.length > 0 || postResults.value.length > 0);

function go(path) {
  router.push(path);
  emit("close");
}
</script>

<template>
  <div class="fixed inset-0 z-[100] flex flex-col" @click.self="emit('close')">
    <div class="absolute inset-0 bg-foreground/60 backdrop-blur-sm" @click="emit('close')" />

    <div class="relative mx-auto mt-20 w-full max-w-2xl px-4">
      <div class="bg-background border border-border shadow-2xl">
        <!-- Input -->
        <div class="flex items-center gap-3 border-b border-border px-4 py-4">
          <Search class="h-5 w-5 shrink-0 text-muted-foreground" />
          <input
            ref="inputRef"
            v-model="query"
            placeholder="جستجو در محصولات، بلاگ و..."
            class="flex-1 bg-transparent text-base outline-none placeholder:text-muted-foreground"
          />
          <button @click="emit('close')" class="p-1 hover:text-maroon text-muted-foreground">
            <X class="h-4 w-4" />
          </button>
        </div>

        <!-- Results -->
        <div v-if="query.length >= 2" class="max-h-[60vh] overflow-y-auto divide-y divide-border">

          <!-- Products -->
          <div v-if="productResults.length">
            <div class="px-4 py-2.5 text-[10px] uppercase tracking-widest text-muted-foreground bg-muted/50">محصولات</div>
            <button
              v-for="p in productResults"
              :key="p.id"
              @click="go(`/products/${p.id}`)"
              class="flex w-full items-center gap-3 px-4 py-3 text-right hover:bg-accent transition-colors"
            >
              <img v-if="p.image" :src="p.image" alt="" class="h-12 w-12 shrink-0 object-cover" />
              <div v-else class="h-12 w-12 shrink-0 bg-muted flex items-center justify-center text-xl">
                {{ categoriesStore.getById(p.categoryId)?.icon || '📦' }}
              </div>
              <div class="flex-1 min-w-0 text-right">
                <div class="font-medium text-sm">{{ p.name }}</div>
                <div class="mt-0.5 text-xs text-muted-foreground">
                  {{ categoriesStore.getById(p.categoryId)?.name }}
                  <template v-if="p.notes?.length"> · {{ p.notes.slice(0, 2).join(" · ") }}</template>
                </div>
              </div>
              <ArrowLeft class="h-4 w-4 shrink-0 text-muted-foreground" />
            </button>
          </div>

          <!-- Posts -->
          <div v-if="postResults.length">
            <div class="px-4 py-2.5 text-[10px] uppercase tracking-widest text-muted-foreground bg-muted/50">مقالات بلاگ</div>
            <button
              v-for="p in postResults"
              :key="p.slug"
              @click="go(`/blog/${p.slug}`)"
              class="flex w-full items-center gap-3 px-4 py-3 text-right hover:bg-accent transition-colors"
            >
              <div class="h-12 w-12 shrink-0 bg-muted flex items-center justify-center">
                <FileText class="h-5 w-5 text-muted-foreground" />
              </div>
              <div class="flex-1 min-w-0 text-right">
                <div class="font-medium text-sm">{{ p.title }}</div>
                <div v-if="p.excerpt" class="mt-0.5 text-xs text-muted-foreground line-clamp-1">{{ p.excerpt }}</div>
              </div>
              <ArrowLeft class="h-4 w-4 shrink-0 text-muted-foreground" />
            </button>
          </div>

          <!-- No results -->
          <div v-if="!hasResults" class="px-4 py-12 text-center text-sm text-muted-foreground">
            نتیجه‌ای برای «{{ query }}» پیدا نشد
          </div>
        </div>

        <!-- Hint -->
        <div v-if="query.length < 2" class="px-4 py-5 text-center text-xs text-muted-foreground">
          برای جستجو حداقل ۲ کاراکتر وارد کنید
        </div>

        <div class="border-t border-border px-4 py-2 flex items-center justify-between text-[10px] text-muted-foreground">
          <span>Esc برای بستن</span>
          <span>{{ productResults.length + postResults.length }} نتیجه</span>
        </div>
      </div>
    </div>
  </div>
</template>
