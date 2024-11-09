<script setup lang="ts">
import StudentList from '../components/StudentList.vue'
</script>

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
      </div>

      <!-- Main content -->
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div class="pt-3 pb-2 mb-3 border-bottom" style="padding: 0;">
          <h1>Student List</h1>
        </div>

        <StudentList/>

      </main>
    </div>
  </div>
</template>