<template>
  <div class="results">
    <h1>Results</h1>
    <p>Coming soon...</p>
    <router-link to="/model-training">← Back to Model Training</router-link>
  </div>
</template>

<script>
export default {
  name: 'Results'
}
</script>

<style scoped>
.results {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  gap: 1rem;
}
</style>
