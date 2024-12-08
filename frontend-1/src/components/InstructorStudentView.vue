<template>

      <!-- Main content -->
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div class="pt-3 pb-2 mb-3 border-bottom" style="padding: 0;">
          <h1>Student List</h1>
        </div>

        <StudentList v-if="!this.student_loading" :students="this.students" :project_id="this.project_id" @new-students="fetchStudents"/>

      </main>
</template>

<script>
import StudentList from '../components/StudentList.vue'
import { useRouter } from 'vue-router';

export default {
  name: 'InstructorStudentView',
  components: {
    StudentList,
  },
  props: {
    project_id: Number,
  },
  data() {
    return {
      student_loading: true,
      students: [],
    };
  },
  methods: {
    async fetchStudents() {
      this.student_loading = true;
      const response = await fetch('http://localhost:5000/students/' + localStorage.getItem('user_id') + '/' + this.project_id, {
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': localStorage.getItem('token'),
        },
      })
      const result = await response.json()
      //console.log(result)
      if (!response.ok) {
        alert(result.error)
        return
      }
      this.students = result.students;
      this.student_loading = false;
    },
  },
  async created() {
    await this.fetchStudents();
  },
}
</script>