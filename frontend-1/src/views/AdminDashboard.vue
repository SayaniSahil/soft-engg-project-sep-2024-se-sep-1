<script setup lang="ts">
import { ref } from 'vue'
import StatisticsCard from '../components/StatisticsCard.vue'

const stats = ref({
  totalProjects: 15,
  activeStudents: 45,
  completionRate: '78%'
})
</script>

<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-3 col-lg-2 d-md-block bg-light sidebar">
        <div class="position-sticky pt-3">
          <ul class="nav flex-column">
            <li class="nav-item">
              <router-link class="nav-link" to="/admin">Statistics</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/projects">Projects</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/stats">Project Stats</router-link>
            </li>
          </ul>
        </div>
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
      </main>
    </div>
  </div>
</template>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 100;
  padding: 48px 0 0;
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, .1);
}
</style>