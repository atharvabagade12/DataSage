<template>
  <nav class="global-navbar">
    <div class="nav-left">
      <div class="logo" @click="navigateTo('/')">
        <div class="brand-logo">
          <img src="@/assets/logo.jpeg" alt="DataSage Logo" class="logo-img">
        </div>
        <div class="brand-text">DataSage</div>
      </div>
    </div>
    
    <div class="nav-center">
      <div class="nav-links">
        <NuxtLink to="/dashboard" class="nav-link" :class="{ active: $route.path === '/dashboard' && (!$route.query.tab || $route.query.tab === 'dashboard') }">Dashboard</NuxtLink>
        <NuxtLink to="/dashboard?tab=projects" class="nav-link" :class="{ active: $route.query.tab === 'projects' }">Projects</NuxtLink>
        <NuxtLink to="/dashboard?tab=analytics" class="nav-link" :class="{ active: $route.query.tab === 'analytics' }">Analytics</NuxtLink>
        <NuxtLink to="/dashboard?tab=models" class="nav-link" :class="{ active: $route.query.tab === 'models' }">Models</NuxtLink>
      </div>
    </div>
    
    <div class="nav-right">
      <div class="user-section">
        <div class="user-avatar" @click="showUserMenu = !showUserMenu">{{ userInitials }}</div>
        <div class="user-info">
          <span class="user-name">{{ userName }}</span>
        </div>
        <div class="nav-actions">
            <button @click="logout" class="logout-btn" title="Logout">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9"/>
                </svg>
            </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const showUserMenu = ref(false)

const userName = computed(() => {
  try {
    const userString = sessionStorage.getItem('user') || localStorage.getItem('user')
    const user = JSON.parse(userString || '{}')
    return user.username || user.name || 'Data Scientist'
  } catch {
    return 'Data Scientist'
  }
})

const userInitials = computed(() => {
  const name = userName.value
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2) || 'DS'
})

const navigateTo = (path) => router.push(path)
const logout = () => { sessionStorage.clear(); localStorage.clear(); navigateTo('/login') }
</script>

<style scoped>
.global-navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 2rem;
  background: rgba(11, 11, 26, 0.95);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  position: sticky;
  top: 0;
  z-index: 1001;
  height: 64px;
}

.logo { display: flex; align-items: center; gap: 10px; cursor: pointer; }

.brand-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.2);
  overflow: hidden;
}

.logo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center;
  display: block;
}
.brand-text { 
    font-size: 1.25rem; 
    font-weight: 800; 
    letter-spacing: -0.5px; 
    background: linear-gradient(to right, #667eea, #764ba2); 
    -webkit-background-clip: text; 
    background-clip: text; 
    -webkit-text-fill-color: transparent; 
}

.nav-links { 
    display: flex; 
    background: rgba(255, 255, 255, 0.03); 
    padding: 3px; 
    border-radius: 12px; 
    border: 1px solid rgba(255, 255, 255, 0.05); 
}
.nav-link { 
    text-decoration: none;
    color: #6a6a8a; 
    padding: 8px 18px; 
    border-radius: 9px; 
    cursor: pointer; 
    font-weight: 600; 
    font-size: 0.9rem;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); 
}
.nav-link.active { 
    background: rgba(102, 126, 234, 0.1); 
    color: #667eea; 
    box-shadow: inset 0 0 10px rgba(102, 126, 234, 0.1); 
}
.nav-link:hover:not(.active) { color: #ffffff; }

.user-section { display: flex; align-items: center; gap: 0.75rem; }
.user-avatar { 
    width: 32px; 
    height: 32px; 
    border-radius: 50%; 
    background: linear-gradient(135deg, #667eea, #764ba2); 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    font-weight: 800; 
    font-size: 0.75rem; 
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3); 
    cursor: pointer;
}
.user-info { display: flex; flex-direction: column; }
.user-name { font-weight: 600; font-size: 0.85rem; color: #b3b3d1; }

.logout-btn { 
    background: none; 
    border: none; 
    color: #4a4a6a; 
    cursor: pointer; 
    transition: color 0.2s; 
    display: flex;
    align-items: center;
    padding: 5px;
}
.logout-btn:hover { color: #ff5757; }

@media (max-width: 768px) {
  .nav-center { display: none; }
  .user-info { display: none; }
}
</style>
