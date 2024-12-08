<template>
    <div class="row mb-4">
        <div class="col-md-4">
          <div style="margin-bottom: 10px;" data-bs-toggle="modal" data-bs-target="#addStudent">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 18 18">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
            </svg>  Add Student
        </div>
  
          <!-- Student List -->
          <div v-if="!this.student_loading" class="list-group">
                <div v-for="student in students" :key="student.id" 
                    class="list-group-item list-group-item-action d-flex justify-content-between align-items-center unclicked" :id="student.id"
                    @click="changeStuff(student.id)">
                    <div>
                        <div style="margin-bottom: 10px;">
                            {{ student.name }}<br>
                            Email: {{ student.email }}
                        </div>
                        <div class="progress">
                            <div class="progress-bar" role="progressbar" :style="'width: '+student.progress+'% !important'" :aria-valuenow="student.progress" aria-valuemin="0" aria-valuemax="100"></div>
                        </div>
                    </div>
                    
                    <!-- Icon Section -->
                    <div class="icon-container d-flex align-items-center">
                        <div data-bs-toggle="modal" data-bs-target="#deleteStudent" @click.stop="changeId(student.id)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
                            <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                        </svg>
                        </div>
                    </div>
                </div>
            </div>
            <div>
                <!-- Add Student Modal -->
                <div class="modal fade" id="addStudent" tabindex="-1" role="dialog" aria-labelledby="addStudentLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <form id="add_student" enctype="multipart/form-data">
                            <div class="modal-header">
                                <h5 class="modal-title" id="addStudentLabel">Add Students</h5>
                            </div>
                            <input type="file" id="document" name="document" accept=".csv">
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button class="btn btn-success" type="submit" @click="addStudents" data-bs-dismiss="modal">Upload Document</button>
                            </div>
                        </form>
                    </div>
                    </div>
                </div>

                <!-- Delete Student Modal -->
                <div class="modal fade" id="deleteStudent" tabindex="-1" role="dialog" aria-labelledby="deleteStudentLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <div class="alert alert-warning" role="alert">
                            This action will remove the student from the project.
                        </div>
                        <form id="delete_student">
                            <div class="modal-header">
                                <h5 class="modal-title" id="deleteStudentLabel">Student</h5>
                            </div>
                            <div class="modal-body">
                                <label class="form-label">Are you sure?</label>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button class="btn btn-danger" @click="deleteStudent" data-bs-dismiss="modal">Delete Student</button>
                            </div>
                        </form>
                    </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-1"></div>
        <div class="col-md-7" id="statsPanel">
            <ProgressComponent :student_id="this.student_id" :project_id="this.project_id" />
        </div>
    </div>
  </template>
  
  <script>
import ProgressComponent from './ProgressComponent.vue';

  export default {
    props: {
      students: Object,
      project_id: Number,
    },
    data() {
      return {
        newStudent: { name: "", email: "" },
        student_loading: false,
        last_clicked: null,
        id: -1,
        student_id: null,
      };
    },
    components: {
      ProgressComponent,
    },
    methods: {
        async addStudents(event){
            event.preventDefault();
            let form = document.getElementById('add_student');
            let formData = new FormData(form);
            const response = await fetch('http://localhost:5000/students/bulk-upload/' + localStorage.getItem('user_id') + '/' + this.project_id, {
                method: 'POST',
                headers: {
                    'Authentication-Token': localStorage.getItem('token'),
                },
                body: formData,
            });
            const result = await response.json();
            if (!response.ok) {
                alert(result.error);
                return;
            }
            this.$emit('new-students');
      },
      async deleteStudent(event) {
        event.preventDefault();
        const response = await fetch('http://localhost:5000/students/' + localStorage.getItem('user_id') + '/' + this.project_id, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': localStorage.getItem('token'),
          },
          body: JSON.stringify({ id: this.id }),
        });
        const result = await response.json();
        if (!response.ok) {
          alert(result.error);
          return;
        }
        this.$emit('new-students');
      },
      changeStuff(id){
        //console.log(id);
        this.student_id = id;
        let ele = document.getElementById(id);
        //console.log(ele);
        if(this.last_clicked != null){
            let last_ele = document.getElementById(this.last_clicked);
            if(last_ele != null){
            last_ele.classList.remove("clicked");
            last_ele.classList.add("unclicked");
            }
        }
        ele.classList.remove("unclicked");
        ele.classList.add("clicked");
        this.last_clicked = id;
    },
    changeId(id){
        this.id = id;
    },
},
    mounted(){
    if(this.students.length > 0){
        this.changeStuff(this.students[0].id);
    }
  },
  };
  </script>