<script setup lang="ts">
import { ref } from 'vue'
import StatisticsCard from '../components/StatisticsCard.vue'
import MilestoneList from '../components/MilestoneList.vue'
import ProgressComponent from '../components/ProgressComponent.vue'

const studentProgress = ref(65)
const milestones = ref([
  { id: 1, name: 'Project Document', status: 'completed' },
  { id: 2, name: 'Milestone 1', status: 'completed' },
  { id: 3, name: 'Milestone 2', status: 'pending' },
  { id: 4, name: 'Milestone 3', status: 'pending' },
  { id: 5, name: 'Milestone 4', status: 'pending' }
])

const submissions = ref([
  { id: 1, name: 'Project Proposal', status: 'submitted', grade: 'A' },
  { id: 2, name: 'Progress Report', status: 'pending', grade: '-' }
])
</script>

<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-3 col-lg-2 d-md-block bg-light sidebar">
        <div class="position-sticky pt-3">
          <div class="sidebar-header d-flex align-items-center">
            <i class="bi bi-house-door-fill me-2"></i> <!-- Example icon, use any icon you like -->
            <span class="app-name">My Application</span>
          </div>
          <ul class="nav flex-column">
            <li class="nav-item">
              <router-link class="nav-link" to="/student" active-class="active-link">Progress</router-link>
            </li>
            <li v-for="milestone in milestones" :key="milestone.id" class="nav-item">
              <router-link class="nav-link" :to="'/student/milestones/'+milestone.id" active-class="active-link">{{ milestone.name }}</router-link>
            </li>
          </ul>
        </div>
      </div>

      <!-- Main content -->
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div class="pt-3 pb-2 mb-3 border-bottom">
          <h1>Progress Overview</h1>
        </div>

        <div>
          <ProgressComponent />
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