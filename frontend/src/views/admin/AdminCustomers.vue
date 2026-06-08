<script setup>
import { ref, computed } from "vue";
import { customers, formatPrice } from "@/lib/data.js";
import { Search, MapPin, Phone, Mail, ShoppingBag, X, Pencil, Check } from "lucide-vue-next";

const search = ref("");
const selected = ref(null);

const list = ref(customers.map(c => ({ ...c })));

const filtered = computed(() =>
  list.value.filter(
    (c) =>
      c.name.includes(search.value) ||
      c.email.includes(search.value) ||
      c.city.includes(search.value) ||
      c.phone.includes(search.value)
  )
);

const totalSpentAll = computed(() => list.value.reduce((s, c) => s + c.totalSpent, 0));
const totalOrdersAll = computed(() => list.value.reduce((s, c) => s + c.totalOrders, 0));

function toggleSelect(c) {
  selected.value = selected.value?.id === c.id ? null : c;
  inlineEdit.value = null;
}

const inlineEdit = ref(null);
const inlineForm = ref({});

function openInline(c) {
  if (inlineEdit.value === c.id) { inlineEdit.value = null; return; }
  selected.value = null;
  inlineForm.value = {
    id: c.id,
    name: c.name,
    email: c.email,
    phone: c.phone,
    city: c.city,
    totalOrders: c.totalOrders,
    totalSpent: c.totalSpent,
  };
  inlineEdit.value = c.id;
}

function saveInline() {
  list.value = list.value.map((c) =>
    c.id === inlineForm.value.id ? { ...c, ...inlineForm.value } : c
  );
  inlineEdit.value = null;
}
</script>

<template>
  <div class="p-4 md:p-10">
    <div class="mb-8">
      <h1 class="text-3xl font-light">مشتریان <span class="text-maroon">.</span></h1>
      <p class="mt-2 text-sm text-muted-foreground">اطلاعات و سابقه‌ی خرید مشتریان</p>
    </div>

    <!-- Stats -->
    <div class="mb-8 grid grid-cols-3 gap-px bg-border">
      <div class="bg-background p-4 md:p-6">
        <div class="text-xs uppercase tracking-widest text-muted-foreground">تعداد مشتریان</div>
        <div class="mt-2 text-2xl font-light">{{ list.length }}</div>
      </div>
      <div class="bg-background p-4 md:p-6">
        <div class="text-xs uppercase tracking-widest text-muted-foreground">مجموع سفارش‌ها</div>
        <div class="mt-2 text-2xl font-light">{{ totalOrdersAll }}</div>
      </div>
      <div class="bg-background p-4 md:p-6">
        <div class="text-xs uppercase tracking-widest text-muted-foreground">مجموع فروش</div>
        <div class="mt-2 text-2xl font-light text-maroon">{{ formatPrice(totalSpentAll) }}</div>
      </div>
    </div>

    <!-- Search -->
    <div class="relative mb-6">
      <Search class="absolute right-4 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
      <input
        v-model="search"
        placeholder="جستجو بر اساس نام، ایمیل، شهر..."
        class="w-full border border-border bg-background py-3 pr-12 pl-4 text-sm placeholder:text-muted-foreground focus:border-maroon focus:outline-none"
      />
    </div>

    <!-- MOBILE: Card list -->
    <div class="md:hidden space-y-3">
      <div
        v-for="c in filtered"
        :key="c.id"
        :class="['border border-border', inlineEdit === c.id ? 'border-maroon/30' : '']"
      >
        <div class="flex items-start gap-3 p-3">
          <div class="flex-1 min-w-0">
            <div class="font-medium text-sm">{{ c.name }}</div>
            <div class="mt-0.5 text-xs text-muted-foreground truncate">{{ c.email }}</div>
            <div class="mt-1.5 flex items-center gap-3 flex-wrap">
              <span class="flex items-center gap-1 text-xs text-muted-foreground">
                <MapPin class="h-3 w-3" />{{ c.city }}
              </span>
              <span class="text-xs text-maroon font-medium">{{ formatPrice(c.totalSpent) }}</span>
              <span class="text-xs text-muted-foreground">{{ c.totalOrders }} سفارش</span>
            </div>
          </div>
          <button
            @click="openInline(c)"
            :class="['p-2 hover:bg-accent shrink-0 transition-colors', inlineEdit === c.id ? 'text-maroon' : 'text-muted-foreground hover:text-maroon']"
          >
            <X v-if="inlineEdit === c.id" class="h-4 w-4" />
            <Pencil v-else class="h-4 w-4" />
          </button>
        </div>

        <!-- Mobile inline edit -->
        <div v-if="inlineEdit === c.id" class="border-t border-maroon/20 bg-maroon/5 p-3 space-y-3">
          <div class="grid grid-cols-2 gap-2">
            <label class="block">
              <span class="text-xs text-muted-foreground uppercase tracking-wider">نام</span>
              <input v-model="inlineForm.name" class="mt-1 w-full border border-border bg-background px-2 py-1.5 text-sm outline-none focus:border-maroon" />
            </label>
            <label class="block">
              <span class="text-xs text-muted-foreground uppercase tracking-wider">شهر</span>
              <input v-model="inlineForm.city" class="mt-1 w-full border border-border bg-background px-2 py-1.5 text-sm outline-none focus:border-maroon" />
            </label>
          </div>
          <label class="block">
            <span class="text-xs text-muted-foreground uppercase tracking-wider">ایمیل</span>
            <input v-model="inlineForm.email" dir="ltr" class="mt-1 w-full border border-border bg-background px-2 py-1.5 text-sm outline-none focus:border-maroon" />
          </label>
          <label class="block">
            <span class="text-xs text-muted-foreground uppercase tracking-wider">شماره تماس</span>
            <input v-model="inlineForm.phone" dir="ltr" class="mt-1 w-full border border-border bg-background px-2 py-1.5 text-sm outline-none focus:border-maroon" />
          </label>
          <div class="grid grid-cols-2 gap-2">
            <label class="block">
              <span class="text-xs text-muted-foreground uppercase tracking-wider">تعداد سفارش</span>
              <input type="number" v-model.number="inlineForm.totalOrders" class="mt-1 w-full border border-border bg-background px-2 py-1.5 text-sm outline-none focus:border-maroon" />
            </label>
            <label class="block">
              <span class="text-xs text-muted-foreground uppercase tracking-wider">مجموع خرید</span>
              <input type="number" v-model.number="inlineForm.totalSpent" class="mt-1 w-full border border-border bg-background px-2 py-1.5 text-sm outline-none focus:border-maroon" />
            </label>
          </div>
          <div class="flex gap-2 justify-end">
            <button @click="inlineEdit = null" class="border border-border px-4 py-1.5 text-xs hover:bg-accent">انصراف</button>
            <button @click="saveInline" class="bg-maroon px-5 py-1.5 text-xs text-maroon-foreground hover:opacity-90 flex items-center gap-1.5">
              <Check class="h-3 w-3" /> ذخیره
            </button>
          </div>
        </div>
      </div>
      <div v-if="filtered.length === 0" class="border border-dashed border-border p-12 text-center text-sm text-muted-foreground">مشتری‌ای پیدا نشد</div>
    </div>

    <!-- DESKTOP: Table + Detail panel -->
    <div class="hidden md:flex gap-6">
      <div :class="['flex-1 border border-border transition-all', selected ? 'lg:flex-none lg:w-[55%]' : '']">
        <table class="w-full text-sm">
          <thead class="bg-muted text-xs uppercase tracking-widest text-muted-foreground">
            <tr>
              <th class="px-5 py-4 text-right">مشتری</th>
              <th class="hidden px-5 py-4 text-right md:table-cell">شهر</th>
              <th class="hidden px-5 py-4 text-right lg:table-cell">سفارش‌ها</th>
              <th class="px-5 py-4 text-right">مجموع خرید</th>
              <th class="hidden px-5 py-4 text-right md:table-cell">آخرین سفارش</th>
              <th class="px-5 py-4"></th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <template v-for="c in filtered" :key="c.id">
              <tr
                @click="toggleSelect(c)"
                :class="[
                  'cursor-pointer transition-colors',
                  selected?.id === c.id ? 'bg-maroon/5' : inlineEdit === c.id ? 'bg-maroon/5' : 'hover:bg-accent/40',
                ]"
              >
                <td class="px-5 py-3">
                  <div class="font-medium">{{ c.name }}</div>
                  <div class="mt-0.5 text-xs text-muted-foreground">{{ c.email }}</div>
                </td>
                <td class="hidden px-5 py-3 text-muted-foreground md:table-cell">{{ c.city }}</td>
                <td class="hidden px-5 py-3 lg:table-cell">{{ c.totalOrders }}</td>
                <td class="px-5 py-3 text-maroon font-medium">{{ formatPrice(c.totalSpent) }}</td>
                <td class="hidden px-5 py-3 text-muted-foreground md:table-cell">{{ c.lastOrder }}</td>
                <td class="px-5 py-3" @click.stop>
                  <button
                    @click="openInline(c)"
                    :class="['p-1.5 hover:bg-accent transition-colors', inlineEdit === c.id ? 'text-maroon' : 'text-muted-foreground hover:text-maroon']"
                    title="ویرایش سریع"
                  >
                    <X v-if="inlineEdit === c.id" class="h-3.5 w-3.5" />
                    <Pencil v-else class="h-3.5 w-3.5" />
                  </button>
                </td>
              </tr>

              <!-- Inline edit row -->
              <tr v-if="inlineEdit === c.id" class="bg-maroon/5 border-b border-maroon/20">
                <td colspan="6" class="px-5 py-4">
                  <div class="flex flex-wrap items-end gap-4">
                    <label class="block">
                      <span class="text-xs text-muted-foreground uppercase tracking-wider block mb-1">نام</span>
                      <input v-model="inlineForm.name" class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon w-36" />
                    </label>
                    <label class="block">
                      <span class="text-xs text-muted-foreground uppercase tracking-wider block mb-1">ایمیل</span>
                      <input v-model="inlineForm.email" dir="ltr" class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon w-48" />
                    </label>
                    <label class="block">
                      <span class="text-xs text-muted-foreground uppercase tracking-wider block mb-1">شماره تماس</span>
                      <input v-model="inlineForm.phone" dir="ltr" class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon w-36" />
                    </label>
                    <label class="block">
                      <span class="text-xs text-muted-foreground uppercase tracking-wider block mb-1">شهر</span>
                      <input v-model="inlineForm.city" class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon w-28" />
                    </label>
                    <label class="block">
                      <span class="text-xs text-muted-foreground uppercase tracking-wider block mb-1">تعداد سفارش</span>
                      <input type="number" v-model.number="inlineForm.totalOrders" class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon w-24" />
                    </label>
                    <label class="block">
                      <span class="text-xs text-muted-foreground uppercase tracking-wider block mb-1">مجموع خرید</span>
                      <input type="number" v-model.number="inlineForm.totalSpent" class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon w-32" />
                    </label>
                    <div class="flex items-end gap-2 mr-auto">
                      <button @click="inlineEdit = null" class="border border-border px-4 py-2 text-xs hover:bg-accent">انصراف</button>
                      <button @click="saveInline" class="bg-maroon px-5 py-2 text-xs text-maroon-foreground hover:opacity-90 flex items-center gap-1.5">
                        <Check class="h-3.5 w-3.5" /> ذخیره
                      </button>
                    </div>
                  </div>
                </td>
              </tr>
            </template>

            <tr v-if="filtered.length === 0">
              <td colspan="6" class="px-5 py-10 text-center text-muted-foreground">
                مشتری‌ای با این مشخصات پیدا نشد.
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Detail Panel -->
      <div v-if="selected" class="hidden w-[40%] border border-border bg-background lg:block">
        <div class="flex items-center justify-between border-b border-border px-6 py-4">
          <div class="text-sm font-medium">{{ selected.name }}</div>
          <button @click="selected = null" class="text-muted-foreground hover:text-foreground">
            <X class="h-4 w-4" />
          </button>
        </div>

        <div class="p-6 space-y-6">
          <div>
            <div class="mb-3 text-xs uppercase tracking-widest text-maroon">اطلاعات تماس</div>
            <div class="space-y-3">
              <div class="flex items-center gap-3 text-sm">
                <Mail class="h-4 w-4 shrink-0 text-muted-foreground" />
                <span class="text-muted-foreground">{{ selected.email }}</span>
              </div>
              <div class="flex items-center gap-3 text-sm">
                <Phone class="h-4 w-4 shrink-0 text-muted-foreground" />
                <span class="text-muted-foreground">{{ selected.phone }}</span>
              </div>
            </div>
          </div>

          <div class="border-t border-border pt-6">
            <div class="mb-3 text-xs uppercase tracking-widest text-maroon">آدرس</div>
            <div class="flex items-start gap-3 text-sm">
              <MapPin class="mt-0.5 h-4 w-4 shrink-0 text-muted-foreground" />
              <div class="text-muted-foreground leading-6">
                <div class="font-medium text-foreground mb-1">{{ selected.city }}</div>
                <div>{{ selected.address }}</div>
                <div class="mt-1 text-xs">کد پستی: {{ selected.postalCode }}</div>
              </div>
            </div>
          </div>

          <div class="border-t border-border pt-6">
            <div class="mb-3 text-xs uppercase tracking-widest text-maroon">سابقه‌ی خرید</div>
            <div class="grid grid-cols-2 gap-px bg-border">
              <div class="bg-background p-4 text-center">
                <div class="text-xs text-muted-foreground mb-1">تعداد سفارش</div>
                <div class="flex items-center justify-center gap-1.5">
                  <ShoppingBag class="h-3.5 w-3.5 text-maroon" />
                  <span class="text-xl font-light">{{ selected.totalOrders }}</span>
                </div>
              </div>
              <div class="bg-background p-4 text-center">
                <div class="text-xs text-muted-foreground mb-1">مجموع خرید</div>
                <div class="text-sm font-medium text-maroon">{{ formatPrice(selected.totalSpent) }}</div>
              </div>
            </div>
          </div>

          <div class="border-t border-border pt-6 space-y-3 text-sm">
            <div class="flex items-center justify-between">
              <span class="text-muted-foreground">تاریخ عضویت</span>
              <span>{{ selected.joinDate }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-muted-foreground">آخرین سفارش</span>
              <span class="text-maroon">{{ selected.lastOrder }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
