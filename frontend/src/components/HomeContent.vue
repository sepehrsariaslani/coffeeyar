<template>
  <section v-if="html" class="home-editorial">
    <div class="home-editorial__line" />
    <div class="home-editorial__body" v-html="html" />
  </section>
</template>

<script setup>
defineProps({
  html: { type: String, default: null },
})
</script>

<style scoped>
.home-editorial {
  padding: 4rem 5vw;
  max-width: 720px;
  margin: 0 auto;
}

.home-editorial__line {
  width: 2.5rem;
  height: 1px;
  background-color: #800000;
  margin-bottom: 2.5rem;
}

.home-editorial__body {
  font-family: 'Vazirmatn', sans-serif;
  font-size: 1rem;
  font-weight: 300;
  line-height: 2;
  color: #4a4540;
}

.home-editorial__body :deep(h2) {
  font-size: 1.25rem;
  font-weight: 400;
  color: #111;
  margin-bottom: 1rem;
}

.home-editorial__body :deep(p) {
  margin-bottom: 1.25rem;
}

.home-editorial__body :deep(a) {
  color: #800000;
  text-decoration: none;
  border-bottom: 1px solid #80000040;
}
</style>
