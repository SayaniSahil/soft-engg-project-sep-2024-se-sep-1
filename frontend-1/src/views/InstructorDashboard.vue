<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import StatisticsCard from '../components/StatisticsCard.vue'
import Statistics from '../components/Statistics.vue'

const students = ref([
  { id: 1, name: 'Student 1', progress: 75 },
  { id: 2, name: 'Student 2', progress: 45 },
  { id: 3, name: 'Student 3', progress: 90 }
])

const milestones = ref([
  { id: 1, name: 'Project Document', status: 'completed' },
  { id: 2, name: 'Milestone 1', status: 'completed' },
  { id: 3, name: 'Milestone 2', status: 'pending' },
  { id: 4, name: 'Milestone 3', status: 'pending' },
  { id: 5, name: 'Milestone 4', status: 'overdue' }
])

const router = useRouter()
const logout = () => {
  sessionStorage.clear()
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
              <router-link class="nav-link" to="/instructor" active-class="active-link">Statistics</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/instructor/milestones" active-class="active-link">Milestones</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/instructor/students" active-class="active-link">Students</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/instructor/github" active-class="active-link">Github History</router-link>
            </li>
          </ul>
        </div>
        <div class="nav-link logout" @click="logout">Logout</div>
      </div>

      <!-- Main content -->
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div class="pt-3 pb-2 mb-3 border-bottom">
          <h1>Instructor Dashboard</h1>
        </div>

        <!-- Statistics -->
        <div class="row mb-4">
          <div class="col-md-4">
            <StatisticsCard title="Total Students" :value="students.length" type="primary" />
          </div>
          <div class="col-md-4">
            <StatisticsCard 
              title="Average Progress" 
              :value="`${Math.round(students.reduce((acc, s) => acc + s.progress, 0) / students.length)}%`"
              type="success"
            />
          </div>
          <div class="col-md-4">
            <StatisticsCard 
              title="Active Milestones" 
              :value="milestones.filter(m => m.status === 'pending').length"
              type="warning"
            />
          </div>
        </div>
        <Statistics role="Instructor" :project_id="1"/>
      </main>
    </div>
  </div>
</template>
