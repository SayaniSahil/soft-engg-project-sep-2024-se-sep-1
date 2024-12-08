<template>
  <div class="row mb-4">
        <div class="col-md-4">
            <div style="margin-bottom: 10px;" v-if="!showStats" data-bs-toggle="modal" data-bs-target="#addProject">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 18 18">
                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z"/>
                </svg>   Add Project
            </div>
            <div class="list-group">
                <div v-for="project in projects" :key="project.project_id" 
                    class="list-group-item list-group-item-action d-flex justify-content-between align-items-center unclicked" :id="project.project_id"
                    @click="changeStuff(project.project_id)">
                    <div>
                        {{ project.title }}<br>
                        Students Registered: {{ project.students }}<br>
                        Instructors Assigned: {{ project.instructors.length }}
                    </div>
                    
                    <!-- Icon Section -->
                    <div v-if="!showStats" class="icon-container d-flex align-items-center">
                        <div data-bs-toggle="modal" data-bs-target="#editProject" @click.stop="changeId(project.project_id, 0)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
                            <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                            <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                        </svg>
                        </div>
                        <div data-bs-toggle="modal" data-bs-target="#deleteProject" @click.stop="changeId(project.project_id, 1)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
                            <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                        </svg>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="!showStats" class="Modals">
                <!-- Add Project Modal -->
                <div class="modal fade" id="addProject" tabindex="-1" role="dialog" aria-labelledby="addProjectLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <form id="add_project">
                            <div class="modal-header">
                                <h5 class="modal-title" id="addProjectLabel">Add Project</h5>
                            </div>
                            <div class="modal-body">
                                <input type="hidden" name="form_id" value="add_project">
                                <!-- Name input -->
                                <div data-mdb-input-init class="form-outline mb-4">
                                    <input type="text" name="title" id="title" class="form-control" required maxlength=45/>
                                    <label class="form-label" for="name">Project Title</label>
                                </div>

                                <!-- Description input -->
                                <div data-mdb-input-init class="form-outline mb-4">
                                    <input type="text" id="Description" name="description" class="form-control" required maxlength=250/>
                                    <label class="form-label" for="description">Description</label>
                                </div>

                                <!-- Instructors input -->
                                <div data-mdb-input-init class="form-outline mb-4">
                                    <input type="email" id="instructor_email" name="instructor_email" class="form-control" required maxlength=250/>
                                    <label class="form-label" for="instructor_email">Instructor Email</label>
                                </div>
                            
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button class="btn btn-success" @click="addProject" data-bs-dismiss="modal">Add Project</button>
                            </div>
                        </form>
                    </div>
                    </div>
                </div>
                <!-- Edit Project Modal -->
                <div class="modal fade" id="editProject" tabindex="-1" role="dialog" aria-labelledby="editProjectLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <form id="edit_project">
                            <div class="modal-header">
                                <h5 class="modal-title" id="editProjectLabel">Edit Project</h5>
                            </div>
                            <div class="modal-body">
                                <input type="hidden" name="form_id" value="edit_project">
                                <!-- Name input -->
                                <div data-mdb-input-init class="form-outline mb-4">
                                    <input type="text" name="title" id="title" class="form-control" required maxlength=45/>
                                    <label class="form-label" for="name">Project Title</label>
                                </div>

                                <!-- Description input -->
                                <div data-mdb-input-init class="form-outline mb-4">
                                    <input type="text" id="Description" name="description" class="form-control" required maxlength=250/>
                                    <label class="form-label" for="description">Description</label>
                                </div>

                                <!-- Instructors input -->
                                <div data-mdb-input-init class="form-outline mb-4">
                                    <input type="email" id="instructor_email" name="instructor_email" class="form-control" required maxlength=250/>
                                    <label class="form-label" for="instructor_email">Instructor Email</label>
                                </div>
                            
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button class="btn btn-success" @click="editProject" data-bs-dismiss="modal">Edit Project</button>
                            </div>
                        </form>
                    </div>
                    </div>
                </div>
                <!-- Delete Project Modal -->
                <div class="modal fade" id="deleteProject" tabindex="-1" role="dialog" aria-labelledby="deleteProjectLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <div class="alert alert-warning" role="alert">
                            This action will delete the project and all associated milestones.
                        </div>
                        <form id="delete_project">
                            <div class="modal-header">
                                <h5 class="modal-title" id="deleteProjectLabel">Delete Project</h5>
                            </div>
                            <div class="modal-body">
                                <label class="form-label">Are you sure?</label>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button class="btn btn-danger" @click="deleteProject" data-bs-dismiss="modal">Delete Project</button>
                            </div>
                        </form>
                    </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-1"></div>
        <div v-if="showStats" class="col-md-7" id="statsPanel">
        </div>
        <div v-else class="col-md-7" id="descriptionPanel">
            <div style="text-align: center;">
                <h2 id="projectTitle"></h2>
            </div>
            <p id="projectDescription"></p><br>
            <p id="projectInstructors"></p>
        </div>
    </div>
</template>

<script>


export default {
  props: {
    role: String,
    showStats: Boolean,
    project: Object,
    projects: Object
  },
  data(){
    return {
      project_id: null,
      title: null,
      description: null,
      pie_chart: null,
      bar_chart: null,
      instructors: null,
      students: null,
      last_clicked: null,
    };
  },
  methods: {
    async addProject(event){
        event.preventDefault();
        // Get all details from form, title, description, and instructors
        let form = document.getElementById("add_project");
        const response = await fetch('http://localhost:5000/projects', {
           method: 'POST',
           headers: {
               'Content-Type': 'application/json',
               'Authentication-Token': localStorage.getItem('token')
           },
           body: JSON.stringify({
               'title': form.title.value,
               'description': form.description.value,
               'instructors': form.instructor_email.value.split(",") // This is a comma separated list of emails, each email must already be registered in the system
           })
        });
        const data = await response.json();
        //console.log(data);
        if (!response.ok){
            alert(data.error);
            return;
        }
        // We add the project to list, and reset the form
        this.projects.push({project_id: data.project.project_id, title: data.project.title, description: data.project.description, students: 0, instructors: data.project.instructors, students: 0});
        //console.log(this.projects);
        this.project_id = null;
        this.title = null;
        this.description = null;
        this.instructors = null;
    },
    async editProject(event){
        event.preventDefault();
        let form = document.getElementById("edit_project");
        const response = await fetch('http://localhost:5000/projects/' + this.project_id, {
           method: 'PUT',
           headers: {
               'Content-Type': 'application/json',
               'Authentication-Token': localStorage.getItem('token')
           },
            body: JSON.stringify({
            'title': form.title.value,
            'description': form.description.value,
            'instructors': form.instructor_email.value.split(",") // This is a comma separated list of emails, each email must already be registered in the system
            })
        });
        let result = await response.json();
        if (!response.ok){
            alert(result.error);
            return;
        }
        // Update the project in the list, have to go through all as we need to find the correct project
        for(let i = 0; i < this.projects.length; i++){
            if(this.projects[i].project_id == result.project.project_id){
                this.projects[i].title = result.project.title;
                this.projects[i].description = result.project.description;
                this.projects[i].instructors = result.project.instructors;
                this.projects[i].students = result.project.students;
                break;
            }
        }
        // If the project is currently being displayed, update the display
        let ele = document.getElementById(this.project_id);
        if(ele.classList.contains("clicked")){
            this.changePanel(this.project_id);
        }
        this.title = null;
        this.description = null;
        this.instructors = null;
        this.students = null;
        this.project_id = null;
    },
    async deleteProject(event){
        event.preventDefault();
        const response = await fetch('http://localhost:5000/projects/' + this.project_id, {
           method: 'DELETE',
           headers: {
               'Content-Type': 'application/json',
               'Authentication-Token': localStorage.getItem('token')
           }
        });
        let result = await response.json();
        if (!response.ok){
            alert(result.error);
            return;
        }
        // Remove the project from the list
        for (let i = 0; i < this.projects.length; i++){
            if (this.projects[i].project_id == this.project_id){
                this.projects.splice(i, 1);
            }
        }
        // If the project is the only one, reset the display
        if(this.projects.length == 0){
            this.changePanel(null);
        }
        // If the project is currently being displayed, update the display
        if(this.last_clicked == this.project_id){
            this.changeStuff(this.projects[0].project_id);
        }
    },
    changePanel(id){
        // Changes panel based on id, panel is the right side of the screen
        for (let i = 0; i < this.projects.length; i++){
                if (this.projects[i].project_id == id){
                    this.title = this.projects[i].title;
                    this.description = this.projects[i].description;
                    this.instructors = this.projects[i].instructors;
                    this.students = this.projects[i].students;
                    this.pie_chart = this.projects[i].pie_chart;
                    this.bar_chart = this.projects[i].bar_chart;
                }
            }
        if (this.showStats){
            let ele = document.getElementById("statsPanel");
            //ele.innerHTML = "<img src='data:image/png;base64,'" + this.pie_chart + " alt='Pie Chart'>" + "<img src='data:image/png;base64,'" + this.bar_chart + " alt='Bar Chart'>";
            //ele.innerHTML = "<img src='" + pieChart + "' alt='Pie Chart'>" + "<img src='" + barChart + "' alt='Bar Chart'>";
        } else {
            document.getElementById("projectTitle").innerHTML = this.title;
            document.getElementById("projectDescription").innerHTML = this.description;
            let instructor_string = "Instructors Assigned<br>";
            for (let i = 0; i < this.instructors.length; i++){
                instructor_string += this.instructors[i];
                if (i != this.instructors.length - 1){
                    instructor_string += "<br>";
                }
            }
            document.getElementById("projectInstructors").innerHTML = instructor_string;
        }
        this.title = null;
        this.description = null;
        this.instructors = null;
        this.pie_chart = null;
        this.bar_chart = null;
    },
    changeStuff(id){
        // Changes the clicked project, changes the panel to the right, and the color of the clicked project
        let ele = document.getElementById(id);
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
        this.changePanel(id); 
    },
    changeId(id, type){
        // Changes the id of the project to be edited or deleted, used for making things easier
        this.project_id = id;
        if(type == 0){
            for(let i = 0; i < this.projects.length; i++){
                if(this.projects[i].project_id == id){
                    let form = document.getElementById("edit_project");
                    form.title.value = this.projects[i].title;
                    form.description.value = this.projects[i].description;
                    let instructors = "";
                    for(let j = 0; j < this.projects[i].instructors.length; j++){
                        instructors += this.projects[i].instructors[j];
                        if(j != this.projects[i].instructors.length - 1){
                            instructors += ",";
                        }
                    }
                    form.instructor_email.value = instructors;
                }
            }
        }
    },
  },
  mounted(){
    //console.log(this.projects);
    if(this.projects.length > 0){
        this.changeStuff(this.projects[0].project_id);
    }else{
        this.changePanel(null);
    }
  }
}
</script>