<script setup lang="ts">
defineProps<{
  title: string
  text: string
  imgSrc?: string
}>()
</script>

<template>
  <div class="card h-100">
    <img v-if="imgSrc" :src="imgSrc" class="card-img-top" alt="Card image">
    <div class="card-body">
      <h5 class="card-title">{{ title }}</h5>
      <p class="card-text">{{ text }}</p>
      <slot></slot>
    </div>
  </div>
</template>