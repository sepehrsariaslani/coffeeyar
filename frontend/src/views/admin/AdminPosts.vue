<script setup>
import { ref, computed } from "vue";
import { usePostsStore } from "@/stores/posts.js";
import { Plus, Pencil, Trash2, X, Eye, EyeOff, Image, Bold, Italic, List } from "lucide-vue-next";

const store = usePostsStore();
const drawer = ref({ mode: "closed" });
const filter = ref("all");

const emptyForm = () => ({
  title: "",
  excerpt: "",
  body: "",
  category: "عمومی",
  readTime: "۵ دقیقه",
  status: "draft",
  coverImage: "",
  author: "نوار",
});

const form = ref(emptyForm());
const bodyRef = ref(null);

const filtered = computed(() => {
  if (filter.value === "all") return store.posts;
  return store.posts.filter((p) => p.status === filter.value);
});

const counts = computed(() => ({
  all: store.posts.length,
  published: store.posts.filter((p) => p.status === "published").length,
  draft: store.posts.filter((p) => p.status === "draft").length,
}));

function openCreate() {
  form.value = emptyForm();
  drawer.value = { mode: "create" };
}

function openEdit(p) {
  form.value = {
    title: p.title,
    excerpt: p.excerpt || "",
    body: p.body || "",
    category: p.category || "عمومی",
    readTime: p.readTime || "۵ دقیقه",
    status: p.status || "published",
    coverImage: p.coverImage || "",
    author: p.author || "نوار",
  };
  drawer.value = { mode: "edit", slug: p.slug };
}

function submitForm(e) {
  e.preventDefault();
  if (drawer.value.mode === "edit") {
    store.update(drawer.value.slug, form.value);
  } else {
    store.create(form.value);
  }
  drawer.value = { mode: "closed" };
}

function toggleStatus(post) {
  store.update(post.slug, { status: post.status === "published" ? "draft" : "published" });
}

function remove(slug) {
  if (confirm("این مقاله حذف شود؟")) store.remove(slug);
}

function handleImageUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (ev) => { form.value.coverImage = ev.target.result; };
  reader.readAsDataURL(file);
}

function insertBodyImage(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (ev) => {
    const url = ev.target.result;
    const tag = `\n![${file.name}](${url})\n`;
    const el = bodyRef.value;
    if (el) {
      const start = el.selectionStart;
      form.value.body = form.value.body.slice(0, start) + tag + form.value.body.slice(start);
    } else {
      form.value.body += tag;
    }
  };
  reader.readAsDataURL(file);
}

function wrapText(before, after = before) {
  const el = bodyRef.value;
  if (!el) return;
  const start = el.selectionStart;
  const end = el.selectionEnd;
  const selected = form.value.body.slice(start, end);
  form.value.body = form.value.body.slice(0, start) + before + selected + after + form.value.body.slice(end);
  setTimeout(() => {
    el.selectionStart = start + before.length;
    el.selectionEnd = end + before.length;
    el.focus();
  }, 0);
}

function insertList() {
  const el = bodyRef.value;
  if (!el) return;
  const start = el.selectionStart;
  form.value.body = form.value.body.slice(0, start) + "\n- " + form.value.body.slice(start);
}

const statusLabels = { published: "منتشر شده", draft: "پیش‌نویس" };

function parsedBody(body) {
  if (!body) return "";
  return body
    .replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" class="max-w-full my-3 rounded" />')
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    .replace(/\n- ([^\n]+)/g, "<li class='mr-4 list-disc'>$1</li>")
    .replace(/\n/g, "<br />");
}
</script>

<template>
  <div class="p-6 md:p-10">
    <div class="mb-8 flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 class="text-3xl font-light">بلاگ <span class="text-maroon">.</span></h1>
        <p class="mt-2 text-sm text-muted-foreground">{{ counts.published }} منتشر شده · {{ counts.draft }} پیش‌نویس</p>
      </div>
      <button @click="openCreate" class="inline-flex items-center gap-2 bg-maroon px-5 py-3 text-sm text-maroon-foreground hover:opacity-90">
        <Plus class="h-4 w-4" /> مقاله جدید
      </button>
    </div>

    <!-- Filter tabs -->
    <div class="mb-6 flex gap-1 border-b border-border">
      <button
        v-for="f in [{ v: 'all', l: 'همه', c: counts.all }, { v: 'published', l: 'منتشر شده', c: counts.published }, { v: 'draft', l: 'پیش‌نویس', c: counts.draft }]"
        :key="f.v"
        @click="filter = f.v"
        :class="['px-4 py-2.5 text-sm transition-colors relative', filter === f.v ? 'text-foreground after:absolute after:bottom-0 after:right-0 after:left-0 after:h-0.5 after:bg-maroon' : 'text-muted-foreground hover:text-foreground']"
      >
        {{ f.l }} <span class="mr-1 text-xs text-muted-foreground">({{ f.c }})</span>
      </button>
    </div>

    <!-- Posts list -->
    <div class="divide-y divide-border border-y border-border">
      <div v-for="p in filtered" :key="p.slug" class="flex items-start gap-4 py-5">
        <!-- Cover thumbnail -->
        <div class="hidden shrink-0 sm:block">
          <img v-if="p.coverImage" :src="p.coverImage" alt="" class="h-16 w-24 object-cover" />
          <div v-else class="h-16 w-24 bg-muted flex items-center justify-center text-muted-foreground">
            <Image class="h-5 w-5" />
          </div>
        </div>

        <div class="flex-1 min-w-0">
          <div class="flex items-start justify-between gap-3">
            <div class="min-w-0">
              <div class="font-medium truncate">{{ p.title }}</div>
              <div class="mt-1 flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
                <span>{{ p.date }}</span>
                <span v-if="p.category" class="border border-border px-2 py-0.5">{{ p.category }}</span>
                <span>{{ p.readTime }}</span>
              </div>
              <p v-if="p.excerpt" class="mt-1.5 text-sm text-muted-foreground line-clamp-2">{{ p.excerpt }}</p>
            </div>

            <!-- Status + actions -->
            <div class="flex shrink-0 items-center gap-2">
              <button
                @click="toggleStatus(p)"
                :class="['flex items-center gap-1.5 px-2.5 py-1 text-xs transition-colors', p.status === 'published' ? 'bg-maroon/10 text-maroon hover:bg-maroon/20' : 'border border-border text-muted-foreground hover:bg-accent']"
                :title="p.status === 'published' ? 'تبدیل به پیش‌نویس' : 'انتشار'"
              >
                <Eye v-if="p.status === 'published'" class="h-3 w-3" />
                <EyeOff v-else class="h-3 w-3" />
                {{ statusLabels[p.status] }}
              </button>
              <button @click="openEdit(p)" class="p-2 hover:bg-accent hover:text-maroon"><Pencil class="h-4 w-4" /></button>
              <button @click="remove(p.slug)" class="p-2 hover:bg-accent"><Trash2 class="h-4 w-4 text-maroon" /></button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="filtered.length === 0" class="py-16 text-center text-muted-foreground text-sm">
        مقاله‌ای با این فیلتر پیدا نشد.
      </div>
    </div>
  </div>

  <!-- Drawer -->
  <template v-if="drawer.mode !== 'closed'">
    <div class="fixed inset-0 z-40 bg-foreground/40 backdrop-blur-sm" @click="drawer = { mode: 'closed' }" />
    <aside class="fixed bottom-0 left-0 top-0 z-50 flex w-full max-w-2xl flex-col border-l border-maroon/30 bg-background">
      <header class="flex items-center justify-between border-b border-border px-6 py-4 shrink-0">
        <div>
          <div class="text-xs uppercase tracking-widest text-maroon">{{ drawer.mode === "edit" ? "ویرایش مقاله" : "مقاله جدید" }}</div>
          <h2 class="mt-0.5 text-lg font-light truncate max-w-xs">{{ form.title || "بدون عنوان" }}</h2>
        </div>
        <button @click="drawer = { mode: 'closed' }" class="p-2 hover:bg-accent"><X class="h-4 w-4" /></button>
      </header>

      <form @submit="submitForm" class="flex flex-1 flex-col overflow-hidden">
        <div class="flex-1 overflow-y-auto space-y-5 p-6">

          <!-- Title -->
          <label class="block">
            <span class="field-label">عنوان مقاله *</span>
            <input required v-model="form.title" class="inp mt-1.5" placeholder="عنوان را اینجا بنویسید..." />
          </label>

          <!-- Meta row -->
          <div class="grid grid-cols-2 gap-4">
            <label class="block">
              <span class="field-label">دسته‌بندی</span>
              <input v-model="form.category" class="inp mt-1.5" placeholder="مثلاً: آموزش دم‌آوری" />
            </label>
            <label class="block">
              <span class="field-label">زمان مطالعه</span>
              <input v-model="form.readTime" class="inp mt-1.5" placeholder="۵ دقیقه" />
            </label>
          </div>

          <!-- Status -->
          <div>
            <span class="field-label">وضعیت</span>
            <div class="mt-2 flex gap-3">
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" value="draft" v-model="form.status" class="accent-[var(--maroon)]" />
                <span class="text-sm">پیش‌نویس</span>
              </label>
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="radio" value="published" v-model="form.status" class="accent-[var(--maroon)]" />
                <span class="text-sm">منتشر شده</span>
              </label>
            </div>
          </div>

          <!-- Cover image -->
          <div>
            <span class="field-label">تصویر کاور</span>
            <div class="mt-1.5">
              <img v-if="form.coverImage" :src="form.coverImage" alt="" class="mb-2 h-32 w-full object-cover border border-border" />
              <label class="flex cursor-pointer items-center gap-2 border border-dashed border-border px-4 py-3 text-sm text-muted-foreground hover:border-maroon hover:text-maroon transition-colors">
                <Image class="h-4 w-4" />
                {{ form.coverImage ? "تغییر تصویر کاور" : "انتخاب تصویر کاور" }}
                <input type="file" accept="image/*" class="hidden" @change="handleImageUpload" />
              </label>
              <button v-if="form.coverImage" type="button" @click="form.coverImage = ''" class="mt-1 text-xs text-maroon hover:underline">حذف تصویر</button>
            </div>
          </div>

          <!-- Excerpt -->
          <label class="block">
            <span class="field-label">خلاصه (نمایش در لیست بلاگ)</span>
            <textarea v-model="form.excerpt" rows="2" class="inp mt-1.5 resize-none" placeholder="یک یا دو جمله خلاصه..." />
          </label>

          <!-- Body editor -->
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <span class="field-label">محتوای مقاله</span>
              <div class="flex items-center gap-1">
                <button type="button" @click="wrapText('**')" class="p-1.5 border border-border hover:bg-accent text-xs" title="بولد"><Bold class="h-3.5 w-3.5" /></button>
                <button type="button" @click="wrapText('*')" class="p-1.5 border border-border hover:bg-accent text-xs" title="ایتالیک"><Italic class="h-3.5 w-3.5" /></button>
                <button type="button" @click="insertList()" class="p-1.5 border border-border hover:bg-accent text-xs" title="لیست"><List class="h-3.5 w-3.5" /></button>
                <label class="p-1.5 border border-border hover:bg-accent cursor-pointer" title="افزودن عکس">
                  <Image class="h-3.5 w-3.5" />
                  <input type="file" accept="image/*" class="hidden" @change="insertBodyImage" />
                </label>
              </div>
            </div>
            <textarea
              ref="bodyRef"
              v-model="form.body"
              rows="14"
              class="inp resize-y font-mono text-xs"
              placeholder="محتوای مقاله را اینجا بنویسید...&#10;&#10;از **متن بولد**، *ایتالیک* و دکمه‌های بالا استفاده کنید."
            />
            <p class="mt-1 text-xs text-muted-foreground">فرمت: **بولد** · *ایتالیک* · - لیست · ![عنوان](url) برای تصویر</p>
          </div>
        </div>

        <footer class="shrink-0 flex items-center justify-end gap-3 border-t border-border bg-muted/30 px-6 py-4">
          <button type="button" @click="drawer = { mode: 'closed' }" class="border border-border px-5 py-2.5 text-sm hover:bg-accent">انصراف</button>
          <button type="submit" class="bg-maroon px-6 py-2.5 text-sm text-maroon-foreground hover:opacity-90">
            {{ drawer.mode === "edit" ? "ذخیره تغییرات" : "ساخت مقاله" }}
          </button>
        </footer>
      </form>
    </aside>
  </template>
</template>

<style scoped>
.inp {
  display: block;
  width: 100%;
  border: 1px solid var(--color-border);
  background-color: var(--color-background);
  padding: 0.625rem 0.75rem;
  font-size: 0.875rem;
  outline: none;
}
.inp:focus { border-color: var(--color-maroon); }
.field-label {
  display: block;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--muted-foreground);
}
</style>
