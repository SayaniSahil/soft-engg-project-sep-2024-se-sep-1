<script setup lang="ts">
defineProps<{
  milestones: Array<{
    id: number
    name: string
    status: 'pending' | 'completed' | 'overdue'
  }>
}>()
</script>

<template>
  <div class="list-group">
    <div v-for="milestone in milestones" :key="milestone.id" 
         class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
      {{ milestone.name }}
      <span :class="`badge bg-${milestone.status === 'completed' ? 'success' : 
                              milestone.status === 'overdue' ? 'danger' : 'warning'}`">
        {{ milestone.status }}
      </span>
    </div>
  </div>
</template>