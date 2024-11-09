<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const isLoggedIn = computed(() => route.path !== '/')

const logout = () => {
  sessionStorage.removeItem('role')
  router.push('/')
}
</script>

<template>
  <nav v-if="isLoggedIn" class="navbar navbar-expand navbar-dark bg-dark fixed-top">
    <div class="container-fluid" style="margin-left: 20px;">
      <div class="navbar-brand hexagon-logo">
        <img src="../assets/logo2.jpeg" alt="Logo" class="logo">
      </div>
      <div class="navbar-brand pacifico-regular">Trackie</div>
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

</template>
