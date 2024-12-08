<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Chart from 'chart.js/auto';
import StatisticsCard from '../components/StatisticsCard.vue'
import Statistics from '../components/Statistics.vue'
// References for statistics
const stats = ref({
  daily_submissions: [],
  milestone_submission_stats: [],
  milestone_density: [],
});

let total_projects = ref(0);
let milestones_due_this_week = ref(0);
let milestones_completed_this_week = ref(0);
let total_students = ref(0);

const router = useRouter()
const logout = () => {
  localStorage.clear()
  router.push('/')
}

// Fetch data for Completion Rate Chart
const fetchCompletionRate = async () => {
  try {
    const response = await fetch('http://localhost:5000/admin/dashboard/statistics', {
      headers: {
        'Authentication-Token': `${localStorage.getItem('token')}`,
        'Content-Type': 'application/json',
      },
    });
    if (response.ok) {
      const { data } = await response.json();
      total_projects.value = data.total_projects;
      milestones_due_this_week.value = data.milestones_due_this_week;
      milestones_completed_this_week.value = data.milestones_completed_this_week;
      total_students.value = data.total_students;
      stats.daily_submissions = data.daily_submissions;
      stats.milestone_submission_stats = data.milestone_submission_stats;
      stats.milestone_density = data.milestone_density;
      renderDailySubmissionChart(stats.daily_submissions);
      renderMilestonePieChart(stats.milestone_submission_stats);
      renderMilestoneDensity(stats.milestone_density);
      console.log(data);
    } else {
      console.error('Failed to fetch completion rate statistics.', await response.text());
    }
  } catch (error) {
    console.error('Error fetching completion rate statistics:', error);
  }
};

const renderDailySubmissionChart = (daily_submissions: any) => {
  const ctx = document.getElementById('dailySubmissionChart') as HTMLCanvasElement;
  if (!ctx) return;

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: daily_submissions.map((s: any) => s.date),
      datasets: [
        {
          label: 'Submissions',
          data: daily_submissions.map((s: any) => s.count),
          borderColor: '#2196f3',
          fill: false,
        },
      ],
    },
    options: {
      scales: {
        x: {
          title: {
            display: true,
            text: 'Date',
          },
        },
        y: {
          title: {
            display: true,
            text: 'Submissions',
          },
        },
      },
      plugins: {
        legend: { display: false },
        title: {
        display: true,
        text: 'Daily Submission Stats',
        font: {
            size: 16,
            weight: 'bold',
          },
      }
      },
    },
  });
};

const renderMilestonePieChart = (milestone_submission_stats: any) => {
  const ctx = document.getElementById('milestonePieChart') as HTMLCanvasElement;
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

const renderMilestoneDensity = (milestone_density: any) => {
  const ctx = document.getElementById('milestoneDensityChart') as HTMLCanvasElement;
  if (!ctx) return;

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: milestone_density.map((s: any) => s.date),
      datasets: [
        {
          label: 'Submissions',
          data: milestone_density.map((s: any) => s.count),
          borderColor: '#2196f3',
          fill: false,
        },
      ],
    },
    options: {
      scales: {
        x: {
          title: {
            display: true,
            text: 'End Date',
          },
        },
        y: {
          title: {
            display: true,
            text: 'Count',
          },
        },
      },
      plugins: {
        legend: { display: false },
        title: {
        display: true,
        text: 'Milestone Density',
        font: {
            size: 16,
            weight: 'bold',
          },
      }
      },
    },
  });
}

// Call APIs and Render Charts on Mount
onMounted(() => {
  fetchCompletionRate();
});
</script>

<template>
  <div class="container-fluid">
    <div class="row">
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
        <h1>Admin Dashboard</h1>
        <div class="row mb-4">
          <div class="col-md-3">
            <StatisticsCard title="Total Projects" :value="total_projects" type="primary"/>
          </div>
          <div class="col-md-3">
            <StatisticsCard title="Milestones Due This Week" :value="milestones_due_this_week" type="danger"/>
          </div>
          <div class="col-md-3">
            <StatisticsCard title="Milestones Completed This Week" :value="milestones_completed_this_week" type="success"/>
          </div>
          <div class="col-md-3">
            <StatisticsCard title="Total Students" :value="total_students" type="primary"/>
          </div>
        </div>
        <div class="row mb-4">
          <div class="col-md-6 d-flex justify-content-center">
            <canvas id="dailySubmissionChart"></canvas>
          </div>
          <div class="col-md-6 d-flex justify-content-center">
            <canvas id="milestonePieChart"></canvas>
          </div>
        </div>
        <div class="row mb-4">
          <div class="col-md-12 d-flex justify-content-center">
            <canvas id="milestoneDensityChart"></canvas>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
