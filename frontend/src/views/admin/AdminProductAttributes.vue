<script setup>
import { ref, computed, onMounted } from "vue";
import { api } from "@/lib/api.js";
import { Plus, Trash2, Save, Image, Check, X } from "lucide-vue-next";

const products = ref([]);
const attributes = ref([]);
const selectedProduct = ref(null);
const newAttrName = ref("");
const newAttrValues = ref("");
const loading = ref(false);
const message = ref("");
const messageType = ref("success");
const uploadingImage = ref(false);

async function loadProducts() {
  try {
    const res = await api.admin.products.list();
    products.value = res.map(p => {
      let attrs = [];
      if (p.attributes_json) {
        try { attrs = JSON.parse(p.attributes_json); } catch {}
      }
      return {
        id: p.name || p.id,
        name: p.title || p.name,
        slug: p.slug,
        image: p.image,
        price: p.price_toman,
        discount: p.discount_toman,
        stockCount: p.stock_qty,
        isPublished: p.is_published,
        isFeatured: p.is_featured,
        attributes: attrs,
      };
    });
  } catch (e) {
    showMessage("خطا در دریافت محصولات: " + e.message, "error");
  }
}

async function loadAttributes() {
  try {
    const res = await api.admin.attributes.list();
    attributes.value = res.map(a => ({
      id: a.name || a.id,
      name: a.title || a.name,
      slug: a.slug,
      values: a.options || a.values || [],
    }));
  } catch (e) {
    // Attributes API might not exist yet, ignore
    attributes.value = [];
  }
}

function showMessage(msg, type = "success") {
  message.value = msg;
  messageType.value = type;
  setTimeout(() => { message.value = ""; }, 3000);
}

function selectProduct(product) {
  selectedProduct.value = { ...product };
}

async function saveProduct() {
  if (!selectedProduct.value) return;
  loading.value = true;
  try {
    const attributesJson = JSON.stringify(selectedProduct.value.attributes || []);
    await api.admin.products.update(selectedProduct.value.id, {
      item_name: selectedProduct.value.name,
      slug: selectedProduct.value.slug,
      image: selectedProduct.value.image,
      short_description: selectedProduct.value.shortDescription || "",
      description: selectedProduct.value.description || "",
      price_toman: selectedProduct.value.price || 0,
      discount_toman: selectedProduct.value.discount || 0,
      stock_qty: selectedProduct.value.stockCount || 0,
      is_published: selectedProduct.value.isPublished ? 1 : 0,
      is_featured: selectedProduct.value.isFeatured ? 1 : 0,
      attributes_json: attributesJson,
    });
    showMessage("محصول با موفقیت ذخیره شد ✓");
    await loadProducts();
  } catch (e) {
    showMessage("خطا در ذخیره: " + e.message, "error");
  } finally {
    loading.value = false;
  }
}

async function uploadImage(e) {
  const file = e.target.files[0];
  if (!file) return;
  if (!file.type.startsWith("image/")) {
    showMessage("فایل باید تصویر باشد", "error");
    return;
  }
  if (file.size > 5 * 1024 * 1024) {
    showMessage("حجم فایل بیشتر از ۵ مگابایت است", "error");
    return;
  }

  uploadingImage.value = true;
  try {
    const res = await api.uploadImage(file);
    if (selectedProduct.value) {
      selectedProduct.value.image = res.url;
    }
    showMessage("تصویر با موفقیت آپلود شد ✓");
  } catch (e) {
    // Fallback: use data URL
    const reader = new FileReader();
    reader.onload = (ev) => {
      if (selectedProduct.value) {
        selectedProduct.value.image = ev.target.result;
      }
      showMessage("تصویر به‌صورت محلی ذخیره شد (آپلود سرور ناموفق بود)", "warning");
    };
    reader.readAsDataURL(file);
  } finally {
    uploadingImage.value = false;
  }
}

function addAttribute() {
  if (!selectedProduct.value || !newAttrName.value.trim()) return;
  
  const attrName = newAttrName.value.trim();
  const values = newAttrValues.value.split(",").map(v => v.trim()).filter(Boolean);
  
  if (!selectedProduct.value.attributes) {
    selectedProduct.value.attributes = [];
  }
  
  // Check if attribute already exists
  const existing = selectedProduct.value.attributes.find(a => a.name === attrName);
  if (existing) {
    existing.values = values;
  } else {
    selectedProduct.value.attributes.push({ name: attrName, values });
  }
  
  newAttrName.value = "";
  newAttrValues.value = "";
  showMessage("ویژگی اضافه شد ✓");
}

function removeAttribute(index) {
  if (!selectedProduct.value) return;
  selectedProduct.value.attributes.splice(index, 1);
}

function addValueToAttr(attr) {
  const val = prompt("مقدار جدید:");
  if (val && val.trim()) {
    attr.values.push(val.trim());
  }
}

function removeValueFromAttr(attr, valIndex) {
  attr.values.splice(valIndex, 1);
}

onMounted(async () => {
  loading.value = true;
  await Promise.all([loadProducts(), loadAttributes()]);
  loading.value = false;
});
</script>

<template>
  <div class="p-4 md:p-10">
    <div class="mb-8">
      <h1 class="text-3xl font-light">ویژگی‌های محصولات <span class="text-maroon">.</span></h1>
      <p class="mt-2 text-sm text-muted-foreground">مدیریت ویژگی‌ها و تصاویر محصولات</p>
    </div>

    <!-- Message -->
    <div v-if="message" class="mb-6 px-4 py-3 text-sm" :class="{
      'bg-green-50 text-green-700 border border-green-200': messageType === 'success',
      'bg-red-50 text-red-700 border border-red-200': messageType === 'error',
      'bg-amber-50 text-amber-700 border border-amber-200': messageType === 'warning',
    }">
      {{ message }}
    </div>

    <!-- Loading -->
    <div v-if="loading" class="py-20 text-center text-muted-foreground">
      در حال بارگذاری...
    </div>

    <div v-else class="grid gap-6 lg:grid-cols-[1fr_1.5fr]">
      <!-- Product List -->
      <div class="border border-border">
        <div class="border-b border-border px-4 py-3">
          <h2 class="text-sm font-medium">محصولات ({{ products.length }})</h2>
        </div>
        <div class="divide-y divide-border max-h-[60vh] overflow-y-auto">
          <button
            v-for="p in products"
            :key="p.id"
            @click="selectProduct(p)"
            class="w-full text-right px-4 py-3 hover:bg-accent/30 transition-colors flex items-center gap-3"
            :class="selectedProduct?.id === p.id ? 'bg-maroon/5 border-r-2 border-maroon' : ''"
          >
            <img v-if="p.image" :src="p.image" class="h-10 w-10 object-cover shrink-0" />
            <div v-else class="h-10 w-10 bg-muted shrink-0 flex items-center justify-center text-muted-foreground">
              <Image class="h-4 w-4" />
            </div>
            <div class="flex-1 min-w-0">
              <div class="text-sm font-medium truncate">{{ p.name }}</div>
              <div class="text-xs text-muted-foreground">{{ p.attributes?.length || 0 }} ویژگی</div>
            </div>
          </button>
          <div v-if="products.length === 0" class="px-4 py-8 text-center text-sm text-muted-foreground">
            محصولی وجود ندارد
          </div>
        </div>
      </div>

      <!-- Product Editor -->
      <div class="border border-border">
        <div v-if="!selectedProduct" class="py-20 text-center text-muted-foreground">
          یک محصول را انتخاب کنید
        </div>

        <template v-else>
          <div class="border-b border-border px-4 py-3 flex items-center justify-between flex-wrap gap-2">
            <h2 class="text-sm font-medium">ویرایش محصول</h2>
            <button
              @click="saveProduct"
              :disabled="loading"
              class="inline-flex items-center gap-2 bg-maroon px-4 py-2 text-sm text-white hover:opacity-90 disabled:opacity-50"
            >
              <Save class="h-4 w-4" />
              ذخیره
            </button>
          </div>

          <div class="p-4 space-y-5">
            <!-- Image Upload -->
            <div>
              <label class="block text-xs uppercase tracking-widest text-muted-foreground mb-2">تصویر محصول</label>
              <div class="flex items-start gap-4 flex-wrap">
                <div v-if="selectedProduct.image" class="relative">
                  <img :src="selectedProduct.image" class="h-24 w-24 object-cover border border-border" />
                  <button
                    @click="selectedProduct.image = ''"
                    class="absolute -top-2 -left-2 bg-red-500 text-white p-1 rounded-full hover:bg-red-600"
                  >
                    <X class="h-3 w-3" />
                  </button>
                </div>
                <div v-else class="h-24 w-24 bg-muted/30 border border-dashed border-border flex items-center justify-center">
                  <Image class="h-6 w-6 text-muted-foreground" />
                </div>
                <label class="cursor-pointer inline-flex items-center gap-2 border border-border px-4 py-2 text-sm hover:bg-accent">
                  <input type="file" accept="image/*" class="hidden" @change="uploadImage" :disabled="uploadingImage" />
                  <Plus class="h-4 w-4" />
                  {{ uploadingImage ? "در حال آپلود..." : "آپلود تصویر" }}
                </label>
              </div>
            </div>

            <!-- Basic Info -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs uppercase tracking-widest text-muted-foreground mb-1">نام محصول</label>
                <input v-model="selectedProduct.name" class="w-full border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon" />
              </div>
              <div>
                <label class="block text-xs uppercase tracking-widest text-muted-foreground mb-1">Slug</label>
                <input v-model="selectedProduct.slug" class="w-full border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon" />
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label class="block text-xs uppercase tracking-widest text-muted-foreground mb-1">قیمت (تومان)</label>
                <input type="number" v-model.number="selectedProduct.price" class="w-full border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon" />
              </div>
              <div>
                <label class="block text-xs uppercase tracking-widest text-muted-foreground mb-1">تخفیف</label>
                <input type="number" v-model.number="selectedProduct.discount" class="w-full border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon" />
              </div>
              <div>
                <label class="block text-xs uppercase tracking-widest text-muted-foreground mb-1">موجودی</label>
                <input type="number" v-model.number="selectedProduct.stockCount" class="w-full border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon" />
              </div>
            </div>

            <!-- Attributes Section -->
            <div>
              <div class="flex items-center justify-between mb-3">
                <label class="text-xs uppercase tracking-widest text-muted-foreground">ویژگی‌ها</label>
                <span class="text-xs text-muted-foreground">{{ selectedProduct.attributes?.length || 0 }} ویژگی</span>
              </div>

              <!-- Existing attributes -->
              <div v-if="selectedProduct.attributes?.length" class="space-y-3 mb-4">
                <div v-for="(attr, idx) in selectedProduct.attributes" :key="idx" class="border border-border p-3">
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-sm font-medium">{{ attr.name }}</span>
                    <button @click="removeAttribute(idx)" class="text-red-500 hover:text-red-700">
                      <Trash2 class="h-3.5 w-3.5" />
                    </button>
                  </div>
                  <div class="flex flex-wrap gap-2">
                    <span
                      v-for="(val, vIdx) in attr.values"
                      :key="vIdx"
                      class="inline-flex items-center gap-1 border border-border px-2 py-1 text-xs"
                    >
                      {{ val }}
                      <button @click="removeValueFromAttr(attr, vIdx)" class="text-muted-foreground hover:text-red-500">
                        <X class="h-3 w-3" />
                      </button>
                    </span>
                    <button
                      @click="addValueToAttr(attr)"
                      class="inline-flex items-center gap-1 border border-dashed border-border px-2 py-1 text-xs text-muted-foreground hover:border-maroon hover:text-maroon"
                    >
                      <Plus class="h-3 w-3" />
                      مقدار جدید
                    </button>
                  </div>
                </div>
              </div>

              <!-- Add new attribute -->
              <div class="border border-dashed border-border p-3">
                <div class="grid grid-cols-1 sm:grid-cols-[1fr_1.5fr_auto] gap-2">
                  <input
                    v-model="newAttrName"
                    placeholder="نام ویژگی (مثلاً: رنگ)"
                    class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon"
                  />
                  <input
                    v-model="newAttrValues"
                    placeholder="مقادیر با کاما جدا شوند (مثلاً: قرمز, آبی, سبز)"
                    class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon"
                  />
                  <button
                    @click="addAttribute"
                    :disabled="!newAttrName.trim()"
                    class="bg-foreground text-background px-4 py-2 text-sm hover:opacity-90 disabled:opacity-50 sm:w-auto w-full"
                  >
                    <Plus class="h-4 w-4 inline" />
                    افزودن
                  </button>
                </div>
              </div>
            </div>

            <!-- Description -->
            <div>
              <label class="block text-xs uppercase tracking-widest text-muted-foreground mb-1">توضیحات</label>
              <textarea v-model="selectedProduct.description" rows="3" class="w-full border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon resize-none"></textarea>
            </div>

            <!-- Flags -->
            <div class="flex items-center gap-6">
              <label class="inline-flex items-center gap-2 text-sm cursor-pointer">
                <input type="checkbox" v-model="selectedProduct.isPublished" class="accent-maroon" />
                منتشر شده
              </label>
              <label class="inline-flex items-center gap-2 text-sm cursor-pointer">
                <input type="checkbox" v-model="selectedProduct.isFeatured" class="accent-maroon" />
                محصول ویژه
              </label>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>
