import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Regis from '../views/RegisterView.vue'
import Login from '../views/LoginView.vue'
import SearchFlights from '../views/SearchFlights.vue'
import MyFlights from '../views/MyFlights.vue'

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
    path: '/SearchFlights',
    name: 'SearchFlights',
    component: SearchFlights
  
  },
  {
    path: '/MyFlights',
    name: 'MyFlights',
    component: MyFlights
  
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
