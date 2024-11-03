<template>
    <h1>Project List Component</h1>
    <div class="project-container">
      <div class="project-list">
        <h3>This is the project list</h3>
        <!-- Check if there are no projects -->
        <div v-if="projects.length === 0" class="empty-card">
          <h2>No Projects Available</h2>
          <p>The project list is empty.</p>
        </div>
        <div v-else>
          <div
            class="card"
            v-for="(project, index) in projects"
            :key="index"
            @click="selectProject(project)"
          >
            <h2>{{ project.name }}</h2>
            <div class="card-content"> <!-- Optional wrapper for scrollable content -->
              <ul>
                <li v-if="project.students.length > 0"> <!-- Display only if there are students -->
                  <strong>Name:</strong> {{ project.students[0].name }} <br>
                  <strong>Email:</strong> {{ project.students[0].email }}
                </li>
                <li v-else>
                  <strong>No students available</strong>
                </li>
              </ul>
            </div>
            <button @click.stop="removeProject(index)" class="delete-button">Delete</button>
          </div>
        </div>
      </div>
      <div class="separator"></div> <!-- Vertical separator -->
      <div class="project-details" v-if="selectedProject">
        <h2>{{ selectedProject.name }} Details</h2>
        <p>{{ selectedProject.details }}</p>
        <p>{{ selectedProject.description }}</p> <!-- Dynamic paragraph -->
        
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ProjectList',
    data() {
      return {
        projects: [
          {
            name: 'Project 1',
            details: 'This is a detailed description of Project 1.',
            description: 'Dustin is the best striker in the lightweight division.',
            students: [
              { name: 'Dustin', email: 'Dustindiamond@ufc.com' },
              // More students can be added if needed
            ]
          },
          {
            name: 'Project 2',
            details: 'This is a detailed description of Project 2.',
            description: 'A former kickboxer and now the light heavyweight champion of the world.',
            students: [
              { name: 'Alex', email: 'alexthepoatan@ufc.com' },
              // More students can be added if needed
            ]
          },
          // Add more projects here as needed
        ],
        selectedProject: null, // Store the selected project for details view
      }
    },
    methods: {
      removeProject(index) {
        if (confirm("Are you sure you want to delete this project?")) {
          this.projects.splice(index, 1);
          if (this.selectedProject === this.projects[index]) {
            this.selectedProject = null; // Clear selection if deleted
          }
        }
      },
      selectProject(project) {
        this.selectedProject = project;
      }
    }
  }
  </script>
  
  <style>
  .project-container {
    display: flex; /* Use flex to align project list and details side by side */
    width: 100%; /* Full width of the container */
    height: 100vh; /* Full height of the viewport */
  }
  
  .project-list {
    flex: 0 0 350px; /* Fixed width for the project list */
    display: flex;
    flex-direction: column;
    gap: 16px;
    height: calc(100vh - 40px); /* Adjust the height to account for margins or other elements */
    overflow-y: auto; /* Allow vertical scrolling */
  }
  
  .project-details {
    flex: 1; /* Take up the remaining space for project details */
    padding: 16px;
    background-color: #f9f9f9;
    border-left: 1px solid #ddd;
    overflow-y: auto; /* Allow scrolling if content exceeds available height */
    height: calc(100vh - 40px); /* Match the height of the project list */
  }
  
  .separator {
    width: 2px; /* Width of the vertical line */
    background-color: #ddd; /* Color of the vertical line */
    height: auto; /* Height will automatically adjust */
    margin: 0 16px; /* Space around the separator */
  }
  
  .card {
    width: 100%; /* Make cards fill the project list's width */
    padding: 16px;
    background-color: #add8e6;
    border: 1px solid #ddd;
    border-radius: 8px;
    text-align: left;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-size: 16px;
    position: relative;
    cursor: pointer; /* Change cursor to indicate clickable */
    color: #000; /* Set text color to black */
}

  
  .card:hover {
    background-color: #e9ecef; /* Change color on hover for better UX */
  }
  
  .delete-button {
    margin-top: 8px;
    padding: 4px 8px;
    color: #fff;
    background-color: #e74c3c;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .delete-button:hover {
    background-color: #c0392b;
  }
  
  .empty-card {
    width: 100%; /* Full width of the container */
    padding: 16px;
    background-color: #f0f0f0; /* Background color for empty card */
    border: 1px solid #ddd;
    border-radius: 8px;
    text-align: center; /* Center text in the card */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-size: 16px;
  }
  </style>
  