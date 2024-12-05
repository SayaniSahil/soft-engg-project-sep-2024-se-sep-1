<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ProgressComponent from '../components/ProgressComponent.vue'

const milestones = ref([
  { id: 1, name: 'Project Document', status: 'completed' },
  { id: 2, name: 'Milestone 1', status: 'completed' },
  { id: 3, name: 'Milestone 2', status: 'pending' },
  { id: 4, name: 'Milestone 3', status: 'pending' },
  { id: 5, name: 'Milestone 4', status: 'pending' }
])

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
              <router-link class="nav-link" to="/student" active-class="active-link">Progress</router-link>
            </li>
            <li v-for="milestone in milestones" :key="milestone.id" class="nav-item">
              <router-link class="nav-link" :to="'/student/milestones/'+milestone.id" active-class="active-link">{{ milestone.name }}</router-link>
            </li>
          </ul>
        </div>
        <div class="nav-link logout" @click="logout">Logout</div>
      </div>

      <!-- Main content -->
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div class="pt-3 pb-2 mb-3 border-bottom">
          <h1>Progress Overview</h1>
        </div>

        <div>
          <ProgressComponent/>
        </div>
      </main>
    </div>
  </div>
</template>
