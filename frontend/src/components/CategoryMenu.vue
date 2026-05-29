<template>
  <div class="menu-overlay" :class="{ open }" @click.self="$emit('close')">
    <aside class="menu-sheet">
      <button class="menu-close" @click="$emit('close')">✕</button>
      <nav>
        <RouterLink v-for="link in links" :key="link.to" :to="link.to" class="menu-link" @click="$emit('close')">
          {{ link.label }}
        </RouterLink>
      </nav>
    </aside>
  </div>
</template>

<script setup>
defineProps({
  open: Boolean,
  links: {
    type: Array,
    default: () => [],
  },
})
</script>
