<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const isLoggedIn = computed(() => route.path !== '/')

const logout = () => {
  router.push('/')
}
</script>

<template>
  <nav v-if="isLoggedIn" class="navbar navbar-expand navbar-dark bg-dark fixed-top">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">Project Management</router-link>
      <div class="navbar-nav me-auto">
        <router-link class="nav-link" to="/admin">Admin</router-link>
        <router-link class="nav-link" to="/instructor">Instructor</router-link>
        <router-link class="nav-link" to="/student">Student</router-link>
      </div>
      <div class="navbar-nav">
        <button class="btn btn-outline-light" @click="logout">Logout</button>
      </div>
    </div>
  </nav>

  <!-- Debug Navigation -->
  <div v-if="isLoggedIn" class="debug-nav bg-light border-bottom" style="margin-top: 56px; padding: 0.5rem 1rem;">
    <div class="container-fluid">
      <small class="text-muted">Debug Navigation: </small>
      <div class="btn-group btn-group-sm">
        <button 
          class="btn btn-outline-secondary"
          @click="router.push('/admin')"
        >
          Admin
        </button>
        <button 
          class="btn btn-outline-secondary"
          @click="router.push('/instructor')"
        >
          Instructor
        </button>
        <button 
          class="btn btn-outline-secondary"
          @click="router.push('/student')"
        >
          Student
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.debug-nav {
  z-index: 900;
  position: fixed;
  top: 0;
  right: 0;
  left: 0;
}
.navbar{
  z-index: 1000;
}
</style>