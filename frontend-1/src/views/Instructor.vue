<template>
    <div class="container-fluid">
        <div class="row">
            <!-- Sidebar -->
            <div class="col-md-3 col-lg-2 d-md-block bg-light sidebar">
                <div class="position-sticky pt-3">
                <ul class="nav flex-column">
                    <li class="nav-item">
                        <router-link class="nav-link" to="/instructor/dashboard" active-class="active-link">Statistics</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/instructor/milestones" active-class="active-link">Milestones</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/instructor/students" active-class="active-link">Students</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/instructor/insights" active-class="active-link">Document Insight</router-link>
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
                <InstructorDashboard :project_id="this.project_id" :key="this.project_id"/>
            </div>
            <div v-else-if="this.type=='insights'">
                <InstructorDocumentInsight :project_id="this.project_id" :key="this.project_id"/>
            </div>
            <div v-else-if="this.type=='milestones'">
                <InstructorMilestoneView :project_id="this.project_id" :key="this.project_id"/>
            </div>
            <div v-else-if="this.type=='students'">
                <InstructorStudentView :project_id="this.project_id" :key="this.project_id"/>
            </div>
        </div>
    </div>
</template>

<script>
import InstructorDashboard from '../components/InstructorDashboard.vue'
import InstructorDocumentInsight from '../components/InstructorDocumentInsight.vue'
import InstructorMilestoneView from '../components/InstructorMilestoneView.vue'
import InstructorStudentView from '../components/InstructorStudentView.vue'
import { ref } from 'vue'

export default{
    name: 'Instructor',
    components: {
        InstructorDashboard,
        InstructorDocumentInsight,
        InstructorMilestoneView,
        InstructorStudentView
    },
    data(){
        return {
            project_id: 1,
            projects: ref([]),
            current_project: '',
            type: this.$route.params.type,
            loading: true
        }
    },
    watch: {
        '$route.params.type': function(){
            this.type = this.$route.params.type
        },
    },
    methods: {
        async getProjects(){
            this.loading = true;
            const response = await fetch('http://localhost:5000/projects/' + localStorage.getItem('user_id'), {
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
        changeProject(project_id){
            this.project_id = project_id;
            this.current_project = this.projects.value.find(project => project.project_id == project_id).title;
        },
        logout() {
            localStorage.clear()
            this.$router.push('/')
        }
    },
    async created(){
        await this.getProjects();
    }
}
</script>