<template>
  <!-- Main content -->
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div class="pt-3 pb-2 mb-3 border-bottom">
          <h1>Progress Overview</h1>
        </div>

        <div>
          <ProgressComponent :student_id="parseInt(student_id)" :project_id="project_id"/>
        </div>
      </main>
</template>

<script>
import ProgressComponent from '../components/ProgressComponent.vue'

export default {
  components: {
    ProgressComponent
  },
  props:{
    project_id: Number,
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
    }
  }
}

</script>
