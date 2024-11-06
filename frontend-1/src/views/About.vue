<script setup lang="ts">
import CardComponent from '../components/CardComponent.vue'
</script>

<template>
  <div class="row">
    <div class="col-12 mb-4">
      <h1>About Us</h1>
      <p class="lead">Learn more about our project and team.</p>
    </div>
    
    <div class="col-md-6 mb-4">
      <CardComponent
        title="Our Mission"
        text="We strive to create beautiful and functional web applications using modern technologies like Vue.js and Bootstrap."
      >
        <button class="btn btn-outline-primary">Read More</button>
      </CardComponent>
    </div>
    
    <div class="col-md-6 mb-4">
      <CardComponent
        title="Our Team"
        text="We are a group of passionate developers dedicated to building great user experiences."
      >
        <button class="btn btn-outline-success">Meet the Team</button>
      </CardComponent>
    </div>
  </div>
</template>