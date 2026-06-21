<script setup>
import { List, LayoutGrid, Columns2, Network, BarChart2, CalendarDays } from "lucide-vue-next";

const props = defineProps({
  modelValue: { type: String, default: "list" },
  modes: { type: Array, default: () => ["list", "gallery", "kanban", "tree", "report"] },
});
const emit = defineEmits(["update:modelValue"]);

const allModes = {
  list:     { icon: List,          label: "جدول" },
  gallery:  { icon: LayoutGrid,    label: "گالری" },
  kanban:   { icon: Columns2,      label: "کانبان" },
  tree:     { icon: Network,       label: "درختی" },
  report:   { icon: BarChart2,     label: "گزارش" },
  gantt:    { icon: CalendarDays,  label: "تایم‌لاین" },
};
</script>

<template>
  <div class="flex border border-border shrink-0" dir="ltr" role="group" aria-label="نوع نمایش">
    <button
      v-for="mode in modes"
      :key="mode"
      type="button"
      @click="emit('update:modelValue', mode)"
      :title="allModes[mode]?.label"
      :class="[
        'flex items-center gap-1.5 px-2.5 py-2 text-xs transition-colors border-r border-border last:border-r-0',
        modelValue === mode
          ? 'bg-maroon text-white'
          : 'text-muted-foreground hover:bg-accent hover:text-foreground',
      ]"
    >
      <component :is="allModes[mode]?.icon" class="h-3.5 w-3.5" />
      <span class="hidden sm:inline">{{ allModes[mode]?.label }}</span>
    </button>
  </div>
</template>
