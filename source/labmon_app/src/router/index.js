import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Collection from '../views/Collection.vue'
import Profile from '../views/Profile.vue'
import AdminPanel from '../views/AdminPanel.vue'
import Encounter from '../views/Encounter.vue'
import { useEncounterStore } from '../stores/encunterStore'
import Inventory from '../views/Inventory.vue'


const routes = [
  { path: '/', name: 'Home', component: Home, meta: { userOnly: true } },
  { path: '/login', name: 'Login', component: Login, meta: { guestOnly: true } },
  { path: '/register', name: 'Register', component: Register, meta: { guestOnly: true } },
  { path: '/collection', name: 'Collection', component: Collection, meta: { userOnly: true } },
  { path: '/profile', name: 'Profile', component: Profile, meta: { userOnly: true } },
  { path: '/admin_panel', name: 'Admin Panel', component: AdminPanel, meta: { adminOnly: true } },
  { path: '/encounter', name: 'Encounter', component: Encounter, meta: { isEncounterActive: true } },
  { path: '/inventory', name: 'Inventory', component: Inventory, meta: { userOnly: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const encounterStore = useEncounterStore()

  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return next('/')
  }

  if (to.meta.isEncounterActive && !encounterStore.isEncounterActive) {
    return next('/')
  }

  if (to.meta.userOnly && authStore.isAuthenticated === false) {
    return next('/login')
  }

  if (to.meta.adminOnly && authStore.isAdmin === false) {
    return next('/')
  }

  next()
})

export default router
