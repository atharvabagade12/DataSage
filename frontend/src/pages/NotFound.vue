<template>
  <div class="not-found">
    <div class="not-found-content">
      <div class="error-icon">🤖</div>
      <h1>404 - Page Not Found</h1>
      <p>The page you're looking for doesn't exist or has been moved.</p>
      <router-link to="/dashboard" class="back-btn">
        ← Back to Dashboard
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.not-found-content {
  text-align: center;
  max-width: 500px;
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

h1 {
  font-size: 2rem;
  color: #667eea;
  margin-bottom: 1rem;
}

p {
  color: #b3b3d1;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  transition: transform 0.2s ease;
}

.back-btn:hover {
  transform: translateY(-2px);
}
</style>
