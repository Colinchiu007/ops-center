import { createRouter, createWebHashHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { guest: true },
  },
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/feature-flags',
    name: 'FeatureFlags',
    component: () => import('../views/FeatureFlags.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('../views/Projects.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/audit-log',
    name: 'AuditLog',
    component: () => import('../views/AuditLog.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Initialize auth from localStorage
  if (!authStore.initialized) {
    authStore.init()
  }

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next('/login')
  } else if (to.meta.guest && authStore.isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router
