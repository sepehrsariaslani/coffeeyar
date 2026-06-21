<script setup>
import { ref, computed } from "vue";
import { useContentStore } from "@/stores/content.js";
import { Plus, Trash2, RotateCcw, Check } from "lucide-vue-next";

const store = useContentStore();
const c = computed(() => store.content);

// Wait for content to load
const isLoading = computed(() => store.loading || !store.loaded);

const activeSection = ref("home");
const saved = ref(false);

function markSaved() {
  saved.value = true;
  setTimeout(() => (saved.value = false), 2000);
}

function resetAll() {
  if (confirm("همه محتوا به حالت پیش‌فرض بازگردانده می‌شود. ادامه؟")) {
    store.reset();
    markSaved();
  }
}

// Timeline helpers
function addTimelineItem() {
  if (c.value?.about?.timeline) c.value.about.timeline.push({ year: "", title: "", description: "" });
}
function removeTimelineItem(i) {
  if (c.value?.about?.timeline) c.value.about.timeline.splice(i, 1);
}

// Stats helpers
function addStat() {
  if (c.value?.about?.stats) c.value.about.stats.push({ value: "", label: "" });
}
function removeStat(i) {
  if (c.value?.about?.stats) c.value.about.stats.splice(i, 1);
}

// Values helpers
function addValue() {
  if (c.value?.about?.values) c.value.about.values.push({ title: "", description: "" });
}
function removeValue(i) {
  if (c.value?.about?.values) c.value.about.values.splice(i, 1);
}

// Story paragraph helpers
function addParagraph() {
  if (c.value?.about?.storyParagraphs) c.value.about.storyParagraphs.push("");
}
function removeParagraph(i) {
  if (c.value?.about?.storyParagraphs) c.value.about.storyParagraphs.splice(i, 1);
}

const sections = [
  { id: "home", label: "صفحه اصلی" },
  { id: "about", label: "درباره ما" },
  { id: "contact", label: "تماس با ما" },
];
</script>

<template>
  <div class="p-10" dir="rtl">
    <!-- Loading state -->
    <div v-if="isLoading" class="flex items-center justify-center py-20">
      <p class="text-muted-foreground">در حال بارگذاری محتوا...</p>
    </div>

    <div v-else>
      <div class="mb-6 md:mb-8 flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 class="text-2xl md:text-3xl font-light">مدیریت محتوا <span class="text-maroon">.</span></h1>
          <p class="mt-1 md:mt-2 text-xs md:text-sm text-muted-foreground">ویرایش متن و محتوای تمام صفحات سایت</p>
        </div>
        <div class="flex gap-2 md:gap-3">
          <button
            type="button"
            @click="resetAll"
            class="flex items-center gap-2 border border-border px-4 py-2.5 text-sm hover:bg-accent"
          >
            <RotateCcw class="h-4 w-4" /> بازگشت به پیش‌فرض
          </button>
          <div
            v-if="saved"
            class="flex items-center gap-2 bg-maroon/10 px-4 py-2.5 text-sm text-maroon"
          >
            <Check class="h-4 w-4" /> ذخیره شد
          </div>
        </div>
      </div>

      <div class="flex gap-0 border border-border">
        <!-- Sidebar -->
        <nav class="w-48 shrink-0 border-l border-border bg-muted/20 hidden md:block">
          <button
            v-for="s in sections"
            :key="s.id"
            type="button"
            @click="activeSection = s.id"
            :class="[
              'w-full px-5 py-3.5 text-right text-sm transition-colors',
              activeSection === s.id
                ? 'bg-foreground text-background'
                : 'text-muted-foreground hover:bg-accent hover:text-foreground',
            ]"
          >
            {{ s.label }}
          </button>
        </nav>

        <!-- Mobile section tabs -->
        <div class="flex md:hidden border-b border-border bg-muted/20 overflow-x-auto w-full">
          <button
            v-for="s in sections"
            :key="s.id"
            type="button"
            @click="activeSection = s.id"
            :class="[
              'px-4 py-3 text-sm whitespace-nowrap transition-colors shrink-0',
              activeSection === s.id
                ? 'bg-foreground text-background'
                : 'text-muted-foreground hover:bg-accent hover:text-foreground',
            ]"
          >
            {{ s.label }}
          </button>
        </div>

        <!-- Content -->
        <div class="flex-1 overflow-y-auto p-4 md:p-8">
          <!-- Home -->
          <template v-if="activeSection === 'home'">
            <div class="space-y-6 max-w-2xl">
              <h2 class="text-lg font-light border-b border-border pb-3">صفحه اصلی</h2>

              <fieldset class="space-y-4 border border-border p-5">
                <legend class="px-2 text-xs uppercase tracking-widest text-maroon">بخش هیرو</legend>
                <label class="block">
                  <span class="field-label">برچسب بالا</span>
                  <input v-model="c.home.heroTag" @input="markSaved" class="field-input" />
                </label>
                <label class="block">
                  <span class="field-label">عنوان اصلی</span>
                  <textarea v-model="c.home.heroTitle" @input="markSaved" rows="2" class="field-input resize-none" />
                </label>
                <label class="block">
                  <span class="field-label">توضیحات</span>
                  <textarea v-model="c.home.heroSubtitle" @input="markSaved" rows="3" class="field-input resize-none" />
                </label>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <label class="block">
                    <span class="field-label">دکمه اصلی</span>
                    <input v-model="c.home.heroCtaPrimary" @input="markSaved" class="field-input" />
                  </label>
                  <label class="block">
                    <span class="field-label">دکمه ثانوی</span>
                    <input v-model="c.home.heroCtaSecondary" @input="markSaved" class="field-input" />
                  </label>
                </div>
              </fieldset>

              <fieldset class="space-y-4 border border-border p-5">
                <legend class="px-2 text-xs uppercase tracking-widest text-maroon">بخش محصولات ویژه</legend>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <label class="block">
                    <span class="field-label">برچسب</span>
                    <input v-model="c.home.featuredTag" @input="markSaved" class="field-input" />
                  </label>
                  <label class="block">
                    <span class="field-label">عنوان</span>
                    <input v-model="c.home.featuredTitle" @input="markSaved" class="field-input" />
                  </label>
                </div>
                <label class="block">
                  <span class="field-label">توضیحات</span>
                  <textarea v-model="c.home.featuredSubtitle" @input="markSaved" rows="2" class="field-input resize-none" />
                </label>
              </fieldset>
            </div>
          </template>

          <!-- About -->
          <template v-if="activeSection === 'about'">
            <div class="space-y-6 max-w-2xl">
              <h2 class="text-lg font-light border-b border-border pb-3">صفحه درباره ما</h2>

              <fieldset class="space-y-4 border border-border p-5">
                <legend class="px-2 text-xs uppercase tracking-widest text-maroon">هیرو</legend>
                <label class="block">
                  <span class="field-label">برچسب</span>
                  <input v-model="c.about.heroTag" @input="markSaved" class="field-input" />
                </label>
                <label class="block">
                  <span class="field-label">عنوان اصلی</span>
                  <input v-model="c.about.heroTitle" @input="markSaved" class="field-input" />
                </label>
              </fieldset>

              <fieldset class="space-y-4 border border-border p-5">
                <legend class="px-2 text-xs uppercase tracking-widest text-maroon">بخش داستان</legend>
                <label class="block">
                  <span class="field-label">عنوان بخش</span>
                  <input v-model="c.about.storyTitle" @input="markSaved" class="field-input" />
                </label>
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-muted-foreground">پاراگراف‌ها</span>
                    <button type="button" @click="addParagraph" class="text-xs text-maroon hover:underline">+ افزودن</button>
                  </div>
                  <div v-for="(p, i) in c.about.storyParagraphs" :key="i" class="flex gap-2">
                    <textarea
                      :value="p"
                      @input="c.about.storyParagraphs[i] = $event.target.value; markSaved()"
                      rows="3"
                      :placeholder="`پاراگراف ${i + 1}`"
                      class="field-input flex-1 resize-none"
                    />
                    <button type="button" @click="removeParagraph(i)" class="self-start p-1.5 hover:text-maroon">
                      <Trash2 class="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </fieldset>

              <fieldset class="space-y-4 border border-border p-5">
                <legend class="px-2 text-xs uppercase tracking-widest text-maroon">آمار</legend>
                <div class="flex justify-end">
                  <button type="button" @click="addStat" class="text-xs text-maroon hover:underline">+ افزودن</button>
                </div>
                <div v-for="(s, i) in c.about.stats" :key="i" class="flex items-center gap-3">
                  <input v-model="s.value" @input="markSaved" placeholder="مقدار (مثلاً ۲۰۰+)" class="field-input flex-1" />
                  <input v-model="s.label" @input="markSaved" placeholder="برچسب" class="field-input flex-1" />
                  <button type="button" @click="removeStat(i)" class="p-1.5 hover:text-maroon">
                    <Trash2 class="h-4 w-4" />
                  </button>
                </div>
              </fieldset>

              <fieldset class="space-y-4 border border-border p-5">
                <legend class="px-2 text-xs uppercase tracking-widest text-maroon">تایملاین تاریخچه</legend>
                <div class="flex justify-end">
                  <button type="button" @click="addTimelineItem" class="text-xs text-maroon hover:underline">+ افزودن رویداد</button>
                </div>
                <div v-for="(item, i) in c.about.timeline" :key="i" class="relative border border-border p-4 space-y-3">
                  <button type="button" @click="removeTimelineItem(i)" class="absolute left-3 top-3 p-1 text-muted-foreground hover:text-maroon">
                    <Trash2 class="h-3.5 w-3.5" />
                  </button>
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <label class="block">
                      <span class="field-label">سال</span>
                      <input v-model="item.year" @input="markSaved" placeholder="۱۴۰۱" class="field-input" />
                    </label>
                    <label class="block">
                      <span class="field-label">عنوان</span>
                      <input v-model="item.title" @input="markSaved" placeholder="اولین خاستگاه‌ها" class="field-input" />
                    </label>
                  </div>
                  <label class="block">
                    <span class="field-label">توضیحات</span>
                    <textarea v-model="item.description" @input="markSaved" rows="2" class="field-input resize-none" />
                  </label>
                </div>
              </fieldset>

              <fieldset class="space-y-4 border border-border p-5">
                <legend class="px-2 text-xs uppercase tracking-widest text-maroon">ماموریت و چشم‌انداز</legend>
                <label class="block">
                  <span class="field-label">ماموریت</span>
                  <textarea v-model="c.about.mission" @input="markSaved" rows="4" class="field-input resize-none" />
                </label>
                <label class="block">
                  <span class="field-label">چشم‌انداز</span>
                  <textarea v-model="c.about.vision" @input="markSaved" rows="4" class="field-input resize-none" />
                </label>
              </fieldset>

              <fieldset class="space-y-4 border border-border p-5">
                <legend class="px-2 text-xs uppercase tracking-widest text-maroon">ارزش‌های کلیدی</legend>
                <div class="flex justify-end">
                  <button type="button" @click="addValue" class="text-xs text-maroon hover:underline">+ افزودن ارزش</button>
                </div>
                <div v-for="(v, i) in c.about.values" :key="i" class="relative border border-border p-4 space-y-3">
                  <button type="button" @click="removeValue(i)" class="absolute left-3 top-3 p-1 text-muted-foreground hover:text-maroon">
                    <Trash2 class="h-3.5 w-3.5" />
                  </button>
                  <label class="block">
                    <span class="field-label">عنوان</span>
                    <input v-model="v.title" @input="markSaved" class="field-input" />
                  </label>
                  <label class="block">
                    <span class="field-label">توضیحات</span>
                    <textarea v-model="v.description" @input="markSaved" rows="2" class="field-input resize-none" />
                  </label>
                </div>
              </fieldset>
            </div>
          </template>

          <!-- Contact -->
          <template v-if="activeSection === 'contact'">
            <div class="space-y-6 max-w-2xl">
              <h2 class="text-lg font-light border-b border-border pb-3">صفحه تماس</h2>

              <fieldset class="space-y-4 border border-border p-5">
                <legend class="px-2 text-xs uppercase tracking-widest text-maroon">هیرو</legend>
                <label class="block">
                  <span class="field-label">برچسب</span>
                  <input v-model="c.contact.heroTag" @input="markSaved" class="field-input" />
                </label>
                <label class="block">
                  <span class="field-label">عنوان</span>
                  <input v-model="c.contact.heroTitle" @input="markSaved" class="field-input" />
                </label>
              </fieldset>

              <fieldset class="space-y-4 border border-border p-5">
                <legend class="px-2 text-xs uppercase tracking-widest text-maroon">اطلاعات تماس</legend>
                <label class="block">
                  <span class="field-label">آدرس</span>
                  <input v-model="c.contact.address" @input="markSaved" class="field-input" />
                </label>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <label class="block">
                    <span class="field-label">تلفن</span>
                    <input v-model="c.contact.phone" @input="markSaved" dir="ltr" class="field-input" />
                  </label>
                  <label class="block">
                    <span class="field-label">ایمیل</span>
                    <input v-model="c.contact.email" @input="markSaved" dir="ltr" class="field-input" />
                  </label>
                </div>
                <label class="block">
                  <span class="field-label">ساعات کاری</span>
                  <input v-model="c.contact.workingHours" @input="markSaved" class="field-input" />
                </label>
              </fieldset>
            </div>
          </template>
        </div>
      </div>
    </div><!-- end v-else -->
  </div>
</template>

<style scoped>
.field-label {
  display: block;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--muted-foreground);
  margin-bottom: 0.4rem;
}

.field-input {
  width: 100%;
  border: 1px solid var(--border);
  background-color: var(--background);
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  outline: none;
  transition: border-color 0.15s;
  font-family: 'Vazirmatn', sans-serif;
}

.field-input:focus {
  border-color: var(--maroon);
}
</style>
