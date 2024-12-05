<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Chart from 'chart.js/auto';
import StatisticsCard from '../components/StatisticsCard.vue'
import Statistics from '../components/Statistics.vue'
// References for statistics
const stats = ref({
  totalProjects: 0,
  activeStudents: 0,
  completionRate: '0%',
  totalStudents: 0,
});

const router = useRouter()
const logout = () => {
  localStorage.clear()
  router.push('/')
}

// Fetch data for Completion Rate Chart
const fetchCompletionRate = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/admin/dashboard/statistics', {
      headers: {
        'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
        'Content-Type': 'application/json',
      },
    });
    if (response.ok) {
      const { data } = await response.json();
      stats.value = {
        ...stats.value,
        completionRate: `${data.completion_rate}%`,
      };
      renderCompletionRateChart(data.completion_rate);
    } else {
      console.error('Failed to fetch completion rate statistics.', await response.text());
    }
  } catch (error) {
    console.error('Error fetching completion rate statistics:', error);
  }
};

// Fetch data for Projects Chart
const fetchProjectsData = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/admin/dashboard/projects', {
      headers: {
        'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
        'Content-Type': 'application/json',
      },
    });
    if (response.ok) {
      const { data } = await response.json();
      renderProjectsChart(data.projects.length); // Assume number of projects as data for visualization
    } else {
      console.error('Failed to fetch projects data.', await response.text());
    }
  } catch (error) {
    console.error('Error fetching projects data:', error);
  }
};

// Fetch data for Students Chart
const fetchStudentsData = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/admin/dashboard/students', {
      headers: {
        'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
        'Content-Type': 'application/json',
      },
    });
    if (response.ok) {
      const { data } = await response.json();
      renderStudentsChart(data.students.length); // Number of students assigned
    } else {
      console.error('Failed to fetch students data.', await response.text());
    }
  } catch (error) {
    console.error('Error fetching students data:', error);
  }
};

// Fetch data for Milestone Chart
const fetchMilestonesData = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/admin/dashboard/milestones', {
      headers: {
        'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
        'Content-Type': 'application/json',
      },
    });
    if (response.ok) {
      const { data } = await response.json();
      const completed = data.milestones.filter(m => m.status === 'Completed').length;
      renderMilestonesChart(completed, data.milestones.length - completed);
    } else {
      console.error('Failed to fetch milestones data.', await response.text());
    }
  } catch (error) {
    console.error('Error fetching milestones data:', error);
  }
};

// Render Completion Rate Chart
const renderCompletionRateChart = (completionRate: number) => {
  const ctx = document.getElementById('completionRateChart') as HTMLCanvasElement;
  if (!ctx) return;

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Completed', 'Pending'],
      datasets: [
        {
          data: [completionRate, 100 - completionRate],
          backgroundColor: ['#4caf50', '#f44336'],
        },
      ],
    },
    options: {
      plugins: {
        legend: {
          position: 'bottom',
        },
      },
    },
  });
};

// Render Projects Chart
const renderProjectsChart = (totalProjects: number) => {
  const ctx = document.getElementById('projectsChart') as HTMLCanvasElement;
  if (!ctx) return;

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Projects'],
      datasets: [
        {
          label: 'Total Projects',
          data: [totalProjects],
          backgroundColor: ['#42A5F5'],
        },
      ],
    },
    options: {
      plugins: {
        legend: { display: false },
      },
    },
  });
};

// Render Students Chart
const renderStudentsChart = (totalStudents: number) => {
  const ctx = document.getElementById('studentsChart') as HTMLCanvasElement;
  if (!ctx) return;

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Students'],
      datasets: [
        {
          label: 'Total Students',
          data: [totalStudents],
          backgroundColor: ['#66BB6A'],
        },
      ],
    },
    options: {
      plugins: {
        legend: { display: false },
      },
    },
  });
};

// Render Milestones Chart
const renderMilestonesChart = (completed: number, pending: number) => {
  const ctx = document.getElementById('milestonesChart') as HTMLCanvasElement;
  if (!ctx) return;

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Completed', 'Pending'],
      datasets: [
        {
          data: [completed, pending],
          backgroundColor: ['#8E24AA', '#FF7043'],
        },
      ],
    },
    options: {
      plugins: {
        legend: { position: 'bottom' },
      },
    },
  });
};

// Call APIs and Render Charts on Mount
onMounted(() => {
  fetchCompletionRate();
  fetchProjectsData();
  fetchStudentsData();
  fetchMilestonesData();
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
          <div class="col-md-6">
            <canvas id="completionRateChart"></canvas>
          </div>
          <div class="col-md-6">
            <canvas id="projectsChart"></canvas>
          </div>
        </div>
        <div class="row mb-4">
          <div class="col-md-6">
            <canvas id="studentsChart"></canvas>
          </div>
          <div class="col-md-6">
            <canvas id="milestonesChart"></canvas>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
