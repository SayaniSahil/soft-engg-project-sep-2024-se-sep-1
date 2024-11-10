<template>
  <div class="container-fluid">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-3 col-lg-2 d-md-block bg-light sidebar">
        <div class="position-sticky pt-3">
          <ul class="nav flex-column">
            <li class="nav-item">
              <router-link class="nav-link" to="/admin" active-class="active-link">Statistics</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/projects" active-class="active-link">Projects</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/stats" active-class="active-link">Project Stats</router-link>
            </li>
          </ul>
        </div>
        <div class="nav-link logout" @click="logout">Logout</div>
      </div>

      <!-- Main content -->
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div class="pt-3 pb-2 mb-3 border-bottom">
          <h1>Project Statistics</h1>
        </div>
        <ProjectList :projects="projects" :showStats="true"/>
      </main>
    </div>
  </div>
</template>

<script>
    import { ref } from 'vue'
    import StatisticsCard from '../components/StatisticsCard.vue'
    import ProjectList from '../components/ProjectList.vue'

    export default {
        name: 'AdminProjectStats',
        components: {
            StatisticsCard,
            ProjectList
        },
        data(){
            return {
                projects: null,
            };
        },
        methods: {
            async getProjects(){
                // Fetch projects from backend
                this.projects = [
                { project_id: 1, title: 'Project 1', description: "This is Project 1", students: 13, instructors: ["instructor1@gmail.com", "instructor2@gmail.com"] },
                { project_id: 2, title: 'Project 2', description: "This is Project 2", students: 34, instructors: ["instructor3@gmail.com", "instructor4@gmail.com"] },
                { project_id: 3, title: 'Project 3', description: "This is Project 3", students: 12, instructors: ["instructor5@gmail.com", "instructor6@gmail.com"] },
                { project_id: 4, title: 'Project 4', description: "This is Project 4", students: 45, instructors: ["instructor7@gmail.com", "instructor8@gmail.com"] },
                { project_id: 5, title: 'Project 5', description: "This is Project 5", students: 23, instructors: ["instructor9@gmail.com", "instructor10@gmail.com"] },
                ];
            },
            async initializePage(){
                await this.getProjects();
            },
            async logout(event){
                event.preventDefault();
                // Clear session storage and redirect to login page
                sessionStorage.clear();
                this.$router.push('/');
            }
        },
        async created(){
            this.getProjects();
        }
    }
</script>
