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
        <div class="pt-3 pb-2 mb-3 border-bottom" style="padding: 0;">
          <h1>Student List</h1>
        </div>

        <StudentList v-if="!this.student_loading" :students="this.students" :project_id="this.project_id" @new-students="fetchStudents"/>

      </main>
    </div>
  </div>
</template>

<script>
import StudentList from '../components/StudentList.vue'
import { useRouter } from 'vue-router';

export default {
  name: 'InstructorStudentView',
  components: {
    StudentList,
  },
  data() {
    return {
      student_loading: true,
      students: [],
      project_id: 1,
    };
  },
  methods: {
    async fetchStudents() {
      this.student_loading = true;
      const response = await fetch('http://localhost:5000/students/' + localStorage.getItem('user_id'), {
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
    logout() {
      localStorage.clear()
      this.$router.push('/')
    },
  },
  async created() {
    await this.fetchStudents();
  },
}
</script>