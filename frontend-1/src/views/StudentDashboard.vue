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
              <router-link class="nav-link" :to="'/student/milestones/'+milestone.id" active-class="active-link">{{ milestone.title }}</router-link>
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
          <ProgressComponent :student_id="parseInt(student_id)" :project_id="project_id"/>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import ProgressComponent from '../components/ProgressComponent.vue'

export default {
  components: {
    ProgressComponent
  },
  data() {
    return {
      milestones: [
      { id: 1, name: 'Project Document', status: 'completed' },
      { id: 2, name: 'Milestone 1', status: 'completed' },
      { id: 3, name: 'Milestone 2', status: 'pending' },
      { id: 4, name: 'Milestone 3', status: 'pending' },
      { id: 5, name: 'Milestone 4', status: 'pending' }
    ],
    student_id: localStorage.getItem('user_id'),
    project_id: 1
    }
  },
  methods: {
    async fetchMilestoneStatus() {
            this.loading = true;
            this.error = null;
            if (this.student_id === null || this.project_id === null) {
                this.error = "Student ID or Project ID not provided.";
                return;
            }
            const response = await fetch('http://localhost:5000/student/milestones/' + this.student_id, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('token'),
                },
            });
            const result = await response.json();
            if (!response.ok) {
                this.error = result.error;
                return;
            }
            this.milestones = result.milestones;
            // Make sure project document is the first milestone
            this.milestones = this.milestones.sort((a, b) => a.title === 'Project Document' ? -1 : 1);
            let temp = this.milestones[0];
            // Reverse the rest
            this.milestones = this.milestones.slice(1).reverse();
            this.milestones.unshift(temp);
        },
    logout(){
      localStorage.clear();
      this.$router.push('/');
    }
  },
  async created() {
    await this.fetchMilestoneStatus()
  }
}

</script>
