import { defineStore } from "pinia";
import { ref } from "vue";
import { posts as initialPosts } from "@/lib/data.js";

const STORAGE_KEY = "navar_posts_v1";

function loadPosts() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {}
  return initialPosts.map((p) => ({
    ...p,
    status: "published",
    coverImage: "",
    author: "نوار",
    updatedAt: p.date,
  }));
}

export const usePostsStore = defineStore("posts", () => {
  const posts = ref(loadPosts());

  function save() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(posts.value));
  }

  function create(data) {
    const slug =
      data.slug ||
      data.title
        .replace(/\s+/g, "-")
        .replace(/[^a-zA-Z0-9\u0600-\u06FF-]/g, "")
        .toLowerCase() +
        "-" +
        Date.now();
    const post = {
      slug,
      title: data.title || "بدون عنوان",
      excerpt: data.excerpt || "",
      body: data.body || "",
      date: new Date().toLocaleDateString("fa-IR"),
      updatedAt: new Date().toLocaleDateString("fa-IR"),
      readTime: data.readTime || "۵ دقیقه",
      category: data.category || "عمومی",
      status: data.status || "draft",
      coverImage: data.coverImage || "",
      author: data.author || "نوار",
    };
    posts.value.unshift(post);
    save();
    return post;
  }

  function update(slug, data) {
    const idx = posts.value.findIndex((p) => p.slug === slug);
    if (idx !== -1) {
      posts.value[idx] = {
        ...posts.value[idx],
        ...data,
        updatedAt: new Date().toLocaleDateString("fa-IR"),
      };
      save();
    }
  }

  function remove(slug) {
    posts.value = posts.value.filter((p) => p.slug !== slug);
    save();
  }

  function getPublished() {
    return posts.value.filter((p) => p.status === "published");
  }

  return { posts, create, update, remove, getPublished };
});
