<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')

const handleLogin = async () => {
  // Call the login API
  let response = await fetch('http://localhost:5000/login_user', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: email.value,
      password: password.value,
    }),
  })
  let result = await response.json()
  if (!response.ok) {
    alert(result.message)
    return
  }
  result.role = result.role.toLowerCase()
  localStorage.setItem('token', result.token)
  localStorage.setItem('username', result.username)
  localStorage.setItem('role', result.role)
  localStorage.setItem('id', result.email.split('@')[0])
  localStorage.setItem('user_id', result.id)
  router.push('/' + result.role)
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
            <label for="email" class="form-label">Email</label>
            <input
              type="text"
              class="form-control"
              id="email"
              v-model="email"
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