<script setup>
import { ref } from "vue";
import { useProductGlobalFaqsStore } from "@/stores/productGlobalFaqs.js";
import { Plus, Trash2, ChevronUp, ChevronDown, Eye, EyeOff } from "lucide-vue-next";

const store = useProductGlobalFaqsStore();
const expanded = ref(null);

const applyToOptions = [
  { v: "all", l: "همه محصولات" },
  { v: "coffee", l: "فقط قهوه‌ها" },
  { v: "accessory", l: "فقط اکسسوری‌ها" },
];

function applyToLabel(v) {
  return applyToOptions.find((o) => o.v === v)?.l ?? v;
}
</script>

<template>
  <div class="p-4 md:p-10">
    <div class="mb-8 flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 class="text-3xl font-light">سوالات متداول محصولات <span class="text-maroon">.</span></h1>
        <p class="mt-2 text-sm text-muted-foreground">این سوالات در پایین صفحه‌ی تمام محصولات (یا محصولات انتخابی) نمایش داده می‌شوند.</p>
      </div>
      <button
        type="button"
        @click="store.add(); expanded = store.faqs[store.faqs.length - 1]?.id"
        class="inline-flex items-center gap-2 bg-maroon px-5 py-2.5 text-sm text-maroon-foreground hover:opacity-90"
      >
        <Plus class="h-4 w-4" /> سوال جدید
      </button>
    </div>

    <!-- Info banner -->
    <div class="mb-6 border border-maroon/20 bg-maroon/5 p-4 text-xs text-muted-foreground leading-6">
      <strong class="text-maroon">راهنما:</strong>
      سوال‌هایی که اینجا تعریف می‌کنید به‌صورت خودکار در همه‌ی صفحات محصول نمایش داده می‌شوند.
      می‌توانید هر سوال را فقط برای قهوه‌ها یا فقط اکسسوری‌ها یا همه محصولات تنظیم کنید.
      علاوه بر این، از داشبورد محصولات می‌توانید سوالات <strong>تخصصی</strong> هر محصول را هم جداگانه تعریف کنید — آن‌ها بالاتر از این سوالات نمایش داده می‌شوند.
    </div>

    <div class="space-y-2">
      <div
        v-for="(faq, idx) in store.faqs"
        :key="faq.id"
        :class="['border border-border', !faq.enabled ? 'opacity-50' : '']"
      >
        <!-- Header row -->
        <div
          class="flex cursor-pointer items-center justify-between p-4 hover:bg-accent/30"
          @click="expanded = expanded === faq.id ? null : faq.id"
        >
          <div class="flex items-center gap-3 min-w-0">
            <span class="text-xs text-muted-foreground w-5 shrink-0">{{ idx + 1 }}</span>
            <span class="text-sm font-medium truncate">{{ faq.title || "بدون عنوان" }}</span>
            <span class="text-[10px] border border-border px-1.5 py-0.5 text-muted-foreground shrink-0">
              {{ applyToLabel(faq.applyTo) }}
            </span>
          </div>
          <div class="flex items-center gap-1 shrink-0 mr-2" @click.stop>
            <button type="button" @click="store.moveUp(idx)" class="p-1.5 hover:bg-accent text-muted-foreground" title="بالاتر">
              <ChevronUp class="h-3.5 w-3.5" />
            </button>
            <button type="button" @click="store.moveDown(idx)" class="p-1.5 hover:bg-accent text-muted-foreground" title="پایین‌تر">
              <ChevronDown class="h-3.5 w-3.5" />
            </button>
            <button type="button" @click="faq.enabled = !faq.enabled; store.save()" class="p-1.5 hover:bg-accent text-muted-foreground" :title="faq.enabled ? 'پنهان کردن' : 'فعال کردن'">
              <EyeOff v-if="faq.enabled" class="h-3.5 w-3.5" />
              <Eye v-else class="h-3.5 w-3.5" />
            </button>
            <button type="button" @click="store.remove(faq.id)" class="p-1.5 hover:bg-accent text-maroon">
              <Trash2 class="h-3.5 w-3.5" />
            </button>
          </div>
        </div>

        <!-- Edit panel -->
        <div v-if="expanded === faq.id" class="border-t border-border bg-muted/20 p-5 space-y-4">
          <div class="grid gap-4 sm:grid-cols-2">
            <label class="block">
              <span class="field-label">عنوان سوال</span>
              <input v-model="faq.title" @input="store.save()" placeholder="مثلاً: ارسال و بازگشت" class="field-input" />
            </label>
            <label class="block">
              <span class="field-label">نمایش برای</span>
              <select v-model="faq.applyTo" @change="store.save()" class="field-input">
                <option v-for="o in applyToOptions" :key="o.v" :value="o.v">{{ o.l }}</option>
              </select>
            </label>
          </div>
          <label class="block">
            <span class="field-label">متن پاسخ (هر خط یک پاراگراف)</span>
            <textarea v-model="faq.content" @input="store.save()" rows="5" placeholder="پاسخ کامل را اینجا بنویسید..." class="field-input resize-y" />
          </label>
        </div>
      </div>

      <div v-if="store.faqs.length === 0" class="border border-dashed border-border p-16 text-center text-muted-foreground text-sm">
        هیچ سوالی اضافه نشده. با کلیک «سوال جدید» شروع کنید.
      </div>
    </div>
  </div>
</template>

<style scoped>
.field-label {
  display: block;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--muted-foreground);
  margin-bottom: 0.25rem;
}
.field-input {
  display: block;
  width: 100%;
  border: 1px solid var(--color-border);
  background-color: var(--color-background);
  padding: 0.625rem 0.75rem;
  font-size: 0.875rem;
  outline: none;
  margin-top: 0.25rem;
}
.field-input:focus { border-color: var(--color-maroon); }
</style>
