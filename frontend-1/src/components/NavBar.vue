<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const name = ref(localStorage.getItem('username') || '')
const id = ref(localStorage.getItem('id') || '')

// Function to update the state based on sessionStorage
const updateFromSessionStorage = () => {
  name.value = localStorage.getItem('username') || ''
  id.value = localStorage.getItem('id') || ''
}

// Watch for changes in the route, indicating a page change or login
watch(route, () => {
  updateFromSessionStorage(); // Update session data whenever route changes
}, { immediate: true });

const isLoggedIn = computed(() => route.path !== '/' && route.path !== '/register-instructor')
</script>

<template>
  <nav v-if="isLoggedIn" class="navbar navbar-expand navbar-dark bg-dark fixed-top">
    <div class="container-fluid" style="margin-left: 20px;">
      <div class="navbar-brand hexagon-logo">
        <img src="../assets/logo2.jpeg" alt="Logo" class="logo">
      </div>
      <div class="navbar-brand pacifico-regular">Trackie</div>
      <div class="navbar-nav me-auto">
      </div>
      <div class="navbar-nav">
        <div class="nav-item greeting" style="margin-right: 20px;">
          <div>Welcome, {{ name }}<br>{{ id }}</div>
        </div>
        <div class="navbar-brand circle-logo">
            <img src="../assets/placeholder.png" alt="Logo" class="logo-2">
        </div>
        <!--<button class="btn btn-outline-light" @click="logout">Logout</button>-->
      </div>
    </div>
  </nav>

</template>
