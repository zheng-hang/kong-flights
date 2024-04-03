import { createRouter, createWebHistory } from 'vue-router'
import Regis from '../views/RegisterView.vue'
import Login from '@/components/LoginPage.vue'
import SearchFlights from '../views/SearchFlights.vue'
import MyFlights from '../views/MyFlights.vue'
import BookingView from '../views/BookingView.vue'
import FlightsResult from '@/components/FlightsResult.vue'
import BookingSeatsView from '@/views/BookingSeatsView.vue'
// import FlightsResult from '@/components/FlightsResult.vue'
// import PaymentPage from '@/components/PaymentPage.vue'


const routes = [
  {
    path: '/',
    name: 'SearchFlights',
    component: SearchFlights
  },
  {
    path: '/register',
    name: 'register',
    component: Regis,

  },
  {
    path: '/login',
    name: 'login',
    component: Login
  
  },
  {
    path: '/searchFlights',
    name: 'SearchFlights',
    component: SearchFlights
  
  },
  {
    path: '/MyFlights',
    name: 'MyFlights',
    component: MyFlights
  
  },
  {
    path: '/booking',
    name: 'booking',
    component: BookingView
  },
  {
    path: '/seatsbooking',
    name: 'seatsbooking',
    component: BookingSeatsView
  },
  {
    path: '/flightsresult',
    name: 'flightsresult',
    component: FlightsResult
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
