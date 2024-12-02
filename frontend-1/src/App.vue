<script setup lang="ts">
import NavBar from './components/NavBar.vue'
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const contentWrapperClass = computed(() => {
  return {
    'content-wrapper': route.name !== 'login' && route.name !== 'register-instructor', // Apply default padding class if not on Login route
    'login-wrapper': route.name === 'login' || route.name === 'register-instructor',      // Apply no padding class if on Login route
  };
});
</script>

<template>
  <NavBar />
  <div :class="contentWrapperClass">
    <router-view></router-view>
  </div>
</template>

<style>
@import 'bootstrap/dist/css/bootstrap.min.css';
@import './style.css';
</style>