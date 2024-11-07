<template>
    <div class="container-fluid">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-3 col-lg-2 d-md-block bg-light sidebar">
        <div class="position-sticky pt-3">
          <div class="sidebar-header d-flex align-items-center">
            <i class="bi bi-house-door-fill me-2"></i> <!-- Example icon, use any icon you like -->
            <span class="app-name">My Application</span>
          </div>
          <ul class="nav flex-column">
            <li class="nav-item">
              <router-link class="nav-link" to="/student" active-class="active-link">Progress</router-link>
            </li>
            <li v-for="milestone in this.milestones" :key="milestone.id" class="nav-item">
              <router-link class="nav-link" :to="'/student/milestones/'+milestone.id" active-class="active-link">{{ milestone.name }}</router-link>
            </li>
          </ul>
        </div>
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
            milestone: null,
            submissions: null,
        };
    },
    created(){
        console.log(this.id);
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

<style scoped>
.dashboard-title {
  font-weight: bold;
  font-size: 1.5rem;
}

.student-info p {
  color: #333;
}

.project-description {
  color: #333;
  font-size: 0.9rem;
}

.border-top {
  border-top: 1px solid #ccc;
}

.col-6 {
  border-right: 1px dashed #ccc;
}

.col-6:last-child {
  border-right: none;
}

.deadline-badge {
  background-color: #f8d7da;
  color: #721c24;
}
</style>