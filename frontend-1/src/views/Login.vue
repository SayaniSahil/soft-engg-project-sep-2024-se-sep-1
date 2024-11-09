<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')

const handleLogin = () => {
  // Simple routing based on user type
  if(username.value == 'admin' && password.value == 'admin'){
    sessionStorage.setItem('role', 'admin')
    router.push('/admin')
  }else if(username.value == 'instructor' && password.value == 'instructor'){
    sessionStorage.setItem('role', 'instructor')
    router.push('/instructor')
  }else if(username.value == 'student' && password.value == 'student'){
    sessionStorage.setItem('role', 'student')
    router.push('/student')
  }else{
    alert('Invalid credentials')
  }
}
</script>

<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center bg-light">
    <div class="background-image"></div>
    <div class="card shadow-sm login-container" style="width: 400px">
      <div class="card-body p-4">
        <h2 class="text-center mb-4">Login</h2>
        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              type="text"
              class="form-control"
              id="username"
              v-model="username"
              required
            >
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              type="password"
              class="form-control"
              id="password"
              v-model="password"
              required
            >
          </div>
          <button type="submit" class="btn btn-primary w-100">Login</button>
        </form>
      </div>
    </div>
  </div>
</template>