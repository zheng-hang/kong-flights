<template>
    <nav style="margin:0; box-shadow: 0 2px 4px 0 rgba(0,0,0,.2); background-color: white; height: 65px;display: flex;align-items: center;justify-content: space-between;">
    <div>
      <img src="@/assets/SMOOth Airlines Logo - Flat.png" style="height: 50px;">
    </div>
    <div>
      <router-link to="/SearchFlights" class="header" style="margin: 10px; text-decoration: none;">Search Flights</router-link> 
      <router-link to="/MyFlights" class="header" style="margin: 10px; text-decoration: none;">My Flights</router-link> 
    </div>
    <div v-if="!isLoggedIn">
      <router-link to="/login" style="text-decoration: none;">Sign In</router-link>
    </div>
    <div v-else>
      <router-link to="/signOut" style="text-decoration: none;"><i class="fa fa-user" aria-hidden="true"></i></router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: true
    }
  },
}
</script>

<style scoped>
    nav {
    padding: 30px;
    }

    nav a {
    font-weight: bold;
    color: #2c3e50;
    }

    nav a.router-link-exact-active {
    color: #42b983;
    }

    /* Doesn't work very well - green color will remain  */
    .header:focus{
    color: blue;
    }
</style>