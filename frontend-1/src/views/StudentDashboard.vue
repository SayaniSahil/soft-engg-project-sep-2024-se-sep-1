<script setup lang="ts">
import { ref } from 'vue'
import StatisticsCard from '../components/StatisticsCard.vue'
import MilestoneList from '../components/MilestoneList.vue'

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
          <ul class="nav flex-column">
            <li class="nav-item">
              <a class="nav-link active" href="#">Progress</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Project Document</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Submissions</a>
            </li>
          </ul>
        </div>
      </div>

      <!-- Main content -->
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div class="pt-3 pb-2 mb-3 border-bottom">
          <h1>Student Dashboard</h1>
        </div>

        <!-- Progress Overview -->
        <div class="row mb-4">
          <div class="col-md-4">
            <StatisticsCard title="Overall Progress" :value="`${studentProgress}%`" type="primary" />
          </div>
          <div class="col-md-4">
            <StatisticsCard 
              title="Completed Milestones" 
              :value="milestones.filter(m => m.status === 'completed').length"
              type="success"
            />
          </div>
          <div class="col-md-4">
            <StatisticsCard 
              title="Pending Submissions" 
              :value="submissions.filter(s => s.status === 'pending').length"
              type="warning"
            />
          </div>
        </div>

        <!-- Milestones -->
        <div class="card shadow-sm mb-4">
          <div class="card-header">
            <h5 class="card-title mb-0">Milestones Progress</h5>
          </div>
          <div class="card-body">
            <MilestoneList :milestones="milestones" />
          </div>
        </div>

        <!-- Submissions -->
        <div class="card shadow-sm">
          <div class="card-header">
            <h5 class="card-title mb-0">Recent Submissions</h5>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table">
                <thead>
                  <tr>
                    <th>Submission</th>
                    <th>Status</th>
                    <th>Grade</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="submission in submissions" :key="submission.id">
                    <td>{{ submission.name }}</td>
                    <td>
                      <span :class="`badge bg-${submission.status === 'submitted' ? 'success' : 'warning'}`">
                        {{ submission.status }}
                      </span>
                    </td>
                    <td>{{ submission.grade }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
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