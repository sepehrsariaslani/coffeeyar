<script setup>
import { ref, computed } from "vue";
import { Plus, Trash2, ToggleLeft, ToggleRight, Tag } from "lucide-vue-next";
import { useCouponsStore } from "@/stores/coupons.js";
import { formatPrice } from "@/lib/data.js";

const store = useCouponsStore();

const showForm = ref(false);
const form = ref({ code: "", type: "percent", value: "", label: "", minOrder: "", maxUses: "", expiry: "", active: true });
const formError = ref("");

function submitAdd() {
  formError.value = "";
  if (!form.value.code.trim()) { formError.value = "کد تخفیف الزامی است"; return; }
  if (!form.value.value || isNaN(Number(form.value.value))) { formError.value = "مقدار تخفیف را وارد کنید"; return; }
  if (store.coupons.find((c) => c.code === form.value.code.trim().toUpperCase())) {
    formError.value = "این کد از قبل وجود دارد";
    return;
  }
  store.add({
    code: form.value.code.trim(),
    type: form.value.type,
    value: Number(form.value.value),
    label: form.value.label || (form.value.type === "percent" ? `${form.value.value}٪ تخفیف` : `${Number(form.value.value).toLocaleString("fa-IR")} تومان تخفیف`),
    minOrder: Number(form.value.minOrder) || 0,
    maxUses: Number(form.value.maxUses) || 0,
    expiry: form.value.expiry,
    active: true,
  });
  form.value = { code: "", type: "percent", value: "", label: "", minOrder: "", maxUses: "", expiry: "", active: true };
  showForm.value = false;
}

const totalSaved = computed(() => store.coupons.reduce((acc, c) => acc + c.used, 0));
</script>

<template>
  <div class="p-4 md:p-10">
    <div class="mb-8 flex items-start justify-between">
      <div>
        <h1 class="text-3xl font-light">کدهای تخفیف <span class="text-maroon">.</span></h1>
        <p class="mt-2 text-sm text-muted-foreground">مدیریت کدهای تخفیف فروشگاه</p>
      </div>
      <button
        @click="showForm = !showForm"
        class="flex items-center gap-2 bg-maroon px-4 py-2.5 text-sm text-white hover:opacity-90"
      >
        <Plus class="h-4 w-4" />
        کد جدید
      </button>
    </div>

    <!-- Stats -->
    <div class="mb-8 grid grid-cols-2 gap-px bg-border sm:grid-cols-3">
      <div class="bg-background p-5">
        <div class="text-xs uppercase tracking-widest text-muted-foreground">تعداد کدها</div>
        <div class="mt-3 text-2xl font-light">{{ store.coupons.length }}</div>
      </div>
      <div class="bg-background p-5">
        <div class="text-xs uppercase tracking-widest text-muted-foreground">کدهای فعال</div>
        <div class="mt-3 text-2xl font-light text-maroon">{{ store.coupons.filter(c => c.active).length }}</div>
      </div>
      <div class="bg-background p-5">
        <div class="text-xs uppercase tracking-widest text-muted-foreground">دفعات استفاده</div>
        <div class="mt-3 text-2xl font-light">{{ totalSaved }}</div>
      </div>
    </div>

    <!-- Add Form -->
    <div v-if="showForm" class="mb-8 border border-maroon/30 bg-maroon/5 p-6">
      <h2 class="mb-5 text-sm font-medium">افزودن کد تخفیف جدید</h2>
      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <label class="block">
          <span class="text-xs uppercase tracking-widest text-muted-foreground">کد تخفیف *</span>
          <input v-model="form.code" dir="ltr" placeholder="COFFEE20"
            class="mt-2 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon uppercase" />
        </label>
        <label class="block">
          <span class="text-xs uppercase tracking-widest text-muted-foreground">نوع تخفیف</span>
          <select v-model="form.type" class="mt-2 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon">
            <option value="percent">درصدی</option>
            <option value="fixed">مبلغ ثابت (تومان)</option>
          </select>
        </label>
        <label class="block">
          <span class="text-xs uppercase tracking-widest text-muted-foreground">مقدار تخفیف *</span>
          <input v-model="form.value" type="number" dir="ltr" :placeholder="form.type === 'percent' ? '10' : '50000'"
            class="mt-2 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
        </label>
        <label class="block">
          <span class="text-xs uppercase tracking-widest text-muted-foreground">برچسب (اختیاری)</span>
          <input v-model="form.label" placeholder="برای اولین خرید"
            class="mt-2 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
        </label>
        <label class="block">
          <span class="text-xs uppercase tracking-widest text-muted-foreground">حداقل خرید (تومان)</span>
          <input v-model="form.minOrder" type="number" dir="ltr" placeholder="0"
            class="mt-2 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
        </label>
        <label class="block">
          <span class="text-xs uppercase tracking-widest text-muted-foreground">حداکثر استفاده (۰ = نامحدود)</span>
          <input v-model="form.maxUses" type="number" dir="ltr" placeholder="0"
            class="mt-2 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
        </label>
        <label class="block">
          <span class="text-xs uppercase tracking-widest text-muted-foreground">تاریخ انقضا (اختیاری)</span>
          <input v-model="form.expiry" type="date" dir="ltr"
            class="mt-2 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
        </label>
      </div>
      <p v-if="formError" class="mt-3 text-xs text-red-600">{{ formError }}</p>
      <div class="mt-5 flex gap-3">
        <button @click="submitAdd" class="bg-maroon px-5 py-2.5 text-sm text-white hover:opacity-90">ذخیره کد</button>
        <button @click="showForm = false; formError = ''" class="border border-border px-5 py-2.5 text-sm text-muted-foreground hover:text-foreground">انصراف</button>
      </div>
    </div>

    <!-- Table -->
    <div v-if="store.coupons.length === 0" class="border border-dashed border-border py-16 text-center text-sm text-muted-foreground">
      <Tag class="mx-auto mb-3 h-8 w-8 opacity-30" />
      هنوز کدی اضافه نشده است.
    </div>

    <div v-else class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-border text-right text-xs uppercase tracking-widest text-muted-foreground">
            <th class="pb-3 font-normal">کد</th>
            <th class="pb-3 font-normal">نوع</th>
            <th class="pb-3 font-normal">مقدار</th>
            <th class="pb-3 font-normal hidden sm:table-cell">حداقل خرید</th>
            <th class="pb-3 font-normal hidden md:table-cell">استفاده</th>
            <th class="pb-3 font-normal hidden md:table-cell">انقضا</th>
            <th class="pb-3 font-normal">وضعیت</th>
            <th class="pb-3 font-normal"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-border">
          <tr v-for="c in store.coupons" :key="c.code" :class="['transition-colors hover:bg-muted/30', !c.active && 'opacity-50']">
            <td class="py-4">
              <div class="flex items-center gap-2">
                <span class="border border-maroon/40 bg-maroon/5 px-2 py-0.5 text-xs text-maroon font-mono tracking-wide">{{ c.code }}</span>
              </div>
              <div class="mt-0.5 text-xs text-muted-foreground">{{ c.label }}</div>
            </td>
            <td class="py-4 text-xs text-muted-foreground">{{ c.type === 'percent' ? 'درصدی' : 'ثابت' }}</td>
            <td class="py-4 font-medium text-maroon">
              {{ c.type === 'percent' ? `${c.value}٪` : formatPrice(c.value) }}
            </td>
            <td class="py-4 text-xs text-muted-foreground hidden sm:table-cell">
              {{ c.minOrder ? formatPrice(c.minOrder) : '—' }}
            </td>
            <td class="py-4 text-xs text-muted-foreground hidden md:table-cell">
              {{ c.used }} {{ c.maxUses ? `/ ${c.maxUses}` : '' }}
            </td>
            <td class="py-4 text-xs text-muted-foreground hidden md:table-cell">
              {{ c.expiry || '—' }}
            </td>
            <td class="py-4">
              <button @click="store.toggle(c.code)" class="flex items-center gap-1 text-xs">
                <ToggleRight v-if="c.active" class="h-5 w-5 text-maroon" />
                <ToggleLeft v-else class="h-5 w-5 text-muted-foreground" />
                <span :class="c.active ? 'text-maroon' : 'text-muted-foreground'">{{ c.active ? 'فعال' : 'غیرفعال' }}</span>
              </button>
            </td>
            <td class="py-4">
              <button @click="store.remove(c.code)" class="text-muted-foreground hover:text-red-500 transition-colors">
                <Trash2 class="h-4 w-4" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
