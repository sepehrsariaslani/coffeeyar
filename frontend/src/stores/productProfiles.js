import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/lib/api'
import { isDemoMode } from '@/lib/demo.js'

const PROFILES_KEY = 'navar_product_profiles'
const ASSIGNMENTS_KEY = 'navar_product_assignments'

function uid() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 6)
}

const DEFAULT_PROFILES = [
  {
    id: 'taste-coffee',
    name: 'پروفایل طعم قهوه',
    traits: [
      { id: 'aroma', name: 'عطر' },
      { id: 'acidity', name: 'اسیدیته' },
      { id: 'bitterness', name: 'تلخی' },
    ],
  },
  {
    id: 'accessory-profile',
    name: 'پروفایل اکسسوری',
    traits: [
      { id: 'design', name: 'دیزاین' },
      { id: 'durability', name: 'مقاومت' },
      { id: 'ergonomics', name: 'ارگونومی' },
      { id: 'value', name: 'ارزش خرید' },
    ],
  },
]

const DEFAULT_ASSIGNMENTS = {
  'ethiopia-yirgacheffe': { profileId: 'taste-coffee', ratings: { aroma: 9, acidity: 8, bitterness: 3 } },
  'colombia-huila':       { profileId: 'taste-coffee', ratings: { aroma: 8, acidity: 7, bitterness: 5 } },
  'kenya-aa':             { profileId: 'taste-coffee', ratings: { aroma: 9, acidity: 9, bitterness: 4 } },
}

export const useProductProfilesStore = defineStore('productProfiles', () => {
  const profiles = ref([])
  const assignments = ref({})
  const loading = ref(false)

  async function fetchProfiles() {
    loading.value = true
    if (isDemoMode) {
      profiles.value = JSON.parse(localStorage.getItem(PROFILES_KEY) ?? 'null') ?? DEFAULT_PROFILES
      assignments.value = JSON.parse(localStorage.getItem(ASSIGNMENTS_KEY) ?? 'null') ?? DEFAULT_ASSIGNMENTS
      loading.value = false
      return
    }
    try {
      const data = await api.admin.profiles.get()
      if (data && data.profiles && data.profiles.length > 0) {
        profiles.value = data.profiles
        assignments.value = data.assignments || {}
        localStorage.setItem(PROFILES_KEY, JSON.stringify(data.profiles))
        localStorage.setItem(ASSIGNMENTS_KEY, JSON.stringify(data.assignments || {}))
      } else {
        throw new Error('empty')
      }
    } catch {
      profiles.value = JSON.parse(localStorage.getItem(PROFILES_KEY) ?? 'null') ?? DEFAULT_PROFILES
      assignments.value = JSON.parse(localStorage.getItem(ASSIGNMENTS_KEY) ?? 'null') ?? DEFAULT_ASSIGNMENTS
    }
    loading.value = false
  }

  async function saveToServer() {
    if (isDemoMode) return
    try {
      await api.admin.profiles.update({
        profiles: profiles.value,
        assignments: assignments.value,
      })
    } catch {
      // silent
    }
  }

  function _save() {
    localStorage.setItem(PROFILES_KEY, JSON.stringify(profiles.value))
    localStorage.setItem(ASSIGNMENTS_KEY, JSON.stringify(assignments.value))
    saveToServer()
  }

  function getProfile(id) {
    return profiles.value.find(p => p.id === id) ?? null
  }

  function createProfile(name, traitNames) {
    const profile = {
      id: uid(),
      name,
      traits: traitNames.map(n => ({ id: uid(), name: n })),
    }
    profiles.value.push(profile)
    _save()
    return profile
  }

  function updateProfile(id, name, traits) {
    const p = profiles.value.find(p => p.id === id)
    if (!p) return
    p.name = name
    p.traits = traits
    _save()
  }

  function deleteProfile(id) {
    profiles.value = profiles.value.filter(p => p.id !== id)
    for (const pid in assignments.value) {
      if (assignments.value[pid].profileId === id) delete assignments.value[pid]
    }
    _save()
  }

  function getAssignment(productId) {
    return assignments.value[productId] ?? null
  }

  function setAssignment(productId, profileId, ratings) {
    assignments.value[productId] = { profileId, ratings: { ...ratings } }
    _save()
  }

  function removeAssignment(productId) {
    delete assignments.value[productId]
    _save()
  }

  fetchProfiles()

  return {
    profiles,
    assignments,
    loading,
    getProfile,
    createProfile,
    updateProfile,
    deleteProfile,
    getAssignment,
    setAssignment,
    removeAssignment,
  }
})
