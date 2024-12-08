<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Chart from 'chart.js/auto';
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
  localStorage.clear()
  router.push('/')
}

// Refs for holding API data
const total_milestones = ref(0);
const total_students = ref(0);
const average_completion_rate = ref(0);
const stats = ref({
  buckets: [],
  milestone_submission_stats: [],
});

// Fetch data from APIs
const fetchChartData = async () => {
  try {
    // Fetch project data
    const projectResponse = await fetch(`http://localhost:5000/projects/statistics/` + localStorage.getItem('user_id'),{
      headers: {
        'Authentication-Token': `${localStorage.getItem('token')}`,
        'Content-Type': 'application/json',
      },
    });
    if (projectResponse.ok) {
      const projectData = await projectResponse.json();
      total_milestones.value = projectData.total_milestones;
      total_students.value = projectData.total_students;
      average_completion_rate.value = projectData.average_completion_rate;
      stats.buckets = projectData.buckets;
      stats.milestone_submission_stats = projectData.milestone_submission_stats;
    }

    renderCharts(stats.buckets, stats.milestone_submission_stats);
  } catch (error) {
    console.error('Error fetching chart data:', error);
  }
};

// Render charts
const renderCharts = (buckets, milestone_submission_stats) => {
  renderHistogram(buckets);
  renderMilestonePieChart(milestone_submission_stats);
};

// Individual chart rendering functions
const renderHistogram = (buckets) => {
  const ctx = document.getElementById('milestoneCompletionRate') as HTMLCanvasElement;
  if (!ctx) return;

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%'],
      datasets: [{
        label: 'Milestones',
        data: buckets,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        x: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Milestone Completion Rate'
          }
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Number of Milestones'
          }
        }
      },
      plugins: {
        legend: {
          display: false
        },
        title: {
          display: true,
          text: 'Milestone Completion Rate Distribution'
        }
      }
    }
  });
};

const renderMilestonePieChart = (milestone_submission_stats) => {
  const ctx = document.getElementById('submissionDistribution') as HTMLCanvasElement;
  if (!ctx) return;

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['On Time', 'Late', 'Early'],
      datasets: [
        {
          data: milestone_submission_stats,
          backgroundColor: ['#2196f3', '#f44336', '#4caf50'],
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' },
        title: {
        display: true,
        text: 'Milestone Submission Stats',
        font: {
            size: 16,
            weight: 'bold',
          },
      }
      },
    },
  });
};

// Fetch data and render charts on mount
onMounted(() => {
  fetchChartData();
});
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
            <StatisticsCard title="Total Students" :value="total_students" type="primary" />
          </div>
          <div class="col-md-4">
            <StatisticsCard 
              title="Total Milestones" 
              :value="total_milestones"
              type="success"
            />
          </div>
          <div class="col-md-4">
            <StatisticsCard 
              title="Average Completion Rate" 
              :value="average_completion_rate"
              type="warning"
            />
          </div>
        </div>
        <div class="row mb-4">
          <div class="col-md-6 d-flex justify-content-center">
            <canvas id="milestoneCompletionRate"></canvas>
          </div>
          <div class="col-md-6 d-flex justify-content-center">
            <canvas id="submissionDistribution"></canvas>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
