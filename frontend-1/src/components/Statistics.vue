<template>
    <div class="container my-4">
      <!-- First row: 2 charts side by side -->
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body text-center">
              <img :src="'data:image/png;base64,' + chart1" alt="Chart 1" class="img-fluid">
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-body text-center">
              <img :src="'data:image/png;base64,' + chart2" alt="Chart 2" class="img-fluid">
            </div>
          </div>
        </div>
      </div>
  
      <!-- Second row: 2 charts side by side -->
      <div class="row">
        <div class="col-md-6">
          <div class="card">
            <div class="card-body text-center">
              <img :src="'data:image/png;base64,' + chart3" alt="Chart 3" class="img-fluid">
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-body text-center">
              <img :src="'data:image/png;base64,' + chart4" alt="Chart 4" class="img-fluid">
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>

<script>
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
        this.chart1 = "chart1_overall";
        this.chart2 = "chart2_overall";
        this.chart3 = "chart3_overall";
        this.chart4 = "chart4_overall";
    },
    projectStats(project_id){
        // Fetch project stats based on id from backend
        this.chart1 = "chart1_project";
        this.chart2 = "chart2_project";
        this.chart3 = "chart3_project";
        this.chart4 = "chart4_project";
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