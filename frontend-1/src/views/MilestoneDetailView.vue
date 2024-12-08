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
            <input type="text"  v-model="document_url" class="form-control" />
            <button type="button"  @click = "submitmilestone"  class="btn btn-primary">Submit</button>

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
          milestone: null,
        submissions: null,
        document_url:'',
          
      };
  },
  methods: {
      async logout(event){
          event.preventDefault()
          sessionStorage.clear()
          this.$router.push('/')
    },
    async submitmilestone() {
    // Check if URL is provided
    if (!this.document_url) {
      alert("Please enter a document link.");
      return;
    }

    // Prepare the data to send to the backend
    const data = {
      document_url: this.document_url,
      student_id: localStorage.getItem('id'),
      milestone_id: this.id,
    };
    console.log("print data",data)
    // Send a POST request to the backend
    try {
      const response = await fetch(" http://127.0.0.1:5000/submitmilestone", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json; charset=UTF-8',
          Authorization: "Bearer " + localStorage.getItem("token"), // Assuming user is authenticated
        },
      });
      const result = await response.json();

      if (response.ok) {
        console.log("Document link submitted:", result);
        alert("Document link submitted successfully!");
        this.document_url = ''; // Clear the input field
      } else {
        alert(result.message || "There was an error submitting the document.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("There was an error submitting the document.");
    }
  },
    
      
  },
  created(){
      this.milestones = [
      { id: 0, name: 'Project Document', status: 'completed' },
      { id: 1, name: 'Milestone 1', status: 'completed' },
      { id: 2, name: 'Milestone 2', status: 'pending' },
      { id: 3, name: 'Milestone 3', status: 'pending' },
      { id: 4, name: 'Milestone 4', status: 'pending' }
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