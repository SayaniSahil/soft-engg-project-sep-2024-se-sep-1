<template> 
  <div class="container-fluid vh-100 d-flex">
    <!-- Main Content -->
    <div class="col-md-10 d-flex p-0">
      <!-- Milestone List Section -->
      <div class="col-4 p-4 bg-light">
        <button class="btn btn-outline-primary w-100 mb-3" @click="showModal = true">
          + Add/Generate Milestone
        </button>
        <ul class="list-group">
          <li
            v-for="(milestone, index) in milestones"
            :key="index"
            class="list-group-item d-flex justify-content-between align-items-center milestone-item"
            :class="{ 'selected-milestone': selectedMilestone === index }"
            @click="selectMilestone(index)"
          >
            {{ milestone.title }}
            <!-- Icon Section -->
            <div class="icon-container d-flex align-items-center">
                <div data-bs-toggle="modal" data-bs-target="#deleteProject" @click.stop="deleteMilestone(index)">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
                    <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                </svg>
                </div>
            </div>
          </li>
        </ul>
      </div>

      <!-- Milestone Details Section -->
       <div class="col-1 p-4"></div>
      <div class="col-7 p-4">
        <h3>{{ currentMilestone.title }}</h3>
        <p>{{ currentMilestone.description }}</p>
        <h5 class="mt-4">Documents</h5>
        <p class="text-muted">This section could display associated documents or files.</p>
      </div>
    </div>

    <!-- Modal for Adding Milestone -->
    <div class="modal fade" tabindex="-1" role="dialog" :class="{ show: showModal }" style="display: block" v-if="showModal">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h3 class="modal-title font-weight-bold">Add Project Document</h3>
            <button type="button" class="btn-close" aria-label="Close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="generateMilestones">
              <div class="form-group mb-3">
                <label for="problemStatement" class="form-label">Problem Statement</label>
                <textarea
                  id="problemStatement"
                  v-model="problemStatement"
                  class="form-control form-control-lg" 
                  rows="5"
                  placeholder="Describe the problem statement here..."
                  required
                ></textarea>
              </div>
              <div class="form-group mb-4">
                <label for="milestoneCount" class="form-label">Number of Milestones</label>
                <input
                  type="number"
                  id="milestoneCount"
                  v-model.number="milestoneCount"
                  class="form-control form-control-lg"
                  min="1"
                  placeholder="Enter the number of milestones"
                  required
                />
              </div>
              <button type="submit" class="btn btn-primary btn-lg w-100">Generate Milestones</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showModal: false,
      milestones: [],
      problemStatement: '',
      milestoneCount: 1,
      selectedMilestone: 0,
    };
  },
  computed: {
    currentMilestone() {
      return this.milestones[this.selectedMilestone] || { title: '', description: '' };
    },
  },
  methods: {
    closeModal() {
      this.showModal = false;
      this.problemStatement = '';
      this.milestoneCount = 1;
    },
    generateMilestones() {
      this.milestones = [
        { title: 'Project Document', description: this.problemStatement },
      ];
      for (let i = 1; i <= this.milestoneCount; i++) {
        this.milestones.push({
          title: `Milestone ${i}`,
          description: `Description of Milestone ${i}.`,
        });
      }
      this.closeModal();
    },
    selectMilestone(index) {
      this.selectedMilestone = index;
    },
    deleteMilestone(index) {
      this.milestones.splice(index, 1);
      this.renumberMilestones();
      if (this.selectedMilestone >= this.milestones.length) {
        this.selectedMilestone = this.milestones.length - 1;
      }
    },
    renumberMilestones() {
      this.milestones.forEach((milestone, i) => {
        if (i > 0) {
          milestone.title = `Milestone ${i}`;
          milestone.description = `Description of Milestone ${i}.`;
        }
      });
    }
  },
};
</script>
