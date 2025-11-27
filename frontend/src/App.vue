<template>
  <div id="app">
    <NuxtPage />
    <Toast />
  </div>
</template>

<script setup>
import Toast from '~/components/Toast.vue'
</script>

<style>
@import './assets/styles/design-tokens.css';

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-primary);
  background: var(--color-background);
  color: var(--color-text-primary);
}

#app {
  min-height: 100vh;
}
</style>
