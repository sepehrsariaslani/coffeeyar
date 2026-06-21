<script setup>
import { ref, computed, watch } from 'vue'
import { Plus, Trash2, Edit2, Check, X, BarChart2 } from 'lucide-vue-next'
import { useProductProfilesStore } from '@/stores/productProfiles.js'
import { useProductsStore } from '@/stores/products.js'
import ProfileChart from '@/components/site/ProfileChart.vue'
import AppSelect from '@/components/AppSelect.vue'
import { toFa } from '@/lib/utils.js'

const store = useProductProfilesStore()
const productsStore = useProductsStore()

const products = computed(() => productsStore.products.map(p => ({ id: p.id, name: p.title || p.name, slug: p.slug })))

onMounted(async () => {
  await productsStore.fetchProducts({ page_size: 100 })
})

const tab = ref('profiles')

/* ───────── PROFILE TAB ───────── */
const selectedProfileId = ref(store.profiles?.[0]?.id ?? null)
const selectedProfile = computed(() => store.profiles.find(p => p.id === selectedProfileId.value) ?? null)

const editName = ref('')
const editTraits = ref([])
const editMode = ref(false)

function selectProfile(id) {
  selectedProfileId.value = id
  cancelEdit()
}

function startEdit() {
  if (!selectedProfile.value) return
  editName.value = selectedProfile.value.name
  editTraits.value = selectedProfile.value.traits.map(t => ({ ...t }))
  editMode.value = true
}

function cancelEdit() {
  editMode.value = false
  editName.value = ''
  editTraits.value = []
}

function saveEdit() {
  if (!editName.value.trim()) return
  const validTraits = editTraits.value.filter(t => t.name.trim())
  store.updateProfile(selectedProfileId.value, editName.value.trim(), validTraits)
  cancelEdit()
}

function addEditTrait() {
  editTraits.value.push({ id: Date.now().toString(36), name: '' })
}

function removeEditTrait(idx) {
  editTraits.value.splice(idx, 1)
}

/* new profile */
const showNewForm = ref(false)
const newName = ref('')
const newTraits = ref(['', '', ''])

function addNewTrait() { newTraits.value.push('') }
function removeNewTrait(i) { if (newTraits.value.length > 2) newTraits.value.splice(i, 1) }

function createProfile() {
  const name = newName.value.trim()
  const traits = newTraits.value.map(t => t.trim()).filter(Boolean)
  if (!name || traits.length < 2) return
  const p = store.createProfile(name, traits)
  selectedProfileId.value = p.id
  newName.value = ''
  newTraits.value = ['', '', '']
  showNewForm.value = false
}

function deleteProfile(id) {
  const remaining = store.profiles.filter(p => p.id !== id)
  store.deleteProfile(id)
  selectedProfileId.value = remaining[0]?.id ?? null
}

/* ───────── ASSIGN TAB ───────── */
const selectedProductId = ref(null)
const assignProfileId = ref(null)
const assignRatings = ref({})

const assignProduct = computed(() => products.find(p => p.id === selectedProductId.value) ?? null)
const assignProfile = computed(() => store.getProfile(assignProfileId.value) ?? null)

watch(selectedProductId, (pid) => {
  if (!pid) { assignProfileId.value = null; assignRatings.value = {}; return }
  const a = store.getAssignment(pid)
  if (a) {
    assignProfileId.value = a.profileId
    assignRatings.value = { ...a.ratings }
  } else {
    assignProfileId.value = null
    assignRatings.value = {}
  }
})

watch(assignProfileId, (pid) => {
  if (!pid) { assignRatings.value = {}; return }
  const profile = store.getProfile(pid)
  if (!profile) return
  const existing = assignRatings.value
  const fresh = {}
  profile.traits.forEach(t => { fresh[t.id] = existing[t.id] ?? 5 })
  assignRatings.value = fresh
})

function saveAssignment() {
  if (!selectedProductId.value || !assignProfileId.value) return
  store.setAssignment(selectedProductId.value, assignProfileId.value, assignRatings.value)
  saved.value = true
  setTimeout(() => { saved.value = false }, 1800)
}

function removeAssignment() {
  if (!selectedProductId.value) return
  store.removeAssignment(selectedProductId.value)
  assignProfileId.value = null
  assignRatings.value = {}
}

const saved = ref(false)
</script>

<template>
  <div class="p-6 md:p-10 max-w-6xl mx-auto" dir="rtl">
    <div class="mb-8">
      <h1 class="text-2xl font-light">پروفایل‌های محصول</h1>
      <p class="mt-1 text-sm text-muted-foreground">قالب‌های ویژگی سفارشی تعریف کنید و به محصولات اختصاص دهید.</p>
    </div>

    <!-- Tabs -->
    <div class="flex border-b border-border mb-8 gap-6">
      <button
        v-for="t in [{ id:'profiles', label:'قالب‌ها' }, { id:'assign', label:'تخصیص به محصولات' }]"
        :key="t.id"
        @click="tab = t.id"
        :class="['pb-3 text-sm transition-colors border-b-2 -mb-px',
          tab === t.id ? 'border-maroon text-foreground font-medium' : 'border-transparent text-muted-foreground hover:text-foreground']"
      >{{ t.label }}</button>
    </div>

    <!-- ═══ PROFILES TAB ═══ -->
    <div v-if="tab === 'profiles'" class="grid md:grid-cols-[280px_1fr] gap-6">

      <!-- Left: profile list -->
      <div>
        <div class="border border-border divide-y divide-border">
          <button
            v-for="p in store.profiles"
            :key="p.id"
            @click="selectProfile(p.id)"
            :class="['w-full flex items-center justify-between px-4 py-3 text-sm text-right transition-colors',
              selectedProfileId === p.id ? 'bg-foreground text-background' : 'hover:bg-accent']"
          >
            <span>{{ p.name }}</span>
            <span :class="['text-xs', selectedProfileId === p.id ? 'text-background/60' : 'text-muted-foreground']">
              {{ toFa(p.traits.length) }} ویژگی
            </span>
          </button>
        </div>

        <button
          @click="showNewForm = !showNewForm; cancelEdit()"
          class="mt-3 w-full flex items-center justify-center gap-2 border border-dashed border-border py-2.5 text-sm text-muted-foreground hover:text-foreground hover:border-foreground/30 transition-colors"
        >
          <Plus class="h-4 w-4" /> قالب جدید
        </button>

        <!-- New profile form -->
        <div v-if="showNewForm" class="mt-4 border border-border p-4 space-y-3">
          <p class="text-xs font-medium text-muted-foreground uppercase tracking-wider">قالب جدید</p>
          <input
            v-model="newName"
            placeholder="نام قالب (مثلاً: پروفایل طعم)"
            class="w-full border border-border px-3 py-2 text-sm bg-background focus:outline-none focus:border-foreground"
          />
          <div class="space-y-2">
            <div v-for="(_, i) in newTraits" :key="i" class="flex gap-2">
              <input
                v-model="newTraits[i]"
                :placeholder="`ویژگی ${toFa(i + 1)}`"
                class="flex-1 border border-border px-3 py-1.5 text-sm bg-background focus:outline-none focus:border-foreground"
              />
              <button
                @click="removeNewTrait(i)"
                :disabled="newTraits.length <= 2"
                class="p-1.5 text-muted-foreground hover:text-red-600 disabled:opacity-30"
              ><Trash2 class="h-3.5 w-3.5" /></button>
            </div>
          </div>
          <div class="flex gap-2">
            <button @click="addNewTrait" class="text-xs text-muted-foreground hover:text-foreground flex items-center gap-1">
              <Plus class="h-3 w-3" /> افزودن ویژگی
            </button>
            <span class="flex-1" />
            <button @click="showNewForm = false" class="text-xs text-muted-foreground hover:text-foreground px-3 py-1.5 border border-border">
              انصراف
            </button>
            <button
              @click="createProfile"
              :disabled="!newName.trim() || newTraits.filter(t=>t.trim()).length < 2"
              class="text-xs px-3 py-1.5 bg-foreground text-background hover:opacity-80 disabled:opacity-30"
            >
              ساخت
            </button>
          </div>
        </div>
      </div>

      <!-- Right: selected profile detail / edit -->
      <div v-if="selectedProfile">
        <div class="border border-border p-6">
          <div class="flex items-start justify-between mb-6">
            <div v-if="!editMode">
              <h2 class="text-xl font-light">{{ selectedProfile.name }}</h2>
              <p class="text-sm text-muted-foreground mt-1">
                {{ toFa(selectedProfile.traits.length) }} ویژگی — شکل چندضلعی:
                <span class="text-maroon">
                  {{ selectedProfile.traits.length === 3 ? 'مثلث' : selectedProfile.traits.length === 4 ? 'مربع' : selectedProfile.traits.length === 5 ? 'پنج‌ضلعی' : selectedProfile.traits.length === 6 ? 'شش‌ضلعی' : `${toFa(selectedProfile.traits.length)}-ضلعی` }}
                </span>
              </p>
            </div>
            <div v-else class="flex-1 ml-4">
              <input
                v-model="editName"
                class="w-full text-xl font-light border-b border-border bg-transparent focus:outline-none focus:border-maroon pb-1"
              />
            </div>

            <div class="flex gap-2 shrink-0">
              <template v-if="!editMode">
                <button @click="startEdit" class="p-2 text-muted-foreground hover:text-foreground border border-border">
                  <Edit2 class="h-4 w-4" />
                </button>
                <button @click="deleteProfile(selectedProfile.id)" class="p-2 text-muted-foreground hover:text-red-600 border border-border">
                  <Trash2 class="h-4 w-4" />
                </button>
              </template>
              <template v-else>
                <button @click="saveEdit" class="p-2 text-green-700 border border-green-200 hover:bg-green-50">
                  <Check class="h-4 w-4" />
                </button>
                <button @click="cancelEdit" class="p-2 text-muted-foreground border border-border hover:bg-accent">
                  <X class="h-4 w-4" />
                </button>
              </template>
            </div>
          </div>

          <!-- Traits list / edit -->
          <div v-if="!editMode" class="space-y-2">
            <div
              v-for="(t, i) in selectedProfile.traits"
              :key="t.id"
              class="flex items-center gap-3 px-3 py-2 bg-accent/40"
            >
              <span class="text-xs text-muted-foreground w-5 text-center">{{ toFa(i + 1) }}</span>
              <span class="text-sm">{{ t.name }}</span>
            </div>
          </div>
          <div v-else class="space-y-2">
            <div v-for="(t, i) in editTraits" :key="t.id" class="flex gap-2 items-center">
              <span class="text-xs text-muted-foreground w-5 text-center">{{ toFa(i + 1) }}</span>
              <input
                v-model="editTraits[i].name"
                class="flex-1 border border-border px-3 py-1.5 text-sm bg-background focus:outline-none focus:border-foreground"
                :placeholder="`ویژگی ${toFa(i + 1)}`"
              />
              <button
                @click="removeEditTrait(i)"
                :disabled="editTraits.length <= 2"
                class="p-1.5 text-muted-foreground hover:text-red-600 disabled:opacity-30"
              ><Trash2 class="h-3.5 w-3.5" /></button>
            </div>
            <button @click="addEditTrait" class="mt-2 text-xs text-muted-foreground hover:text-foreground flex items-center gap-1">
              <Plus class="h-3 w-3" /> افزودن ویژگی
            </button>
          </div>

          <!-- Chart preview -->
          <div v-if="!editMode" class="mt-8 border-t border-border pt-6">
            <p class="text-xs uppercase tracking-widest text-muted-foreground mb-4">پیش‌نمایش شکل</p>
            <ProfileChart
              :traits="selectedProfile.traits"
              :ratings="Object.fromEntries(selectedProfile.traits.map(t => [t.id, 7]))"
            />
            <p class="text-center text-xs text-muted-foreground mt-2">مقادیر نمونه (۷/۱۰)</p>
          </div>
        </div>
      </div>
      <div v-else class="border border-dashed border-border p-10 text-center text-sm text-muted-foreground">
        یک قالب را از سمت راست انتخاب کنید یا قالب جدید بسازید.
      </div>
    </div>

    <!-- ═══ ASSIGN TAB ═══ -->
    <div v-if="tab === 'assign'" class="grid md:grid-cols-2 gap-8">
      <div class="space-y-6">
        <!-- Product selector -->
        <div>
          <label class="block text-xs font-medium uppercase tracking-widest text-muted-foreground mb-2">محصول</label>
          <AppSelect
            v-model="selectedProductId"
            :options="products.map(p => ({ label: p.name, value: p.id }))"
            placeholder="انتخاب محصول…"
          />
        </div>

        <!-- Profile selector -->
        <div v-if="selectedProductId">
          <label class="block text-xs font-medium uppercase tracking-widest text-muted-foreground mb-2">پروفایل</label>
          <AppSelect
            v-model="assignProfileId"
            :options="store.profiles.map(p => ({ label: p.name, value: p.id }))"
            placeholder="انتخاب پروفایل…"
          />

          <button
            v-if="store.getAssignment(selectedProductId)"
            @click="removeAssignment"
            class="mt-2 text-xs text-muted-foreground hover:text-red-600 flex items-center gap-1"
          >
            <Trash2 class="h-3 w-3" /> حذف تخصیص فعلی
          </button>
        </div>

        <!-- Trait sliders -->
        <div v-if="assignProfile && selectedProductId" class="space-y-4">
          <p class="text-xs font-medium uppercase tracking-widest text-muted-foreground">امتیاز ویژگی‌ها</p>
          <div v-for="t in assignProfile.traits" :key="t.id" class="space-y-1">
            <div class="flex justify-between text-sm">
              <span>{{ t.name }}</span>
              <span class="text-maroon font-medium">{{ toFa(assignRatings[t.id] ?? 0) }} / ۱۰</span>
            </div>
            <input
              type="range"
              min="0" max="10" step="0.5"
              v-model.number="assignRatings[t.id]"
              class="w-full accent-maroon h-1.5"
            />
            <div class="flex justify-between text-[10px] text-muted-foreground">
              <span>۰</span><span>۵</span><span>۱۰</span>
            </div>
          </div>
        </div>

        <!-- Save -->
        <div v-if="assignProfile && selectedProductId" class="flex gap-3 pt-2">
          <button
            @click="saveAssignment"
            class="flex-1 bg-foreground text-background text-sm py-2.5 hover:opacity-80 transition-opacity"
          >
            {{ saved ? '✓ ذخیره شد' : 'ذخیره' }}
          </button>
        </div>
      </div>

      <!-- Chart preview -->
      <div class="flex flex-col items-center justify-center">
        <div v-if="assignProfile && Object.keys(assignRatings).length" class="w-full">
          <p class="text-xs uppercase tracking-widest text-muted-foreground mb-2 text-center">پیش‌نمایش زنده</p>
          <div class="border border-border p-6 bg-[#FAFAF8] flex flex-col items-center">
            <p class="text-sm font-medium mb-1">{{ assignProduct?.name }}</p>
            <p class="text-xs text-muted-foreground mb-4">{{ assignProfile.name }}</p>
            <ProfileChart :traits="assignProfile.traits" :ratings="assignRatings" />
            <div class="mt-4 grid gap-3 w-full" :style="`grid-template-columns: repeat(${Math.min(assignProfile.traits.length, 3)}, 1fr)`">
              <div v-for="t in assignProfile.traits" :key="t.id" class="border-t-2 border-maroon pt-2 text-center">
                <div class="text-[10px] text-muted-foreground">{{ t.name }}</div>
                <div class="text-lg font-light text-maroon">{{ toFa(assignRatings[t.id] ?? 0) }}<span class="text-xs text-muted-foreground">/۱۰</span></div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="border border-dashed border-border p-12 text-center text-sm text-muted-foreground w-full">
          <BarChart2 class="h-8 w-8 mx-auto mb-3 text-border" />
          محصول و پروفایل را انتخاب کنید تا نمودار نمایش داده شود.
        </div>
      </div>
    </div>
  </div>
</template>
