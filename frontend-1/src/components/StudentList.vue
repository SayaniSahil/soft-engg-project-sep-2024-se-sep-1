<template>
    <div class="row mb-4">
        <div class="col-md-4">
          <div style="margin-bottom: 10px;" data-bs-toggle="modal" data-bs-target="#addStudent">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 18 18">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
            </svg>  Add Student
        </div>
  
          <!-- Student List -->
          <div class="list-group">
                <div v-for="student in students" :key="student.id" 
                    class="list-group-item list-group-item-action d-flex justify-content-between align-items-center unclicked" :id="student.id"
                    @click="changeStuff(student.id)">
                    <div>
                        <div style="margin-bottom: 10px;">
                            {{ student.name }}<br>
                            Students Email: {{ student.email }}
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
                        <form id="add_student">
                            <div class="modal-header">
                                <h5 class="modal-title" id="addStudentLabel">Add Student</h5>
                            </div>
                            <div class="modal-body">
                                <input type="hidden" name="form_id" value="add_student">
                                <!-- Name input -->
                                <div data-mdb-input-init class="form-outline mb-4">
                                    <input type="text" name="title" id="title" class="form-control" v-model="newStudent.name" required maxlength=45/>
                                    <label class="form-label" for="name">Student Name</label>
                                </div>

                                <!-- Student Email input -->
                                <div data-mdb-input-init class="form-outline mb-4">
                                    <input type="email" id="student_email" name="student_email" class="form-control" v-model="newStudent.email" required maxlength=250/>
                                    <label class="form-label" for="student_email">Student Email</label>
                                </div>
                            
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button class="btn btn-success" @click="addStudent" data-bs-dismiss="modal">Add Student</button>
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
            <ProgressComponent />
        </div>
    </div>
  </template>
  
  <script>
import ProgressComponent from './ProgressComponent.vue';

  export default {
    data() {
      return {
        newStudent: { name: "", email: "" },
        students: [
          { id: 1, name: "Student Name 1", email: "student1@example.com", progress: 50 },
          { id: 2, name: "Student Name 2", email: "student2@gmail.com", progress: 75 },
          { id: 3, name: "Student Name 3", email: "student3@gmail.com", progress: 25 },
          {id: 4, name: "Student Name 4", email: "student4@gmail.com", progress: 100},
          { id: 5, name: "Student Name 5", email: "student5@gmail.com", progress: 10 },
        ],
        last_clicked: null,
        id: null,
        last_clicked: null,
      };
    },
    components: {
      ProgressComponent,
    },
    methods: {
      addStudent(event) {
        event.preventDefault();
        if (this.newStudent.name && this.newStudent.email) {
            let highest_id = 0;
            for (let i = 0; i < this.students.length; i++){
                if (this.students[i].id > highest_id){
                    highest_id = this.students[i].id;
                }
            }
          this.students.push({ ...this.newStudent, id: highest_id+1, progress: Math.floor(Math.random() * 101) });
          this.newStudent = { name: "", email: "" };
          this.showAddStudentForm = false;
        }
      },
      deleteStudent(event) {
        event.preventDefault();
        this.students = this.students.filter(student => student.id !== this.id);
        if(this.last_clicked == this.id && this.students.length > 0){
            this.changeStuff(this.students[0].id);
        }
      },
      changeStuff(id){
        console.log(id);
        let ele = document.getElementById(id);
        console.log(ele);
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
  }
  };
  </script>