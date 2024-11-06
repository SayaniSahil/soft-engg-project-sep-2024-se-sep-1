<script setup lang="ts">
defineProps<{
  title: string
  value: number | string
  type?: 'primary' | 'success' | 'warning' | 'danger'
}>()
</script>

<template>
  <div class="card shadow-sm h-100">
    <div class="card-body">
      <h6 class="card-subtitle mb-2 text-muted">{{ title }}</h6>
      <h2 :class="`text-${type || 'primary'}`">{{ value }}</h2>
      <slot></slot>
    </div>
  </div>
</template>