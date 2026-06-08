<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useTemplatesStore } from "@/stores/templates.js";
import { Plus, Pencil, Trash2, X, ChevronDown, ChevronUp, ArrowLeft } from "lucide-vue-next";

const router = useRouter();

const store = useTemplatesStore();
const expanded = ref(null);
const drawer = ref({ mode: "closed" });

const emptyForm = () => ({
  name: "", description: "",
  weights: [
    { label: "۲۵۰ گرم", multiplier: 1 },
    { label: "۵۰۰ گرم", multiplier: 1.9 },
    { label: "۱ کیلوگرم", multiplier: 3.5 },
  ],
  grinds: ["دانه کامل", "اسپرسو", "فرنچ پرس"],
  attributes: [],
  defaultRoast: "متوسط",
  defaultProcess: "شسته",
});

const form = ref(emptyForm());
const grindsText = ref("");
const drawerTab = ref("basic");

function openCreate() {
  form.value = emptyForm();
  grindsText.value = form.value.grinds.join("، ");
  drawerTab.value = "basic";
  drawer.value = { mode: "create" };
}

function openEdit(tpl) {
  form.value = {
    name: tpl.name, description: tpl.description,
    weights: [...tpl.weights.map((w) => ({ ...w }))],
    grinds: [...tpl.grinds],
    attributes: tpl.attributes.map((a) => ({ ...a, options: [...a.options] })),
    defaultRoast: tpl.defaultRoast,
    defaultProcess: tpl.defaultProcess,
  };
  grindsText.value = tpl.grinds.join("، ");
  drawerTab.value = "basic";
  drawer.value = { mode: "edit", tpl };
}

function remove(id) {
  if (confirm("این قالب حذف شود؟")) store.remove(id);
}

function submitForm(e) {
  e.preventDefault();
  const data = {
    ...form.value,
    grinds: grindsText.value.split("،").map((g) => g.trim()).filter(Boolean),
    weights: form.value.weights.filter((w) => w.label.trim()),
    attributes: form.value.attributes.filter((a) => a.name.trim()),
  };
  if (drawer.value.mode === "edit") {
    store.update({ ...data, id: drawer.value.tpl.id, createdAt: drawer.value.tpl.createdAt });
  } else {
    store.add(data);
  }
  drawer.value = { mode: "closed" };
}

function addWeight() { form.value.weights.push({ label: "", multiplier: 1 }); }
function removeWeight(i) { form.value.weights.splice(i, 1); }
function addAttr() { form.value.attributes.push({ id: Date.now().toString(), name: "", options: [{ value: "" }] }); }
function removeAttr(i) { form.value.attributes.splice(i, 1); }
function addOption(attrIdx) { form.value.attributes[attrIdx].options.push({ value: "" }); }
function removeOption(attrIdx, optIdx) { form.value.attributes[attrIdx].options.splice(optIdx, 1); }

const cls = "w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon";
</script>

<template>
  <div class="p-10">
    <div class="mb-10 flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 class="text-3xl font-light">قالب‌های محصول <span class="text-maroon">.</span></h1>
        <p class="mt-2 text-sm text-muted-foreground">قالب‌ها مجموعه‌ای از ویژگی‌ها هستند که می‌توانید هنگام ساخت محصول اعمال کنید</p>
      </div>
      <button type="button" @click="openCreate" class="inline-flex items-center gap-2 bg-maroon px-5 py-3 text-sm text-maroon-foreground hover:opacity-90">
        <Plus class="h-4 w-4" /> قالب جدید
      </button>
    </div>

    <div class="space-y-3">
      <div v-for="tpl in store.templates" :key="tpl.id" class="border border-border">
        <div class="flex cursor-pointer items-center justify-between p-5 hover:bg-accent/30" @click="expanded = expanded === tpl.id ? null : tpl.id">
          <div class="flex items-center gap-4">
            <div>
              <div class="font-medium">{{ tpl.name }}</div>
              <div class="mt-0.5 text-xs text-muted-foreground">{{ tpl.description }}</div>
            </div>
            <div class="hidden items-center gap-3 text-xs text-muted-foreground md:flex">
              <span class="border border-border px-2 py-1">{{ tpl.weights.length }} وزن</span>
              <span class="border border-border px-2 py-1">{{ tpl.grinds.length }} آسیاب</span>
              <span class="border border-border px-2 py-1">{{ tpl.attributes.length }} ویژگی</span>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <span class="hidden text-xs text-muted-foreground md:block">{{ tpl.createdAt }}</span>
            <button
              type="button"
              @click.stop="router.push('/admin/products?template=' + tpl.id)"
              class="hidden md:inline-flex items-center gap-1.5 border border-maroon/40 px-3 py-1.5 text-xs text-maroon hover:bg-maroon hover:text-maroon-foreground transition-colors"
              title="ساخت محصول با این قالب"
            >
              ساخت محصول <ArrowLeft class="h-3 w-3" />
            </button>
            <button type="button" @click.stop="openEdit(tpl)" class="p-2 hover:bg-accent hover:text-maroon"><Pencil class="h-4 w-4" /></button>
            <button type="button" @click.stop="remove(tpl.id)" class="p-2 hover:bg-accent"><Trash2 class="h-4 w-4 text-maroon" /></button>
            <ChevronUp v-if="expanded === tpl.id" class="h-4 w-4 text-muted-foreground" />
            <ChevronDown v-else class="h-4 w-4 text-muted-foreground" />
          </div>
        </div>

        <div v-if="expanded === tpl.id" class="border-t border-border bg-muted/30 p-5">
          <div class="grid gap-6 md:grid-cols-3">
            <div>
              <div class="mb-3 text-xs uppercase tracking-widest text-maroon">وزن‌ها</div>
              <div class="space-y-1.5">
                <div v-for="w in tpl.weights" :key="w.label" class="flex items-center justify-between text-sm">
                  <span>{{ w.label }}</span>
                  <span class="text-muted-foreground">×{{ w.multiplier }}</span>
                </div>
              </div>
            </div>
            <div>
              <div class="mb-3 text-xs uppercase tracking-widest text-maroon">انواع آسیاب</div>
              <div class="flex flex-wrap gap-1.5">
                <span v-for="g in tpl.grinds" :key="g" class="border border-border px-2 py-1 text-xs">{{ g }}</span>
              </div>
            </div>
            <div v-if="tpl.attributes.length > 0">
              <div class="mb-3 text-xs uppercase tracking-widest text-maroon">ویژگی‌های سفارشی</div>
              <div class="space-y-2">
                <div v-for="attr in tpl.attributes" :key="attr.id">
                  <div class="text-xs font-medium">{{ attr.name }}</div>
                  <div class="mt-1 flex flex-wrap gap-1">
                    <span v-for="o in attr.options" :key="o.value" class="bg-border/60 px-2 py-0.5 text-xs">{{ o.value }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="mt-4 flex items-center gap-4 text-xs text-muted-foreground">
            <span>رست پیش‌فرض: <strong>{{ tpl.defaultRoast }}</strong></span>
            <span>فرآوری پیش‌فرض: <strong>{{ tpl.defaultProcess }}</strong></span>
          </div>
        </div>
      </div>

      <div v-if="store.templates.length === 0" class="border border-dashed border-border p-16 text-center text-muted-foreground">
        هنوز قالبی تعریف نشده است.
      </div>
    </div>

    <!-- Drawer -->
    <template v-if="drawer.mode !== 'closed'">
      <div class="fixed inset-0 z-40 bg-foreground/40 backdrop-blur-sm" @click="drawer = { mode: 'closed' }" />
      <aside class="fixed bottom-0 left-0 top-0 z-50 flex w-full max-w-xl flex-col border-l border-maroon/30 bg-background">
        <header class="flex items-center justify-between border-b border-border p-6">
          <div>
            <div class="text-xs uppercase tracking-widest text-maroon">{{ drawer.mode === "edit" ? "ویرایش قالب" : "قالب جدید" }}</div>
            <h2 class="mt-1 text-xl font-light">{{ drawer.mode === "edit" ? form.name || "بدون نام" : "ساخت قالب" }}</h2>
          </div>
          <button type="button" @click="drawer = { mode: 'closed' }" class="p-2 hover:bg-accent"><X class="h-4 w-4" /></button>
        </header>

        <div class="flex border-b border-border">
          <button
            v-for="t in [{ id: 'basic', label: 'اطلاعات پایه' }, { id: 'weights', label: 'وزن‌ها' }, { id: 'grinds', label: 'آسیاب' }, { id: 'attributes', label: 'ویژگی‌ها' }]"
            :key="t.id"
            type="button"
            @click="drawerTab = t.id"
            :class="['flex flex-1 items-center justify-center px-3 py-3 text-xs transition-colors', drawerTab === t.id ? 'border-b-2 border-maroon text-maroon' : 'text-muted-foreground hover:text-foreground']"
          >
            {{ t.label }}
          </button>
        </div>

        <form @submit="submitForm" class="flex flex-1 flex-col overflow-y-auto">
          <div class="space-y-5 p-6">
            <template v-if="drawerTab === 'basic'">
              <label class="block">
                <span class="text-xs uppercase tracking-widest text-muted-foreground">نام قالب</span>
                <input required v-model="form.name" :class="`mt-2 ${cls}`" />
              </label>
              <label class="block">
                <span class="text-xs uppercase tracking-widest text-muted-foreground">توضیحات</span>
                <textarea rows="3" v-model="form.description" :class="`mt-2 ${cls} resize-none`" />
              </label>
              <div class="grid grid-cols-2 gap-4">
                <label class="block">
                  <span class="text-xs uppercase tracking-widest text-muted-foreground">رست پیش‌فرض</span>
                  <select v-model="form.defaultRoast" :class="`mt-2 ${cls}`">
                    <option>روشن</option><option>متوسط</option><option>تیره</option>
                  </select>
                </label>
                <label class="block">
                  <span class="text-xs uppercase tracking-widest text-muted-foreground">فرآوری پیش‌فرض</span>
                  <input v-model="form.defaultProcess" :class="`mt-2 ${cls}`" />
                </label>
              </div>
            </template>

            <template v-if="drawerTab === 'weights'">
              <div>
                <div class="mb-4 flex items-center justify-between">
                  <span class="text-xs uppercase tracking-widest text-maroon">وزن‌ها ({{ form.weights.length }})</span>
                  <button type="button" @click="addWeight" class="text-xs text-maroon hover:underline">+ افزودن</button>
                </div>
                <div class="space-y-2">
                  <div v-for="(w, i) in form.weights" :key="i" class="grid grid-cols-[1fr_120px_32px] items-center gap-2">
                    <input v-model="w.label" placeholder="۲۵۰ گرم" :class="cls" />
                    <input type="number" step="0.05" v-model.number="w.multiplier" :class="cls" />
                    <button type="button" @click="removeWeight(i)" class="text-muted-foreground hover:text-maroon">
                      <Trash2 class="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            </template>

            <template v-if="drawerTab === 'grinds'">
              <label class="block">
                <span class="text-xs uppercase tracking-widest text-muted-foreground">انواع آسیاب (با ، جدا کنید)</span>
                <input v-model="grindsText" :class="`mt-2 ${cls}`" />
              </label>
              <div class="flex flex-wrap gap-2">
                <span v-for="g in grindsText.split('،').map((g) => g.trim()).filter(Boolean)" :key="g" class="border border-maroon/40 px-3 py-1.5 text-sm">{{ g }}</span>
              </div>
            </template>

            <template v-if="drawerTab === 'attributes'">
              <div class="mb-4 flex items-center justify-between">
                <span class="text-xs uppercase tracking-widest text-maroon">ویژگی‌های سفارشی ({{ form.attributes.length }})</span>
                <button type="button" @click="addAttr" class="text-xs text-maroon hover:underline">+ افزودن ویژگی</button>
              </div>
              <div class="space-y-5">
                <div v-for="(attr, i) in form.attributes" :key="attr.id" class="border border-border p-4">
                  <div class="mb-3 flex items-center justify-between gap-2">
                    <input v-model="attr.name" placeholder="نام ویژگی" :class="`flex-1 ${cls} font-medium`" />
                    <button type="button" @click="removeAttr(i)" class="p-1 text-muted-foreground hover:text-maroon">
                      <Trash2 class="h-4 w-4" />
                    </button>
                  </div>
                  <div class="space-y-2">
                    <div v-for="(opt, j) in attr.options" :key="j" class="flex items-center gap-2">
                      <span class="w-4 text-xs text-muted-foreground">{{ j + 1 }}</span>
                      <input v-model="opt.value" placeholder="مقدار گزینه" :class="cls" />
                      <button type="button" @click="removeOption(i, j)" class="text-muted-foreground hover:text-maroon">
                        <X class="h-4 w-4" />
                      </button>
                    </div>
                    <button type="button" @click="addOption(i)" class="mt-1 text-xs text-maroon hover:underline">+ افزودن گزینه</button>
                  </div>
                </div>
                <div v-if="form.attributes.length === 0" class="border border-dashed border-border p-8 text-center text-xs text-muted-foreground">
                  ویژگی سفارشی تعریف نشده است.
                </div>
              </div>
            </template>
          </div>

          <footer class="mt-auto flex items-center justify-end gap-3 border-t border-border bg-muted/30 p-6">
            <button type="button" @click="drawer = { mode: 'closed' }" class="border border-border px-5 py-2.5 text-sm hover:bg-accent">انصراف</button>
            <button type="submit" class="bg-maroon px-6 py-2.5 text-sm text-maroon-foreground hover:opacity-90">
              {{ drawer.mode === "edit" ? "ذخیره تغییرات" : "ساخت قالب" }}
            </button>
          </footer>
        </form>
      </aside>
    </template>
  </div>
</template>
