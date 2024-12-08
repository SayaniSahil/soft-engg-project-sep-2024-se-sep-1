<script setup lang="ts">
import { onMounted, ref } from 'vue';
import Chart from 'chart.js/auto';

const chart1Data = ref(null);
const chart2Data = ref(null);
const chart3Data = ref(null);
const chart4Data = ref(null);

const fetchData = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/admin/dashboard/statistics', {
      headers: {
        
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      const data = await response.json();
      chart1Data.value = data.chart1;
      chart2Data.value = data.chart2;
      chart3Data.value = data.chart3;
      chart4Data.value = data.chart4;

      renderCharts();
    } else {
      console.error('Failed to fetch chart data.', await response.text());
    }
  } catch (error) {
    console.error('Error fetching chart data:', error);
  }
};

const renderCharts = () => {
  renderChart('chart1Canvas', chart1Data.value, 'bar', 'Chart 1');
  renderChart('chart2Canvas', chart2Data.value, 'line', 'Chart 2');
  renderChart('chart3Canvas', chart3Data.value, 'doughnut', 'Chart 3');
  renderChart('chart4Canvas', chart4Data.value, 'pie', 'Chart 4');
};

const renderChart = (id: string, data: any, type: string, title: string) => {
  const ctx = document.getElementById(id) as HTMLCanvasElement;
  if (!ctx || !data) return;

  new Chart(ctx, {
    type,
    data: {
      labels: data.labels,
      datasets: [
        {
          label: title,
          data: data.values,
          backgroundColor: ['#4caf50', '#f44336', '#2196f3', '#ffeb3b'],
          borderColor: ['#333333'],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom',
        },
      },
    },
  });
};

onMounted(() => {
  fetchData();
});
</script>

<template>
  <div class="container my-4">
    <!-- First row: 2 charts side by side -->
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body text-center">
            <canvas id="chart1Canvas"></canvas>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card">
          <div class="card-body text-center">
            <canvas id="chart2Canvas"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- Second row: 2 charts side by side -->
    <div class="row">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body text-center">
            <canvas id="chart3Canvas"></canvas>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card">
          <div class="card-body text-center">
            <canvas id="chart4Canvas"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.card {
  height: 100%;
}
</style>
