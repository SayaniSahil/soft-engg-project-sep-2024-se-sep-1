<script setup lang="ts">
import CardComponent from '../components/CardComponent.vue'
</script>

<template>
  <div class="row">
    <div class="col-12 mb-4">
      <h1>Welcome to Vue Bootstrap</h1>
      <p class="lead">This is a sample project using Vue 3, Bootstrap 5, and TypeScript.</p>
    </div>
    
    <div class="col-md-4 mb-4">
      <CardComponent
        title="Feature One"
        text="This is a sample feature card showcasing Bootstrap integration."
        imgSrc="https://picsum.photos/300/200?random=1"
      >
        <button class="btn btn-primary">Learn More</button>
      </CardComponent>
    </div>
    
    <div class="col-md-4 mb-4">
      <CardComponent
        title="Feature Two"
        text="Another example of a reusable card component with custom content."
        imgSrc="https://picsum.photos/300/200?random=2"
      >
        <button class="btn btn-success">Explore</button>
      </CardComponent>
    </div>
    
    <div class="col-md-4 mb-4">
      <CardComponent
        title="Feature Three"
        text="Demonstrating the flexibility of our card component system."
        imgSrc="https://picsum.photos/300/200?random=3"
      >
        <button class="btn btn-info">Details</button>
      </CardComponent>
    </div>
  </div>
</template>