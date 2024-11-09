<template>
    <div class="container my-4">
      <!-- First row: 2 charts side by side -->
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body text-center">
              <img :src="chart1">
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-body text-center">
              <img :src="chart2">
            </div>
          </div>
        </div>
      </div>
  
      <!-- Second row: 2 charts side by side -->
      <div class="row">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body text-center">
              <img :src="chart3">
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-body text-center">
              <img :src="chart4">
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>

<script>
import pieChart from '../assets/Pie-Chart-Sample.png';
import barChart from '../assets/Bar-Chart-Sample.png';

export default {
  name: 'Statistics',
  props: {
    role: String,
    project_id: Number
  },
  data(){
    return {
        chart1: null,
        chart2: null,
        chart3: null,
        chart4: null,
    };
  },
  methods: {
    overallStats(){
        // Fetch overall stats from backend
        this.chart1 = pieChart;
        this.chart2 = barChart;
        this.chart3 = barChart;
        this.chart4 = pieChart;
    },
    projectStats(project_id){
        // Fetch project stats based on id from backend
        this.chart1 = pieChart;
        this.chart2 = barChart;
        this.chart3 = barChart;
        this.chart4 = pieChart;
    }
  },
  mounted(){
    if(this.role == "Admin"){
        this.overallStats();
    }else if(this.role == "Instructor"){
        this.projectStats(this.project_id);
    }
  }
}
</script>