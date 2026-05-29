<template>
  <main class="page-wrap content-page blog-post" v-if="post">
    <img v-if="post.cover_image" :src="post.cover_image" :alt="post.title" class="blog-post-cover" />
    <h1>{{ post.title }}</h1>
    <p v-if="post.excerpt">{{ post.excerpt }}</p>
    <div v-if="post.content" v-html="post.content"></div>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/utils/api'

const props = defineProps({ slug: { type: String, required: true } })
const post = ref(null)

onMounted(async () => {
  post.value = await api.getBlogPost(props.slug)
})
</script>
