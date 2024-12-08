<template>
  <div class="container-fluid">
  <div v-if="!loading" class="row">
    <!-- Sidebar -->
    <div class="col-md-3 col-lg-2 d-md-block bg-light sidebar">
      <div class="position-sticky pt-3">
        <ul class="nav flex-column">
          <li class="nav-item">
            <router-link class="nav-link" to="/student" active-class="active-link">Progress</router-link>
          </li>
          <li v-for="milestone in this.milestones" :key="milestone.id" class="nav-item">
            <router-link class="nav-link" :to="'/student/milestones/'+milestone.id" active-class="active-link">{{ milestone.title }}</router-link>
          </li>
        </ul>
      </div>
      <div class="nav-link logout" @click="logout">Logout</div>
    </div>

    <!-- Main content -->
    <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
      <div class="pt-3 pb-2 mb-3 border-bottom">
        <h1>{{ this.title }}</h1>
      </div>

      <div class="row pt-4">
      <div class="col-6">
        <h5 class="text-center">{{ this.title }}</h5>
        <p class="project-description">
          {{ this.description }}
        </p>
        <p class="fw-bold">Documents</p>
        <p>{{ this.document_url }}</p>
      </div>
      <div v-if="this.weightage>0" class="col-6 text-center">
        <h5>Submission</h5>
        <!-- Submission Deadline -->
        <div class="row justify-content-center mb-3">
          <div class="col-auto">
            <span v-if="this.status=='completed'" class="badge text-bg-success">Submitted Successfully</span><br>
            <span class="badge deadline-badge">Submission Deadline {{ this.end_date }}</span><br>
            <span class="badge deadline-badge">Weightage: {{ this.weightage }}</span><br>
            <span class="badge deadline-badge">Note: You can only submit once.</span>
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
          <button v-if="this.status != 'completed'" type="button"  @click = "submitmilestone"  class="btn btn-primary">Submit</button>

        </div>
      </div>
    </div>
    <div v-else class="col-6 text-center">
        <h5>Submission</h5>
        <p>No Submission Required</p>
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
          milestone: {"id":1,"title":"Project Document","status":"completed"},
          title: '',
        description: '',
        weightage: 0,
        start_date: '',
        end_date: '',
        document_url: '',
        status: 'pending',
        milestones: [],
        submissions: null,
        document_url:'',
        student_id: localStorage.getItem('user_id'),
        project_id: 1,
        loading: true,
          
      };
  },
  watch: {
  // Watch for changes in the `id` prop
  id(newId, oldId) {
    this.loading = true;
    this.changeMilestone();
    this.loading = false;
    // You can add logic to fetch new data or update the view
  }
},
  methods: {
    async fetchMilestoneStatus() {
            this.loading = true;
            if (this.student_id === null || this.project_id === null) {
                this.error = "Student ID or Project ID not provided.";
                return;
            }
            const response = await fetch('http://localhost:5000/student/milestones/' + this.student_id, {
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
            console.log(result);
            this.milestones = result.milestones;
            // Make sure project document is the first milestone
            this.milestones = this.milestones.sort((a, b) => a.title === 'Project Document' ? -1 : 1);
            let temp = this.milestones[0];
            // Reverse the rest
            this.milestones = this.milestones.slice(1).reverse();
            this.milestones.unshift(temp);
            // Make milestone the one with id
            for (let i = 0; i < this.milestones.length; i++) {
                if (this.milestones[i].id === this.id) {
                    this.milestone = this.milestones[i];
                    break;
                }
            }
            this.title = this.milestone.title;
            this.description = this.milestone.description;
            this.weightage = this.milestone.weightage;
            this.start_date = this.milestone.start_date;
            this.end_date = this.milestone.end_date;
            this.document_url = this.milestone.document_url;
            this.status = this.milestone.status;
            this.loading = false;
        },
      changeMilestone(){
        for (let i = 0; i < this.milestones.length; i++) {
            if (this.milestones[i].id == this.id) {
                this.milestone = this.milestones[i];
                break;
            }
        }
        this.title = this.milestone.title;
        this.description = this.milestone.description;
        this.weightage = this.milestone.weightage;
        this.start_date = this.milestone.start_date;
        this.end_date = this.milestone.end_date;
        this.document_url = this.milestone.document_url;
        this.status = this.milestone.status;
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
      student_id: localStorage.getItem('user_id'),
      milestone_id: this.id,
    };
    // Send a POST request to the backend
    try {
      const response = await fetch(" http://localhost:5000/submitmilestone", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json; charset=UTF-8',
          'Authentication-Token': localStorage.getItem("token"), // Assuming user is authenticated
        },
      });
      const result = await response.json();

      if (response.ok) {
        console.log("Document link submitted:", result);
        this.status = 'completed';
        for (let i = 0; i < this.milestones.length; i++) {
            if (this.milestones[i].id == this.id) {
                this.milestones[i].status = 'completed';
                break;
            }
        }
        this.document_url = ''; // Clear the input field
      } else {
        alert(result.message || "There was an error submitting the document.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("There was an error submitting the document.");
    }
  },
  
  async logout(event){
          event.preventDefault()
          localStorage.clear()
          this.$router.push('/')
    },
    
      
  },
  async created(){
      await this.fetchMilestoneStatus()
      console.log("Yes I am here")
  }
  }
</script>