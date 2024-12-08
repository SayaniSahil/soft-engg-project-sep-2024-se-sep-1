<template>

      <!-- Main content -->
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div class="pt-3 pb-2 mb-3 border-bottom">
          <h1>Milestones</h1>
        </div>

        <!-- Milestones -->
        <MilestoneList :milestones="this.milestones" :project_id="this.project_id" @milestones-generated="fetchMilestones"/>
      </main>
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
  props: {
    project_id: Number
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
  }
},
  methods: {
    async fetchMilestones() {
      const response = await fetch('http://localhost:5000/instructor/milestones/' + localStorage.getItem('user_id') + '/' + this.project_id, {
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
  },
  async created() {
    await this.fetchMilestones()
  }
}

</script>

