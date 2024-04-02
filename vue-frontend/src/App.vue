<template>
  <!-- Need Logic here -->
   <!-- <main :class="[this.$route.meta.hideNavBar ? 'bg-white' : 'bg-light']" :style="[
    { 'min-height': $route.meta.hideNavBar ? '100vh' : 'calc(100vh - 75px)' },
    { 'margin-top': $route.meta.hideNavBar ? '0' : '74px' },
    ]"/> -->
  <NavBar v-if="!this.$route.meta.hideNavBar"/>
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

<script>
import NavBar from './components/NavBar.vue';
export default {
  components: {
    NavBar
  },
  data() {
    return {
      isLoggedIn: false,
      shouldShowNavbar: true
    };
  },
  watch: {
    $route(to) {
      this.shouldShowNavbar = to.name !== "Login";
    }
  }
}
</script>
