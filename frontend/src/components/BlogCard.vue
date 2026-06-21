<script setup>
import { RouterLink } from "vue-router";

const props = defineProps({
  post: { type: Object, required: true },
  featured: { type: Boolean, default: false },
});

const categoryGradients = {
  "روش دم‌آوری": "from-amber-900/20 via-orange-800/10 to-transparent",
  "عمومی": "from-stone-700/15 via-stone-600/8 to-transparent",
};

const categoryColors = {
  "روش دم‌آوری": "text-amber-800 bg-amber-800/8 border-amber-800/20",
  "عمومی": "text-maroon bg-maroon/8 border-maroon/20",
};
</script>

<template>
  <RouterLink
    :to="`/blog/${post.slug}`"
    :class="[
      'group flex flex-col border border-border bg-background transition-all duration-300',
      'hover:border-maroon/50 hover:shadow-md hover:-translate-y-0.5',
      featured ? 'sm:flex-row' : ''
    ]"
  >
    <!-- Visual header -->
    <div
      :class="[
        'relative overflow-hidden bg-gradient-to-br',
        categoryGradients[post.category] || 'from-stone-700/15 to-transparent',
        featured ? 'sm:w-2/5 h-48 sm:h-auto' : 'h-44'
      ]"
    >
      <div class="absolute inset-0 flex items-center justify-center opacity-10">
        <div class="text-8xl font-black text-foreground/30 select-none leading-none">
          {{ post.title.charAt(0) }}
        </div>
      </div>
      <!-- Coffee ring decoration -->
      <div class="absolute bottom-4 left-4 h-12 w-12 rounded-full border border-maroon/20 opacity-60" />
      <div class="absolute bottom-6 left-6 h-6 w-6 rounded-full border border-maroon/30 opacity-40" />
      <div class="absolute top-4 right-4">
        <span :class="['border px-2.5 py-1 text-[10px] font-medium uppercase tracking-wider', categoryColors[post.category] || 'text-maroon bg-maroon/8 border-maroon/20']">
          {{ post.category }}
        </span>
      </div>
    </div>

    <!-- Content -->
    <div :class="['flex flex-col flex-1', featured ? 'p-8' : 'p-6']">
      <div class="flex items-center gap-3 text-[10px] text-muted-foreground mb-3">
        <time>{{ post.date }}</time>
        <span class="h-px w-6 bg-border" />
        <span>{{ post.readTime }} مطالعه</span>
      </div>

      <h3 :class="[
        'font-medium leading-snug group-hover:text-maroon transition-colors',
        featured ? 'text-xl md:text-2xl' : 'text-base'
      ]">
        {{ post.title }}
      </h3>

      <p :class="['mt-3 leading-7 text-muted-foreground', featured ? 'text-sm line-clamp-4' : 'text-sm line-clamp-3']">
        {{ post.excerpt }}
      </p>

      <div class="mt-auto pt-5 flex items-center justify-between border-t border-border/60">
        <span class="text-[11px] text-muted-foreground/60">نوار کافه</span>
        <span class="flex items-center gap-1.5 text-[11px] text-maroon opacity-0 group-hover:opacity-100 transition-all duration-200 translate-x-1 group-hover:translate-x-0">
          ادامه مطلب
          <svg width="12" height="12" viewBox="0 0 16 16" fill="none">
            <path d="M12 8H4M8 4L4 8L8 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </span>
      </div>
    </div>
  </RouterLink>
</template>
