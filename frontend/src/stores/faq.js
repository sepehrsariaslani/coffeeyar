import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/lib/api.js";

export const useFaqStore = defineStore("faq", () => {
  const faqs = ref([]);
  const loaded = ref(false);
  const loading = ref(false);

  async function fetchFaqs() {
    if (loaded.value) return;
    loading.value = true;
    try {
      faqs.value = await api.faq.list();
      loaded.value = true;
    } catch (e) {
      console.error(e.message);
    } finally {
      loading.value = false;
    }
  }

  async function fetchAdminFaqs() {
    loading.value = true;
    try {
      faqs.value = await api.admin.faq.list();
    } catch (e) {
      console.error(e.message);
    } finally {
      loading.value = false;
    }
  }

  async function create(data) {
    try {
      await api.admin.faq.create(data);
      await fetchAdminFaqs();
    } catch (e) {
      console.error(e.message);
    }
  }

  async function update(id, data) {
    try {
      await api.admin.faq.update(id, data);
      await fetchAdminFaqs();
    } catch (e) {
      console.error(e.message);
    }
  }

  async function remove(id) {
    try {
      await api.admin.faq.remove(id);
      faqs.value = faqs.value.filter((f) => f.id !== id);
    } catch (e) {
      console.error(e.message);
    }
  }

  return { faqs, loaded, loading, fetchFaqs, fetchAdminFaqs, create, update, remove };
});
