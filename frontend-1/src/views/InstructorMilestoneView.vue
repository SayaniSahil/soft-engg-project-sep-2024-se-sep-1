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
          <h1>Milestones</h1>
        </div>

        <!-- Milestones -->
        <MilestoneList :milestones="this.milestones" :project_id="this.project_id" @milestones-generated="fetchMilestones"/>
      </main>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import StatisticsCard from '../components/StatisticsCard.vue'
import MilestoneList from '../components/MilestoneList.vue'

export default {
  components: {
    MilestoneList
  },
  data(){
    return {
      milestones: [
        { id: 1, title: 'Project Document', description: 'Create a project document with the project details.' },
        { id: 2, title: 'Milestone 1', description: 'Complete milestone 1.' },
        { id: 3, title: 'Milestone 2', description: 'Complete milestone 2.' },
        { id: 4, title: 'Milestone 3', description: 'Complete milestone 3.' },
        { id: 5, title: 'Milestone 4', description: 'Complete milestone 4.' }
      ]
    ,
    students: [
      { id: 1, name: 'Student 1', progress: 75 },
      { id: 2, name: 'Student 2', progress: 45 },
      { id: 3, name: 'Student 3', progress: 90 }
    ],
    project_id: 1,
  }
},
  methods: {
    async fetchMilestones() {
      const response = await fetch('http://localhost:5000/instructor/milestones/' + localStorage.getItem('user_id'), {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('token')
        }
      });
      const result = await response.json();
      if (!response.ok) {
        alert(result.error);
        return;
      }
      this.milestones = result.milestones;
      // Make milestone with title Project Document, the first milestone
      this.milestones.sort((a, b) => a.title === 'Project Document' ? -1 : 1);
      let temp = this.milestones[0];
      // Reverse the rest
      this.milestones = this.milestones.slice(1).reverse();
      this.milestones.unshift(temp);
    },
    logout() {
      localStorage.clear()
      router.push('/')
    }
  },
  async created() {
    await this.fetchMilestones()
  }
}

</script>

