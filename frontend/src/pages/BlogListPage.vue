<template>
  <main class="page-wrap">
    <section class="section-head">
      <h2>بلاگ</h2>
    </section>

    <section class="blog-grid">
      <RouterLink v-for="post in posts" :key="post.slug" :to="`/blog/${post.slug}`" class="blog-card">
        <img v-if="post.cover_image" :src="post.cover_image" :alt="post.title" />
        <div v-else class="blog-cover placeholder"></div>
        <h3>{{ post.title }}</h3>
        <p>{{ post.excerpt }}</p>
      </RouterLink>
    </section>

    <p v-if="!posts.length" class="empty-note">هنوز نوشته‌ای منتشر نشده است.</p>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/utils/api'

const posts = ref([])

onMounted(async () => {
  const res = await api.listBlogPosts()
  posts.value = res.items || []
})
</script>
