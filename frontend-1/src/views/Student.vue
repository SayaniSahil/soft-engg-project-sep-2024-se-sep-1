<template>
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <div class="col-md-3 col-lg-2 d-md-block bg-light sidebar">
                <div class="position-sticky pt-3">
                    <ul class="nav flex-column">
                        <li class="nav-item">
                            <router-link class="nav-link" to="/student/dashboard/0" active-class="active-link">Progress</router-link>
                        </li>
                        <li v-for="milestone in milestones" :key="milestone.id" class="nav-item">
                            <router-link class="nav-link" :to="'/student/milestones/'+milestone.id" active-class="active-link">{{ milestone.title }}</router-link>
                        </li>
                        <!-- Dropdown List -->
                        <li v-if="!loading" class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="dropdownMenuLink" data-bs-toggle="dropdown" aria-expanded="false">
                            {{ current_project }}
                            </a>
                            <ul class="dropdown-menu" aria-labelledby="dropdownMenuLink">
                            <li v-for="project in this.projects.value" :key="project.project_id">
                                <a class="dropdown-item" href="#" @click="changeProject(project.project_id)">
                                    {{ project.title }}
                                </a>
                            </li>
                            </ul>
                        </li>
                    </ul>
                </div>
                <div class="nav-link logout" @click="logout">Logout</div>
            </div>

            <div v-if="this.type=='dashboard'">
                <StudentDashboard :project_id="this.project_id" :key="this.project_id"/>
            </div>
            <div v-else-if="this.type=='milestones'">
                <MilestoneDetailView :id="parseInt(this.id)" :project_id="this.project_id" :key="this.project_id + this.id"/>
            </div>
        </div>
    </div>
</template>

<script>
import StudentDashboard from '../components/StudentDashboard.vue'
import MilestoneDetailView from '../components/MilestoneDetailView.vue'
import { ref } from 'vue'

export default {
  components: {
    StudentDashboard,
    MilestoneDetailView
  },
    data() {
        return {
        student_id: localStorage.getItem('user_id'),
        project_id: 1,
        projects: ref([]),
        milestones: ref([]),
        current_project: '',
        type: this.$route.params.type,
        id: this.$route.params.id,
        loading: true,
        }
    },
    watch: {
        '$route.params.type': function(){
            this.type = this.$route.params.type
        },
        '$route.params.id': function(){
            this.id = this.$route.params.id
        }
    },
    methods: {
        async getProjects(){
            this.loading = true;
            const response = await fetch('http://localhost:5000/student/projects/' + localStorage.getItem('user_id'), {
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
            this.projects.value = result.projects;
            this.current_project = this.projects.value[0].title;
            this.loading = false;
        },
        async changeProject(project_id){
            this.project_id = project_id;
            this.current_project = this.projects.value.find(project => project.project_id == project_id).title;
            if (this.type == 'milestones') {
                this.$router.push('/student/dashboard/0');
            }
            await this.fetchMilestoneStatus();
        },
        async fetchMilestoneStatus() {
            this.milestone_loading = true;
            this.error = null;
            if (this.student_id === null || this.project_id === null) {
                this.error = "Student ID or Project ID not provided.";
                return;
            }
            const response = await fetch('http://localhost:5000/student/milestones/' + this.student_id + '/' + this.project_id, {
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
            this.milestone_loading = false;
        },
        logout(){
            localStorage.clear();
            this.$router.push('/')
        }
    },
    async created(){
        await this.getProjects();
        await this.fetchMilestoneStatus();
    }
}

</script>