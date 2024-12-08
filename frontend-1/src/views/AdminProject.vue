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
          <h1>Project Details</h1>
        </div>
        <ProjectList v-if="!this.project_loading" :projects="this.projects" :showStats="false"/>
      </main>
    </div>
  </div>
</template>

<script>
    import { ref } from 'vue'
    import { useRouter } from 'vue-router'
    import StatisticsCard from '../components/StatisticsCard.vue'
    import ProjectList from '../components/ProjectList.vue'

    export default {
        name: 'AdminProject',
        components: {
            StatisticsCard,
            ProjectList
        },
        data(){
            return {
                projects: null,
                project_loading: true
            };
        },
        methods: {
            async getProjects(){
                // Fetch projects from backend
                this.projects = [];
                this.project_loading = true;
                const response = await fetch('http://localhost:5000/projects', {
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
                this.projects = result.projects;
                //console.log(this.projects);
                this.project_loading = false;
            },
            async logout(event){
                event.preventDefault();
                localStorage.clear();
                this.$router.push('/');
            }
        },
        async created(){
            await this.getProjects();
        }
    }
</script>
