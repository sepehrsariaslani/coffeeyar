<script setup>
import { computed } from "vue";
import { RouterLink } from "vue-router";
import { Minus, Plus, Trash2, ShoppingBag, ArrowLeft } from "lucide-vue-next";
import TheLayout from "@/components/site/TheLayout.vue";
import { useCartStore } from "@/stores/cart.js";
import { formatPrice } from "@/lib/data.js";
import { toFa } from "@/lib/utils.js";

const cartStore = useCartStore();

const subtotal = computed(() => cartStore.total);
const shipping = computed(() =>
  subtotal.value > 500000 || subtotal.value === 0 ? 0 : 45000
);
const total = computed(() => subtotal.value + shipping.value);
</script>

<template>
  <TheLayout>
    <!-- Empty state -->
    <section v-if="cartStore.items.length === 0" class="mx-auto max-w-2xl px-6 py-32 text-center">
      <ShoppingBag class="mx-auto h-10 w-10 text-maroon" />
      <h1 class="mt-6 text-3xl font-light">سبد خرید خالی است</h1>
      <p class="mt-3 text-sm text-muted-foreground">هنوز چیزی به سبد اضافه نکرده‌اید.</p>
      <RouterLink
        to="/products"
        class="mt-8 inline-flex items-center gap-2 bg-foreground px-6 py-3 text-sm text-background hover:bg-maroon"
      >
        دیدن محصولات <ArrowLeft class="h-4 w-4" />
      </RouterLink>
    </section>

    <template v-else>
      <section class="border-b border-border">
        <div class="mx-auto max-w-7xl px-6 py-14">
          <span class="text-xs uppercase tracking-[0.3em] text-maroon">سبد شما</span>
          <h1 class="mt-3 text-4xl font-light">{{ toFa(cartStore.items.length) }} قلم در سبد</h1>
        </div>
      </section>

      <section class="mx-auto grid max-w-7xl gap-12 px-6 py-12 lg:grid-cols-[1.6fr_1fr]">
        <!-- Items -->
        <div class="divide-y divide-border border-y border-border">
          <div v-for="i in cartStore.items" :key="i.id" class="flex gap-5 py-6">
            <img :src="i.image" alt="" class="h-28 w-28 shrink-0 object-cover" />
            <div class="flex flex-1 flex-col">
              <div class="flex items-start justify-between gap-3">
                <div>
                  <h3 class="text-lg">{{ i.name }}</h3>
                  <div class="mt-1 text-xs text-muted-foreground">{{ i.weight }} · {{ i.grind }}</div>
                </div>
                <button
                  type="button"
                  @click="cartStore.remove(i.id)"
                  class="p-2 text-muted-foreground hover:text-maroon"
                  aria-label="حذف"
                >
                  <Trash2 class="h-4 w-4" />
                </button>
              </div>

              <div class="mt-auto flex items-end justify-between pt-3">
                <div class="flex items-center border border-border">
                  <button
                    type="button"
                    @click="cartStore.setQty(i.id, i.qty - 1)"
                    class="px-3 py-2 hover:bg-accent"
                    aria-label="کاهش"
                  >
                    <Minus class="h-3.5 w-3.5" />
                  </button>
                  <span class="w-10 text-center text-sm">{{ toFa(i.qty) }}</span>
                  <button
                    type="button"
                    @click="cartStore.setQty(i.id, i.qty + 1)"
                    class="px-3 py-2 hover:bg-accent"
                    aria-label="افزایش"
                  >
                    <Plus class="h-3.5 w-3.5" />
                  </button>
                </div>
                <div class="text-maroon">{{ formatPrice(i.unitPrice * i.qty) }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Summary -->
        <aside class="h-fit border border-maroon/30 bg-muted/40 p-8">
          <div class="text-xs uppercase tracking-widest text-maroon">خلاصه‌ی سفارش</div>
          <h2 class="mt-2 text-2xl font-light">جمع‌بندی</h2>

          <dl class="mt-6 space-y-3 border-y border-border py-5 text-sm">
            <div class="flex justify-between">
              <dt class="text-muted-foreground">جمع کالاها</dt>
              <dd>{{ formatPrice(subtotal) }}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-muted-foreground">هزینه ارسال</dt>
              <dd>{{ shipping === 0 ? "رایگان" : formatPrice(shipping) }}</dd>
            </div>
          </dl>
          <div class="mt-5 flex items-baseline justify-between">
            <span class="text-sm text-muted-foreground">مبلغ قابل پرداخت</span>
            <span class="text-2xl font-light text-maroon">{{ formatPrice(total) }}</span>
          </div>

          <RouterLink
            to="/checkout"
            class="mt-6 block bg-maroon py-3.5 text-center text-sm text-maroon-foreground transition-opacity hover:opacity-90"
          >
            ادامه و پرداخت
          </RouterLink>
          <RouterLink
            to="/products"
            class="mt-3 block text-center text-xs text-muted-foreground hover:text-maroon"
          >
            ادامه‌ی خرید
          </RouterLink>
        </aside>
      </section>
    </template>
  </TheLayout>
</template>
