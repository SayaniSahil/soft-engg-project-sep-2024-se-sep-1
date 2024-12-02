<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import StatisticsCard from '../components/StatisticsCard.vue'
import Statistics from '../components/Statistics.vue'

const stats = ref({
  totalProjects: 15,
  activeStudents: 45,
  completionRate: '78%'
})

const router = useRouter()
const logout = () => {
  localStorage.clear()
  router.push('/')
}
</script>

<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-3 col-lg-2 d-md-block bg-light sidebar">
        <div class="position-sticky pt-3">
          <ul class="nav flex-column">
            <li class="nav-item">
              <router-link class="nav-link" to="/admin" active-class="active-link">Statistics</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/projects" active-class="active-link">Projects</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/stats" active-class="active-link">Project Stats</router-link>
            </li>
          </ul>
        </div>
        <div class="nav-link logout" @click="logout">Logout</div>
      </div>

      <!-- Main content -->
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div class="pt-3 pb-2 mb-3 border-bottom">
          <h1>Admin Dashboard</h1>
        </div>

        <!-- Statistics -->
        <div class="row mb-4">
          <div class="col-md-4">
            <StatisticsCard title="Total Projects" :value="stats.totalProjects" type="primary" />
          </div>
          <div class="col-md-4">
            <StatisticsCard title="Active Students" :value="stats.activeStudents" type="success" />
          </div>
          <div class="col-md-4">
            <StatisticsCard title="Completion Rate" :value="stats.completionRate" type="warning" />
          </div>
        </div>
        <Statistics role="Admin"/>
      </main>
    </div>
  </div>
</template>
