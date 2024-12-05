<template>
    <div class="container-fluid">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-3 col-lg-2 d-md-block bg-light sidebar">
        <div class="position-sticky pt-3">
          <ul class="nav flex-column">
            <li class="nav-item">
              <router-link class="nav-link" to="/student" active-class="active-link">Progress</router-link>
            </li>
            <li v-for="milestone in this.milestones" :key="milestone.id" class="nav-item">
              <router-link class="nav-link" :to="'/student/milestones/'+milestone.id" active-class="active-link">{{ milestone.name }}</router-link>
            </li>
          </ul>
        </div>
        <div class="nav-link logout" @click="logout">Logout</div>
      </div>

      <!-- Main content -->
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div class="pt-3 pb-2 mb-3 border-bottom">
          <h1>{{ this.milestones[this.id-1]["name"] }}</h1>
        </div>

        <div v-if="this.id == 1" class="row pt-4">
          <div class="col-6">
            <h5 class="text-center">Project Document</h5>
            <p class="project-description">
              Ponam in culpa idiot aliis pravitatis. Principium ponere culpam in se justum praeceptum. Neque
              improperes et aliis qui non perfecte ipse docuit.
            </p>
            <p class="project-description">
              Quod Enchiridion Epictetus stoici scripsit. Rodrigo Abela et Technologiae apud Massachusetts
              instituta Opera collectio. Ex anglicus latine translata sunt.
            </p>
            <p class="fw-bold">Documents</p>
          </div>
          <div class="col-6 text-center">
            <h5>Submission</h5>
            <p>No Submission Required</p>
          </div>
        </div>

        <div v-else class="row pt-4">
          <div class="col-6">
            <h5 class="text-center">{{ this.milestones[this.id-1]["name"] }}</h5>
            <p class="project-description">
              Ponam in culpa idiot aliis pravitatis. Principium ponere culpam in se justum praeceptum. Neque
              improperes et aliis qui non perfecte ipse docuit.
            </p>
            <p class="project-description">
              Quod Enchiridion Epictetus stoici scripsit. Rodrigo Abela et Technologiae apud Massachusetts
              instituta Opera collectio. Ex anglicus latine translata sunt.
            </p>
            <p class="fw-bold">Documents</p>
          </div>
          <div class="col-6 text-center">
            <h5>Submission</h5>
            <!-- Submission Deadline -->
              <div class="row justify-content-center mb-3">
            <div class="col-auto">
              <span class="badge deadline-badge">Submission Deadline xx/xx/xxxx 00:00 am</span>
              <form @submit.prevent="submitGithubUrl" class="mt-3">
                <div class="mb-3">
                  <label for="urlInput" class="form-label">Enter URL</label>
                  <input
                    type="url"
                    class="form-control"
                    id="urlInput"
                    v-model="githubUrl"
                    placeholder="https://example.com"
                    required
                  />
                </div>
                <div class="text-center">
                  <button type="submit" class="btn btn-primary">Submit</button>
                </div>
              </form>
              <div v-if="submissionMessage" class="mt-3 alert" :class="submissionStatus ? 'alert-success' : 'alert-danger'">
                {{ submissionMessage }}
              </div>
            </div>
          </div>



          <!-- Questions Section -->
          <div class="row mb-3">
            <div class="col">
              <p><strong>1. Did you complete all the requirements?</strong></p>
              <div class="form-check form-check-inline">
                <input class="form-check-input" type="radio" name="requirement" id="requirementYes" value="yes">
                <label class="form-check-label" for="requirementYes">Yes</label>
              </div>
              <div class="form-check form-check-inline">
                <input class="form-check-input" type="radio" name="requirement" id="requirementNo" value="no">
                <label class="form-check-label" for="requirementNo">No</label>
              </div>
            </div>
          </div>

          <div class="row mb-4">
            <div class="col">
              <p><strong>2. Did you commit and push on GitHub?</strong></p>
              <div class="form-check form-check-inline">
                <input class="form-check-input" type="radio" name="github" id="githubYes" value="yes">
                <label class="form-check-label" for="githubYes">Yes</label>
              </div>
              <div class="form-check form-check-inline">
                <input class="form-check-input" type="radio" name="github" id="githubNo" value="no">
                <label class="form-check-label" for="githubNo">No</label>
              </div>
            </div>
          </div>

          <!-- Upload Documents Section -->
          <div class="row">
            <div class="col">
              <p class="fw-bold">Upload Documents</p>
              <p>Please upload document link</p>
              <input type="text" class="form-control" />
            </div>
          </div>
        </div>

        </div>
      </main>
    </div>
  </div>
</template>

<script>
import StatisticsCard from '../components/StatisticsCard.vue'
export default{
    name: 'MilestoneDetailView',
    props: ['id'],
    components: {
        StatisticsCard
    },
    data(){
        return {
            githubUrl: '',
            milestone: null,
            submissions: null,
        };
    },
    methods: {
        async logout(event){
            event.preventDefault()
            sessionStorage.clear()
            this.$router.push('/')
        },
        
        async submitGithubUrl() {
          try {
            const token = sessionStorage.getItem('authToken'); // Retrieve the token from session storage
            const response = await fetch('http://localhost:5000/assignment', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`, // Add token to the Authorization header
              },
              body: JSON.stringify({
                github_url: this.githubUrl, // Send only the URL
              }),
            });

            if (!response.ok) {
              const errorData = await response.json();
              throw new Error(errorData.error || 'Failed to submit. Please try again.');
            }

            const responseData = await response.json();
            this.submissionMessage = responseData.message || 'GitHub URL submitted successfully!';
            this.submissionStatus = true;
          } catch (error) {
            this.submissionMessage = error.message || 'An error occurred. Please try again.';
            this.submissionStatus = false;
          }
        }
        
    },
    created(){
        this.milestones = [
        { id: 1, name: 'Project Document', status: 'completed' },
        { id: 2, name: 'Milestone 1', status: 'completed' },
        { id: 3, name: 'Milestone 2', status: 'pending' },
        { id: 4, name: 'Milestone 3', status: 'pending' },
        { id: 5, name: 'Milestone 4', status: 'pending' }
        ]
    },
    watch: {
    // Watch for changes in the `id` prop
    id(newId, oldId) {
      console.log(newId);
      // You can add logic to fetch new data or update the view
    }
}
}
</script>