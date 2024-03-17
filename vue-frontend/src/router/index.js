import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Regis from '../views/RegisterView.vue'
import Login from '../views/LoginView.vue'
import BookingView from '../views/BookingView.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/register',
    name: 'register',
    component: Regis
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  
  },
  {
    path: '/booking',
    name: 'booking',
    component: BookingView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
