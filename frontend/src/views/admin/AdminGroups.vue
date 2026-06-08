<script setup>
import { ref, computed } from "vue";
import { useGroupsStore } from "@/stores/groups.js";
import { Plus, Pencil, Trash2, X, ChevronDown, ChevronUp } from "lucide-vue-next";

const store = useGroupsStore();
const expanded = ref(null);
const drawer = ref({ mode: "closed" });
const drawerTab = ref("basic");

const typeLabels = { coffee: "قهوه", accessory: "اکسسوری", equipment: "دستگاه", other: "سایر" };

function emptyForm() {
  return {
    name: "", type: "coffee", description: "",
    weights: [{ label: "۲۵۰ گرم", multiplier: 1 }, { label: "۵۰۰ گرم", multiplier: 1.9 }, { label: "۱ کیلوگرم", multiplier: 3.5 }],
    grinds: ["دانه کامل", "اسپرسو", "فرنچ پرس"],
    attributes: [],
  };
}

const form = ref(emptyForm());
const grindsText = ref("");

function openCreate() {
  form.value = emptyForm();
  grindsText.value = form.value.grinds.join("، ");
  drawerTab.value = "basic";
  drawer.value = { mode: "create" };
}

function openEdit(g) {
  form.value = {
    name: g.name, type: g.type, description: g.description,
    weights: g.weights.map(w => ({ ...w })),
    grinds: [...g.grinds],
    attributes: g.attributes.map(a => ({ ...a, options: [...a.options] })),
  };
  grindsText.value = g.grinds.join("، ");
  drawerTab.value = "basic";
  drawer.value = { mode: "edit", group: g };
}

function submitForm(e) {
  e.preventDefault();
  const data = {
    ...form.value,
    grinds: grindsText.value.split("،").map(g => g.trim()).filter(Boolean),
    weights: form.value.weights.filter(w => w.label.trim()),
    attributes: form.value.attributes.filter(a => a.name.trim()),
  };
  if (drawer.value.mode === "edit") {
    store.update({ ...data, id: drawer.value.group.id, createdAt: drawer.value.group.createdAt });
  } else {
    store.create(data);
  }
  drawer.value = { mode: "closed" };
}

function addWeight() { form.value.weights.push({ label: "", multiplier: 1 }); }
function removeWeight(i) { form.value.weights.splice(i, 1); }
function addAttr() { form.value.attributes.push({ id: Date.now().toString(), name: "", required: false, options: [] }); }
function removeAttr(i) { form.value.attributes.splice(i, 1); }
function addOption(ai) { form.value.attributes[ai].options.push(""); }
function removeOption(ai, oi) { form.value.attributes[ai].options.splice(oi, 1); }

const byType = computed(() => {
  const map = {};
  for (const g of store.groups) {
    const t = g.type || "other";
    if (!map[t]) map[t] = [];
    map[t].push(g);
  }
  return map;
});

const inp = "w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon";
</script>

<template>
  <div class="p-6 md:p-10">
    <div class="mb-8 flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 class="text-3xl font-light">گروه‌های محصول <span class="text-maroon">.</span></h1>
        <p class="mt-2 text-sm text-muted-foreground">دسته‌بندی محصولات و ویژگی‌های هر گروه را اینجا تعریف کنید</p>
      </div>
      <button type="button" @click="openCreate" class="inline-flex items-center gap-2 bg-maroon px-5 py-3 text-sm text-maroon-foreground hover:opacity-90">
        <Plus class="h-4 w-4" /> گروه جدید
      </button>
    </div>

    <!-- Groups by type -->
    <div v-for="(groups, type) in byType" :key="type" class="mb-8">
      <div class="mb-3 flex items-center gap-3">
        <span class="text-xs uppercase tracking-widest text-maroon">{{ typeLabels[type] || type }}</span>
        <span class="text-xs text-muted-foreground">({{ groups.length }} گروه)</span>
      </div>
      <div class="space-y-2">
        <div v-for="g in groups" :key="g.id" class="border border-border">
          <div
            class="flex cursor-pointer items-center justify-between p-4 hover:bg-accent/30"
            @click="expanded = expanded === g.id ? null : g.id"
          >
            <div class="flex items-center gap-4 min-w-0">
              <div class="min-w-0">
                <div class="font-medium text-sm truncate">{{ g.name }}</div>
                <div class="mt-0.5 text-xs text-muted-foreground truncate">{{ g.description }}</div>
              </div>
              <div class="hidden sm:flex items-center gap-2 shrink-0">
                <span v-if="g.attributes.length" class="border border-border px-2 py-0.5 text-xs">{{ g.attributes.length }} ویژگی</span>
                <span v-if="g.weights.length" class="border border-border px-2 py-0.5 text-xs">{{ g.weights.length }} وزن</span>
                <span v-if="g.grinds.length" class="border border-border px-2 py-0.5 text-xs">{{ g.grinds.length }} آسیاب</span>
              </div>
            </div>
            <div class="flex items-center gap-1 shrink-0 mr-3">
              <button type="button" @click.stop="openEdit(g)" class="p-2 hover:bg-accent hover:text-maroon">
                <Pencil class="h-3.5 w-3.5" />
              </button>
              <button type="button" @click.stop="store.remove(g.id)" class="p-2 hover:bg-accent">
                <Trash2 class="h-3.5 w-3.5 text-maroon" />
              </button>
              <ChevronUp v-if="expanded === g.id" class="h-4 w-4 text-muted-foreground" />
              <ChevronDown v-else class="h-4 w-4 text-muted-foreground" />
            </div>
          </div>

          <div v-if="expanded === g.id" class="border-t border-border bg-muted/30 p-5">
            <div class="grid gap-6 md:grid-cols-3">
              <div v-if="g.attributes.length">
                <div class="mb-3 text-xs uppercase tracking-widest text-maroon">ویژگی‌ها</div>
                <div class="space-y-3">
                  <div v-for="attr in g.attributes" :key="attr.id">
                    <div class="text-xs font-medium flex items-center gap-2">
                      {{ attr.name }}
                      <span v-if="attr.required" class="text-maroon text-xs">*اجباری</span>
                    </div>
                    <div class="mt-1 flex flex-wrap gap-1">
                      <span v-for="o in attr.options" :key="o" class="bg-border/50 px-2 py-0.5 text-xs">{{ o }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div v-if="g.weights.length">
                <div class="mb-3 text-xs uppercase tracking-widest text-maroon">وزن‌ها</div>
                <div class="space-y-1">
                  <div v-for="w in g.weights" :key="w.label" class="flex items-center justify-between text-xs">
                    <span>{{ w.label }}</span>
                    <span class="text-muted-foreground">×{{ w.multiplier }}</span>
                  </div>
                </div>
              </div>
              <div v-if="g.grinds.length">
                <div class="mb-3 text-xs uppercase tracking-widest text-maroon">انواع آسیاب</div>
                <div class="flex flex-wrap gap-1">
                  <span v-for="gr in g.grinds" :key="gr" class="border border-border px-2 py-0.5 text-xs">{{ gr }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="store.groups.length === 0" class="border border-dashed border-border p-16 text-center text-muted-foreground">
      هنوز گروهی تعریف نشده است.
    </div>

    <!-- Drawer -->
    <template v-if="drawer.mode !== 'closed'">
      <div class="fixed inset-0 z-40 bg-foreground/40 backdrop-blur-sm" @click="drawer = { mode: 'closed' }" />
      <aside class="fixed bottom-0 left-0 top-0 z-50 flex w-full max-w-xl flex-col border-l border-maroon/30 bg-background">
        <header class="flex items-center justify-between border-b border-border p-5">
          <div>
            <div class="text-xs uppercase tracking-widest text-maroon">{{ drawer.mode === "edit" ? "ویرایش گروه" : "گروه جدید" }}</div>
            <h2 class="mt-1 text-xl font-light">{{ drawer.mode === "edit" ? form.name : "ساخت گروه محصول" }}</h2>
          </div>
          <button type="button" @click="drawer = { mode: 'closed' }" class="p-2 hover:bg-accent"><X class="h-4 w-4" /></button>
        </header>

        <div class="flex border-b border-border overflow-x-auto">
          <button
            v-for="tab in [
              { id: 'basic', label: 'پایه' },
              { id: 'attrs', label: 'ویژگی‌ها' },
              { id: 'weights', label: 'وزن' },
              { id: 'grinds', label: 'آسیاب' },
            ]"
            :key="tab.id"
            type="button"
            @click="drawerTab = tab.id"
            :class="['shrink-0 flex-1 px-3 py-3 text-xs transition-colors', drawerTab === tab.id ? 'border-b-2 border-maroon text-maroon' : 'text-muted-foreground hover:text-foreground']"
          >
            {{ tab.label }}
          </button>
        </div>

        <form @submit="submitForm" class="flex flex-1 flex-col overflow-y-auto">
          <div class="space-y-4 p-5">

            <!-- Basic -->
            <template v-if="drawerTab === 'basic'">
              <label class="block">
                <span class="field-label">نام گروه</span>
                <input required v-model="form.name" :class="`mt-1.5 ${inp}`" placeholder="مثلاً: قهوه تک‌خاستگاه" />
              </label>
              <label class="block">
                <span class="field-label">نوع</span>
                <select v-model="form.type" :class="`mt-1.5 ${inp}`">
                  <option value="coffee">قهوه</option>
                  <option value="accessory">اکسسوری</option>
                  <option value="equipment">دستگاه</option>
                  <option value="other">سایر</option>
                </select>
              </label>
              <label class="block">
                <span class="field-label">توضیحات</span>
                <textarea v-model="form.description" rows="3" :class="`mt-1.5 ${inp} resize-none`" />
              </label>
            </template>

            <!-- Attributes -->
            <template v-if="drawerTab === 'attrs'">
              <div class="flex items-center justify-between">
                <span class="text-xs uppercase tracking-widest text-maroon">ویژگی‌های محصول ({{ form.attributes.length }})</span>
                <button type="button" @click="addAttr" class="text-xs text-maroon hover:underline">+ افزودن ویژگی</button>
              </div>
              <div class="space-y-4">
                <div v-for="(attr, ai) in form.attributes" :key="attr.id" class="border border-border p-4 space-y-3">
                  <div class="flex items-center gap-2">
                    <input v-model="attr.name" placeholder="نام ویژگی (مثلاً: کشور)" :class="`flex-1 ${inp} font-medium`" />
                    <label class="flex items-center gap-1.5 text-xs shrink-0">
                      <input type="checkbox" v-model="attr.required" class="accent-[var(--maroon)]" />
                      اجباری
                    </label>
                    <button type="button" @click="removeAttr(ai)" class="p-1 text-muted-foreground hover:text-maroon shrink-0">
                      <Trash2 class="h-4 w-4" />
                    </button>
                  </div>
                  <div class="space-y-1.5">
                    <div v-for="(opt, oi) in attr.options" :key="oi" class="flex items-center gap-2">
                      <input v-model="attr.options[oi]" placeholder="مقدار گزینه" :class="`flex-1 border border-border bg-background px-3 py-1.5 text-sm outline-none focus:border-maroon`" />
                      <button type="button" @click="removeOption(ai, oi)" class="text-muted-foreground hover:text-maroon">
                        <X class="h-4 w-4" />
                      </button>
                    </div>
                    <button type="button" @click="addOption(ai)" class="text-xs text-maroon hover:underline">+ گزینه جدید</button>
                  </div>
                </div>
                <div v-if="form.attributes.length === 0" class="border border-dashed border-border p-8 text-center text-xs text-muted-foreground">
                  ویژگی‌ای تعریف نشده. با کلیک «افزودن ویژگی» شروع کنید.
                </div>
              </div>
            </template>

            <!-- Weights -->
            <template v-if="drawerTab === 'weights'">
              <div class="flex items-center justify-between">
                <span class="text-xs uppercase tracking-widest text-maroon">وزن‌ها</span>
                <button type="button" @click="addWeight" class="text-xs text-maroon hover:underline">+ افزودن</button>
              </div>
              <div class="space-y-2">
                <div v-for="(w, i) in form.weights" :key="i" class="grid grid-cols-[1fr_110px_32px] items-center gap-2">
                  <input v-model="w.label" placeholder="۲۵۰ گرم" :class="inp" />
                  <div class="flex items-center gap-1">
                    <span class="text-xs text-muted-foreground">×</span>
                    <input type="number" step="0.05" v-model.number="w.multiplier" :class="`flex-1 ${inp}`" />
                  </div>
                  <button type="button" @click="removeWeight(i)" class="text-muted-foreground hover:text-maroon">
                    <Trash2 class="h-4 w-4" />
                  </button>
                </div>
                <p v-if="!form.weights.length" class="text-xs text-muted-foreground py-4 text-center">برای اکسسوری می‌توانید این بخش را خالی بگذارید.</p>
              </div>
            </template>

            <!-- Grinds -->
            <template v-if="drawerTab === 'grinds'">
              <label class="block">
                <span class="field-label">انواع آسیاب (با ، جدا کنید)</span>
                <input v-model="grindsText" :class="`mt-1.5 ${inp}`" placeholder="دانه کامل، اسپرسو، فرنچ پرس" />
              </label>
              <div class="flex flex-wrap gap-2 mt-2">
                <span v-for="g in grindsText.split('،').map(g => g.trim()).filter(Boolean)" :key="g" class="border border-maroon/40 px-3 py-1 text-sm">{{ g }}</span>
              </div>
              <p v-if="!grindsText.trim()" class="text-xs text-muted-foreground">برای اکسسوری می‌توانید این بخش را خالی بگذارید.</p>
            </template>
          </div>

          <footer class="mt-auto flex items-center justify-end gap-3 border-t border-border bg-muted/30 p-5">
            <button type="button" @click="drawer = { mode: 'closed' }" class="border border-border px-5 py-2.5 text-sm hover:bg-accent">انصراف</button>
            <button type="submit" class="bg-maroon px-6 py-2.5 text-sm text-maroon-foreground hover:opacity-90">
              {{ drawer.mode === "edit" ? "ذخیره" : "ساخت گروه" }}
            </button>
          </footer>
        </form>
      </aside>
    </template>
  </div>
</template>

<style scoped>
.field-label {
  display: block;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--muted-foreground);
}
</style>
