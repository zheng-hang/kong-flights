<template>
    <!-- <div class="home">
      <img alt="Vue logo" src="../assets/logo.png">
      <HelloWorld msg="Welcome to Your Vue.js App"/>
    </div> -->
    Read from microservice JSON results: {{ flights }}
    <div style="background-color: #FAFAFA;margin:0;padding:0;text-align: left;">
      <!-- Nav -->
      <!-- <nav style="margin:0; box-shadow: 0 2px 4px 0 rgba(0,0,0,.2); background-color: white; height: 65px;display: flex;align-items: center;justify-content: space-between;">
        <div>
          <img src="@/assets/SMOOth Airlines Logo - Flat.png" style="height: 50px;">
        </div>
        <div>
          <router-link to="/SearchFlights" style="margin: 10px; text-decoration: none; color: blue">Search Flights</router-link> 
          <router-link to="/MyFlights" style="margin: 10px; text-decoration: none;">My Flights</router-link> 
          <router-link to="/MyPayments" style="margin: 10px; text-decoration: none;">My Payment</router-link>
        </div>
        <div>
          <router-link to="/signOut" style="text-decoration: none;">Sign Out</router-link>
        </div>
      </nav> -->
      <!-- <div style="margin:0; box-shadow: 0 2px 4px 0 rgba(0,0,0,.2); 
          background-color: white; height: 65px;display: flex;align-items: center;justify-content: center;">
          <ul style="list-style-type: none; text-align: center;">
              <li style="display: inline; margin: 10px; font-weight: bold;">Search Flights</a></li>
              <li style="display: inline; margin: 10px;">My Flights</a></li>
              <li style="display: inline; margin: 10px;">My Payment</a></li>
          </ul>
      </div> -->
  
      <!-- Title -->
      <div style="text-align: left; margin-left: 60px; margin-top: 20px">
          <h3>Welcome to World Class</h3>
          Where Every Flight is a Seamless Experience
      </div>
  
      <!-- Search -->
      <div id="SearchBox" style="padding-right: 25px; padding-left: 25px; padding-top: 20px;">
          <h5>Hey there, where can we take you?</h5> <br/>
          <div class="row">
              <div class="col-4">
                  <div class="input-group mb-3">
                      <div class="input-group-prepend">
                          <span class="input-group-text">From</span>
                      </div>
                      <input type="text" class="form-control" placeholder="Your current location" value="Singapore">
                  </div>
              </div>
              <div class="col-4">
                  <div class="input-group mb-3">
                      <div class="input-group-prepend">
                          <span class="input-group-text">To</span>
                      </div>
                      <input type="text" class="form-control" placeholder="Your Destination">
                  </div>
              </div>
              <div class="col-4">
                  <div class="input-group mb-3">
                      <div class="input-group-prepend">
                          <span class="input-group-text">Departure Date</span>
                      </div>
                      <input class="form-control" type="date" id="departureDate" name="departureDate">
                  </div>
              </div>
          </div>
          <div class="row" style="margin-top: 5px;">
              <div class="d-flex justify-content-end">
                  <button type="button" class="btn btn-primary col-2" @click="searchFlights">Search Flights</button>
              </div>           
          </div>
      </div>
  
      <!-- Trending Places -->
      <div style="text-align: left; margin-left: 60px; margin-top: 40px">
          <h4>Trending Places for You</h4>
      </div>
      <div class="row row-cols-5" style="margin-left: 60px; margin-right: 60px; padding-right: 25px; padding-left: 25px; padding-top: 20px;">
          <div class="col">
              <div class="card" style="width: 250px; padding: 0">
                  <img class="card-img-top" style="width: 250px; height:150px" src="https://assets.traveltriangle.com/blog/wp-content/uploads/2016/02/Petronas-Twin-Towers-in-Kuala-Lumpur.jpg">
                  <div class="card-body">
                    <div class="card-text">
                      <h5>Kuala Lumpur</h5>
                      Economy
                      | From <span style="font-weight: bold;">SGD 106</span>
                      <p>
                          <small class="text-muted">1 hour ago</small>
                      </p>
                    </div>
                  </div>
              </div>
          </div>
          <div class="col">
              <div class="card" style="width: 250px; padding: 0">
                  <img class="card-img-top" style="width: 250px; height:150px" src="https://www.kkday.com/en/blog/wp-content/uploads/kr_Korea_Seoul_Bukchon-Hanok-Village_Ashutterstock_309071426.jpg">
                  <div class="card-body">
                    <div class="card-text">
                      <h5>Seoul</h5>
                      Economy
                      | From <span style="font-weight: bold;">SGD 269</span>
                      <p>
                          <small class="text-muted">3 hours ago</small>
                      </p>
                    </div>
                  </div>
              </div>
          </div>
          <div class="col">
              <div class="card" style="width: 250px; padding: 0">
                  <img class="card-img-top" style="width: 250px; height:150px" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRRyJK21jR5V9xC77MDZo9KYMeB5wkNXpAt6OlUQCrgg&s">
                  <div class="card-body">
                    <div class="card-text">
                      <h5>Bali</h5>
                      Economy
                      | From <span style="font-weight: bold;">SGD 140</span>
                      <p>
                          <small class="text-muted">1 day ago</small>
                      </p>
                    </div>
                  </div>
              </div>
          </div>
          <div class="col">
              <div class="card" style="width: 250px; padding: 0">
                  <img class="card-img-top" style="width: 250px; height:150px" src="https://content.r9cdn.net/rimg/dimg/39/86/ae1975d6-city-26939-15516fe0259.jpg?width=1366&height=768&xhint=2069&yhint=1666&crop=true">
                  <div class="card-body">
                    <div class="card-text">
                      <h5>Frankfurt</h5>
                      Economy
                      | From <span style="font-weight: bold;">SGD 1,099</span>
                      <p>
                          <small class="text-muted">1 day ago</small>
                      </p>
                    </div>
                  </div>
              </div>
          </div>
          <div class="col d-flex align-items-center">
              <div>
                  <h5 class="text-primary"><a href="#">View More</a> <i class="fa-solid fa-arrow-right fa-xl"></i></h5>
              </div>
          </div>
      </div>
    </div>
</template>
  
<style>
      #SearchBox {
          height: 200px;
          margin-top: 20px;
          margin-left: 60px;
          margin-right: 60px;
          background: #fff;
          border-radius: 20px;
          box-shadow: 1px 5px 10px 1px rgba(0, 0, 0, 0.2); 
      }
</style>
<script>
import axios from 'axios';
  export default {
    async mounted() {
      // Load Bootstrap CSS
      this.loadCss('https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css');
  
      // Load Bootstrap Datepicker Plugin CSS and JavaScript
      //this.loadScript('https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.4.1/js/bootstrap-datepicker.min.js');
      this.loadCss('https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.4.1/css/bootstrap-datepicker3.css');
  
      // Load Font Awesome CSS and JavaScript
      this.loadCss('path/to/font-awesome/css/font-awesome.min.css');
      this.loadScript('https://kit.fontawesome.com/5ca5b3f212.js');
    },
    data: function(){
      return {
        flights: ''
      }
    },
    methods: {
      loadCss(url) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = url;
        if (url.includes('bootstrap')) {
          link.integrity = 'sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx';
          link.crossOrigin = 'anonymous';
        }
        document.head.appendChild(link);
      },
      loadScript(url) {
        const script = document.createElement('script');
        script.src = url;
        if (url.includes('kit.fontawesome')) {
          script.crossOrigin = 'anonymous';
        }
        script.async = true;
        document.body.appendChild(script);
      },
      searchFlights() {
        axios.get('http://localhost:5001/flight')
          .then(response => {
            // Handle the response data here
            this.flights = response.data; // flight data
          })
          .catch(error => {
            // Handle errors here
            this.flights = error;
            console.error('There was an error fetching flight data:', error);
        });
      }
    }
  };
</script>