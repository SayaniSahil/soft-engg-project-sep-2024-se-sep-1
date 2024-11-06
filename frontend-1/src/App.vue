<script setup lang="ts">
import NavBar from './components/NavBar.vue'
</script>

<template>
  <NavBar />
  <div class="content-wrapper">
    <router-view></router-view>
  </div>
</template>

<style>
.content-wrapper {
  padding-top: 104px; /* Account for both navbars */
}

/* Adjust sidebar top position to account for both navbars */
.sidebar {
  padding-top: 104px !important;
}
</style>