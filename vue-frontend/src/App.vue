<script setup>
  import NavBar from './components/NavBar.vue';
</script>

<template>
  <!-- Need Logic here -->
   <!-- <main :class="[this.$route.meta.hideNavBar ? 'bg-white' : 'bg-light']" :style="[
    { 'min-height': $route.meta.hideNavBar ? '100vh' : 'calc(100vh - 75px)' },
    { 'margin-top': $route.meta.hideNavBar ? '0' : '74px' },
    ]"/> -->
  <NavBar/>
  <RouterView />
</template>



<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #FAFAFA;
}
</style>

<!-- <script>
import { ref, watch } from 'vue';

import { useSession } from 'vue-session';

const shouldShowNavbar = ref(true);
const session = useSession();

// Set session data
session.set('isLoggedIn', true);

// Get session data
const isLoggedIn = session.get('isLoggedIn');

watch($route, (to) => {
  shouldShowNavbar.value = to.name !== 'Login' && !to.meta.hideNavBar;
});

</script> -->
