<template>
  <div class="app-container">
    <nav class="sidebar">
      <h3>Navigation</h3>
      <button class="nav-button" @click="showProjectList">Project List</button>
      <!-- You can add more buttons for additional navigation -->
    </nav>
    <div class="main-content">
      <ProjectList v-if="currentComponent === 'ProjectList'" />
      <!-- Add more components conditionally here -->
    </div>
  </div>
</template>

<script>
import ProjectList from './components/ProjectList.vue'; // Adjusted component import

export default {
  name: 'App',
  components: {
    ProjectList,
  },
  data() {
    return {
      currentComponent: null, // To track the currently displayed component
    };
  },
  methods: {
    showProjectList() {
      this.currentComponent = 'ProjectList'; // Set the current component to ProjectList
    },
  },
};
</script>

<style>
.app-container {
  display: flex; /* Use flex to create a sidebar and main content layout */
  height: 100vh; /* Full height of the viewport */
}

.sidebar {
  flex: 0 0 200px; /* Fixed width for the sidebar */
  background-color: #f8f9fa; /* Light background for the sidebar */
  padding: 16px;
  border-right: 1px solid #ddd; /* Right border for separation */
}

.nav-button {
  width: 100%; /* Make the button full width */
  padding: 10px; /* Add padding for better appearance */
  margin-bottom: 8px; /* Space between buttons */
  background-color: #007bff; /* Primary color for the button */
  color: white; /* Text color */
  border: none; /* No border */
  border-radius: 4px; /* Rounded corners */
  cursor: pointer; /* Change cursor to indicate clickable */
}

.nav-button:hover {
  background-color: #0056b3; /* Darker shade on hover */
}

.main-content {
  flex: 1; /* Take the remaining space */
  padding: 16px;
}
</style>
