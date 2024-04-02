<template>
  <!-- <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/register">Register</router-link> |
    <router-link to="/login">Login</router-link>
  </nav> -->
  <nav style="margin:0; box-shadow: 0 2px 4px 0 rgba(0,0,0,.2); background-color: white; height: 65px;display: flex;align-items: center;justify-content: space-between;">
    <div>
      <img src="@/assets/SMOOth Airlines Logo - Flat.png" style="height: 50px;">
    </div>
    <div>
      <router-link to="/SearchFlights" class="header" style="margin: 10px; text-decoration: none;">Search Flights</router-link> 
      <router-link to="/MyFlights" class="header" style="margin: 10px; text-decoration: none;">My Flights</router-link> 
    </div>
    <div>
      <router-link to="/signOut" style="text-decoration: none;">Sign Out</router-link>
    </div>
  </nav>
  <router-view/>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

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
