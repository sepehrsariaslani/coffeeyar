import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/lib/api.js";
import { isDemoMode } from "@/lib/demo.js";
import { copyDemo, DEMO_POSTS } from "@/data/demoData.js";

export const usePostsStore = defineStore("posts", () => {
  const posts = ref([]);
  const loading = ref(false);
  const loaded = ref(false);

  async function fetchPosts() {
    if (loaded.value) return;
    loading.value = true;
    try {
      const res = isDemoMode ? { items: copyDemo(DEMO_POSTS) } : await api.blog.list(1, 100);
      posts.value = (res.items || []).map((p) => ({
        ...p,
        body: p.content,
        status: p.is_published ? "published" : "draft",
        date: p.published_on || p.created_at?.slice(0, 10) || p.date || "",
        coverImage: p.cover_image,
        readTime: p.read_time || p.readTime,
      }));
      loaded.value = true;
    } catch (e) {
      console.error("خطا در دریافت پست‌ها:", e.message);
      posts.value = copyDemo(DEMO_POSTS);
      loaded.value = true;
    } finally {
      loading.value = false;
    }
  }

  async function fetchAdminPosts() {
    loading.value = true;
    try {
      const res = await api.admin.blog.list();
      posts.value = res.map((p) => ({
        ...p,
        body: p.content,
        status: p.is_published ? "published" : "draft",
        date: p.published_on || p.created_at?.slice(0, 10) || "",
        coverImage: p.cover_image,
        readTime: p.read_time,
      }));
    } catch (e) {
      console.error(e.message);
    } finally {
      loading.value = false;
    }
  }

  async function create(data) {
    try {
      const res = await api.admin.blog.create({
        title: data.title,
        slug: data.slug || "",
        excerpt: data.excerpt || "",
        content: data.body || data.content || "",
        cover_image: data.coverImage || data.cover_image || "",
        author: data.author || "نوار",
        category: data.category || "عمومی",
        read_time: data.readTime || data.read_time || "۵ دقیقه",
        is_published: data.status === "published" || !!data.is_published,
      });
      loaded.value = false;
      await fetchAdminPosts();
      return res;
    } catch (e) {
      console.error(e.message);
    }
  }

  async function update(idOrSlug, data) {
    const post = posts.value.find((p) => p.id === idOrSlug || p.slug === idOrSlug);
    if (!post) return;
    try {
      await api.admin.blog.update(post.id, {
        title: data.title ?? post.title,
        slug: data.slug ?? post.slug,
        excerpt: data.excerpt ?? post.excerpt,
        content: data.body ?? data.content ?? post.body,
        cover_image: data.coverImage ?? data.cover_image ?? post.cover_image,
        author: data.author ?? post.author,
        category: data.category ?? post.category,
        read_time: data.readTime ?? data.read_time ?? post.read_time,
        is_published: data.status === "published" || data.is_published || post.is_published,
      });
      loaded.value = false;
      await fetchAdminPosts();
    } catch (e) {
      console.error(e.message);
    }
  }

  async function remove(idOrSlug) {
    const post = posts.value.find((p) => p.id === idOrSlug || p.slug === idOrSlug);
    if (!post) return;
    try {
      await api.admin.blog.remove(post.id);
      posts.value = posts.value.filter((p) => p.id !== post.id);
    } catch (e) {
      console.error(e.message);
    }
  }

  function getPublished() {
    return posts.value.filter((p) => p.status === "published" || p.is_published);
  }

  function getBySlug(slug) {
    return posts.value.find((p) => p.slug === slug) || null;
  }

  return { posts, loading, loaded, fetchPosts, fetchAdminPosts, create, update, remove, getPublished, getBySlug };
});
