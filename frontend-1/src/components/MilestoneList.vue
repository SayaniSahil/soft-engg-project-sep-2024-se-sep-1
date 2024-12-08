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
                <div @click.stop="editMilestone(index)">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                    <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                    <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                  </svg>
                </div>
                <div data-bs-toggle="modal" data-bs-target="#deleteProject" @click.stop="confirmDelete(index)">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
                    <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                </svg>
                </div>
            </div>
          </li>
        </ul>
      </div>

      <!-- Milestone Details Section -->
      <div v-if="this.generating_milestones" class="center-box">
        Generating Milestones
      </div>
       <div class="col-1 p-4"></div>
      <div class="col-7 p-4">
        <h3>{{ currentMilestone.title }}</h3>
        <p>{{ currentMilestone.description }}</p>
        <p>Start Date: {{ currentMilestone.start_date }}</p>
        <p>End Date: {{ currentMilestone.end_date }}</p>
        <p>Weightage: {{ currentMilestone.weightage }}%</p>
        <h5 class="mt-4">Documents</h5>
        <p class="text-muted">{{ currentMilestone.document_url }}</p>
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
                  v-model="this.problemStatement"
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
                  v-model.number="this.milestoneCount"
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

    <!-- Edit Milestone Modal -->
    <div class="modal fade" :class="{ show: showEditModal }" tabindex="-1" role="dialog" style="display: block;" v-if="showEditModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Milestone</h5>
            <button type="button" class="btn-close" @click="closeEditModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateMilestone">
              <div class="mb-3">
                <label class="form-label">Title</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="editingMilestone.title"
                  required
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea 
                  class="form-control" 
                  v-model="editingMilestone.description"
                  rows="3"
                  required
                ></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Start Date</label>
                <input 
                  type="date" 
                  class="form-control" 
                  v-model="editingMilestone.start_date"
                  required
                >
              </div>
              <div class="mb-3">
                <label class="form-label">End Date</label>
                <input 
                  type="date" 
                  class="form-control" 
                  v-model="editingMilestone.end_date"
                  required
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Weightage</label>
                <input 
                  type="number" 
                  class="form-control" 
                  v-model.number="editingMilestone.weightage"
                  default="0"
                  required
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Document URL</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="editingMilestone.document_url"
                >
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeEditModal">Cancel</button>
                <button type="submit" class="btn btn-primary">Save Changes</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div class="modal fade" :class="{ show: showDeleteModal }" tabindex="-1" role="dialog" style="display: block;" v-if="showDeleteModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Delete</h5>
            <button type="button" class="btn-close" @click="closeDeleteModal"></button>
          </div>
          <div class="modal-body">
            Are you sure you want to delete this milestone?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDeleteModal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="deleteMilestone">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    milestones: Array,
    project_id: Number,
  },
  data() {
    return {
      showModal: false,
      showEditModal: false,
      showDeleteModal: false,
      generating_milestones: false,
      problemStatement: '',
      milestoneCount: 1,
      selectedMilestone: 0,
      editingMilestone: null,
      deletingIndex: null,
      loading: false,
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
    },    
    async generateMilestones () {
      // Set the flag to indicate that milestones are being generated
      this.generating_milestones = true;
      this.closeModal();
      //console.log(this.problemStatement, this.milestoneCount)
    // Call the llm API
    let response = await fetch('http://localhost:5000/milestone/' + localStorage.getItem("user_id") + '/' + this.project_id, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': localStorage.getItem('token')
        },
        body: JSON.stringify({
        'description' : this.problemStatement,
        'numbermilestones': this.milestoneCount
        }),
    })
    let result = await response.json()
    if (!response.ok) {
        alert(result.error)
        return 
    }
      // Reset the flag
      this.generating_milestones = false;
      this.problemStatement = '';
      this.milestoneCount = 1;
      // Emit an event to notify the parent component
      this.$emit('milestones-generated');
    },
    editMilestone(index) {
      this.editingMilestone = { ...this.milestones[index] };
      //console.log(this.editingMilestone);
      this.showEditModal = true;
    },

    closeEditModal() {
      this.showEditModal = false;
      this.editingMilestone = null;
    },
    async updateMilestone() {
      try {
        const response = await fetch(`http://localhost:5000/instructor/milestones/${this.editingMilestone.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('token')
          },
          body: JSON.stringify(this.editingMilestone)
        });

        if (response.ok) {
          const result = await response.json();
          const index = this.milestones.findIndex(m => m.id === this.editingMilestone.id);
          if (index !== -1) {
            this.milestones[index] = result.milestone;
          }
          this.closeEditModal();
        } else {
          const error = await response.json();
          alert(error.message || 'Failed to update milestone');
        }
      } catch (error) {
        alert('Error updating milestone');
        console.error(error);
      }
    },
    selectMilestone(index) {
      this.selectedMilestone = index;
    },
    confirmDelete(index) {
      this.deletingIndex = index;
      console.log(this.deletingIndex);
      this.showDeleteModal = true;
    },

    closeDeleteModal() {
      this.showDeleteModal = false;
      this.deletingIndex = null;
    },

    async deleteMilestone() {
      try {
        const milestone = this.milestones[this.deletingIndex];
        const response = await fetch(`http://localhost:5000/instructor/milestones/${milestone.id}`, {
          method: 'DELETE',
          headers: {
            'Authentication-Token': localStorage.getItem('token')
          }
        });

        if (response.ok) {
          this.milestones.splice(this.deletingIndex, 1);
          if (this.selectedMilestone === this.deletingIndex) {
            this.selectedMilestone = Math.max(0, this.deletingIndex - 1);
          }
          this.closeDeleteModal();
        } else {
          const error = await response.json();
          alert(error.message || 'Failed to delete milestone');
        }
      } catch (error) {
        alert('Error deleting milestone');
        console.error(error);
      }
    },
  },
};
</script>
