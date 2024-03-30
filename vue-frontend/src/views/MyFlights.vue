<template>
    <div style="background-color: #FAFAFA;margin:0;padding:0;text-align: left;">
      <!-- Nav -->
      <!-- <nav style="margin:0; box-shadow: 0 2px 4px 0 rgba(0,0,0,.2); background-color: white; height: 65px;display: flex;align-items: center;justify-content: space-between;">
        <div>
          <img src="@/assets/SMOOth Airlines Logo - Flat.png" style="height: 50px;">
        </div>
        <div>
          <router-link to="/SearchFlights" style="margin: 10px; text-decoration: none;">Search Flights</router-link> 
          <router-link to="/MyFlights" style="margin: 10px; text-decoration: none; color: blue">My Flights</router-link> 
          <router-link to="/MyPayments" style="margin: 10px; text-decoration: none;">My Payment</router-link>
        </div>
        <div>
          <router-link to="/signOut" style="text-decoration: none;">Sign Out</router-link>
        </div>
      </nav> -->

      <!-- Title -->
        <div style="text-align: left; margin-left: 60px; margin-top: 20px">
            <h3>My Flight Bookings</h3>
            View all flights booked here
        </div>

        <!-- Upcoming Flights -->
        <div v-if="toggle == 'upcoming'">
            <div class="row" style="margin-left: 45px; margin-right: 45px; margin-top: 20px">
                <div class="d-flex justify-content-between">
                    <div class="col">
                        <button type="button" class="btn btn-primary" v-on:click="toggle = 'upcoming'" style="border-radius: 20px; width: 120px; margin-right: 10px">Upcoming</button>
                        <button type="button" class="btn btn-outline-primary" v-on:click="toggle = 'past'" style="border-radius: 20px; width: 70px;">Past</button>
                    </div>
                    <div class="col input-group mb-3">
                        <input type="text" class="form-control" placeholder="Search a booking...">
                        <button class="btn btn-outline-secondary" type="button" id="button-addon2">Search</button>
                    </div>
                </div>    
            </div>
            
            <!-- Display all bookings -->
            <div class="row" style="display:flex; justify-content: center; margin:250px; margin-top: 20px;">
                <!--Booking 1-->
                <table class="table table-bordered" style="border-style:solid; border-color: #0D6FE5; border-width: thin;">
                    <thead style="background-color: #0DB4F3;">
                    <tr>
                        <th class="d-flex justify-content-between" style="padding: 20px;padding-bottom:10px;">
                            <h6 style="font-weight: bold">1. SQ216 | Singapore to Tokyo</h6>
                            <h6 style="font-weight: bold">Economy | <a href="#" style="color:black">Change Seat</a></h6>
                        </th>
                    </tr>
                    </thead>
                    <tbody style="background-color: white;">
                    <tr>
                        <td style="padding: 40px; padding-top:20px;">
                            <!-- Add flight duration -->
                            <span style="font-weight: bold;">6 hr 40 min</span>
                            <div class="row" style="margin-top: 15px">
                                <!-- Departure -->
                                <div class="col-3">
                                    <p class="text-primary" style="font-weight: bold;">DEPARTURE</p>
                                    <h3>SIN 08:05</h3>
                                    <p>
                                        <span style="font-weight: bold;">Singapore</span><br/>
                                        Thursday, 28 Mar 2024
                                    </p>
                                </div>
                                <div class="col-1 d-flex align-items-center justify-content-start">
                                    <!-- <font-awesome-icon icon="plane" /> -->
                                    <i class="fa-solid fa-plane fa-2xl"></i>
                                </div>
                                <!-- Arrival -->
                                <div class="col-5">
                                    <p class="text-primary" style="font-weight: bold;">ARRIVAL</p>
                                    <h3>NRT 15:45</h3>
                                    <p>
                                        <span style="font-weight: bold;">Tokyo</span><br/>
                                        Thursday, 28 Mar 2024
                                    </p>
                                </div>
                                <!-- Others -->
                                <div class="col-3">
                                    <!-- Status -->
                                    <p class="text-primary"><span style="font-weight: bold;">STATUS:</span> CONFIRMED</p>
                                    <p>
                                        <span style="font-weight: bold;">Singapore Airlines | SQ216</span><br/>
                                        Airbus Industrie A380-800
                                    </p>
                                    <i class="fa-solid fa-suitcase"></i> Checked Baggage: -
                                </div>
                            </div>
                        </td>
                    </tr>
                    </tbody>
                </table>

                <!--Booking 2-->
                
            </div>
        </div>
        <!-- Past Flights -->
        <div v-if="toggle == 'past'">
            <div class="row" style="margin-left: 45px; margin-right: 45px; margin-top: 20px">
                <div class="d-flex justify-content-between">
                    <div class="col">
                        <button type="button" class="btn btn-outline-primary" v-on:click="toggle = 'upcoming'" style="border-radius: 20px; width: 120px; margin-right: 10px">Upcoming</button>
                        <button type="button" class="btn btn-primary" v-on:click="toggle = 'past'" style="border-radius: 20px; width: 70px;">Past</button>
                    </div>
                    <div class="col input-group mb-3">
                        <input type="text" class="form-control" placeholder="Search a booking...">
                        <button class="btn btn-outline-secondary" type="button" id="button-addon2">Search</button>
                    </div>
                </div>
            </div>
            
            <!-- Display all bookings -->
            <div class="row" style="display:flex; justify-content: center; margin:250px; margin-top: 20px;">
                <!--Booking 1-->
                <table class="table table-bordered" style="border-style:solid; border-color: #0D6FE5; border-width: thin;">
                    <thead style="background-color: #0DB4F3;">
                    <tr>
                        <th class="d-flex justify-content-between" style="padding: 20px;padding-bottom:10px;">
                            <h6 style="font-weight: bold">1. SQ216 | Singapore to Tokyo</h6>
                            <h6 style="font-weight: bold">Economy | <a href="#" style="color:black">Change Seat</a></h6>
                        </th>
                    </tr>
                    </thead>
                    <tbody style="background-color: white;">
                    <tr>
                        <td style="padding: 40px; padding-top:20px;">
                            <!-- Add flight duration -->
                            <span style="font-weight: bold;">6 hr 40 min</span>
                            <div class="row" style="margin-top: 15px">
                                <!-- Departure -->
                                <div class="col-3">
                                    <p class="text-primary" style="font-weight: bold;">DEPARTURE</p>
                                    <h3>SIN 08:05</h3>
                                    <p>
                                        <span style="font-weight: bold;">Singapore</span><br/>
                                        Thursday, 28 Mar 2024
                                    </p>
                                </div>
                                <div class="col-1 d-flex align-items-center justify-content-start">
                                    <!-- <font-awesome-icon icon="plane" /> -->
                                    <i class="fa-solid fa-plane fa-2xl"></i>
                                </div>
                                <!-- Arrival -->
                                <div class="col-5">
                                    <p class="text-primary" style="font-weight: bold;">ARRIVAL</p>
                                    <h3>NRT 15:45</h3>
                                    <p>
                                        <span style="font-weight: bold;">Tokyo</span><br/>
                                        Thursday, 28 Mar 2024
                                    </p>
                                </div>
                                <!-- Others -->
                                <div class="col-3">
                                    <!-- Status -->
                                    <p class="text-primary"><span style="font-weight: bold;">STATUS:</span> CONFIRMED</p>
                                    <p>
                                        <span style="font-weight: bold;">Singapore Airlines | SQ216</span><br/>
                                        Airbus Industrie A380-800
                                    </p>
                                    <i class="fa-solid fa-suitcase"></i> Checked Baggage: -
                                </div>
                            </div>
                        </td>
                    </tr>
                    </tbody>
                </table>

                <!--Booking 2-->
                <table class="table table-bordered" style="border-style:solid; border-color: #0D6FE5; border-width: thin;">
                    <thead style="background-color: #0DB4F3;">
                    <tr>
                        <th class="d-flex justify-content-between" style="padding: 20px;padding-bottom:10px;">
                            <h6 style="font-weight: bold">2. SQ216 | Singapore to Tokyo</h6>
                            <h6 style="font-weight: bold">Economy | <a href="#" style="color:black">Change Seat</a></h6>
                        </th>
                    </tr>
                    </thead>
                    <tbody style="background-color: white;">
                    <tr>
                        <td style="padding: 40px; padding-top:20px;">
                            <!-- Add flight duration -->
                            <span style="font-weight: bold;">6 hr 40 min</span>
                            <div class="row" style="margin-top: 15px">
                                <!-- Departure -->
                                <div class="col-3">
                                    <p class="text-primary" style="font-weight: bold;">DEPARTURE</p>
                                    <h3>SIN 08:05</h3>
                                    <p>
                                        <span style="font-weight: bold;">Singapore</span><br/>
                                        Thursday, 28 Mar 2024
                                    </p>
                                </div>
                                <div class="col-1 d-flex align-items-center justify-content-start">
                                    <!-- <font-awesome-icon icon="plane" /> -->
                                    <i class="fa-solid fa-plane fa-2xl"></i>
                                </div>
                                <!-- Arrival -->
                                <div class="col-5">
                                    <p class="text-primary" style="font-weight: bold;">ARRIVAL</p>
                                    <h3>NRT 15:45</h3>
                                    <p>
                                        <span style="font-weight: bold;">Tokyo</span><br/>
                                        Thursday, 28 Mar 2024
                                    </p>
                                </div>
                                <!-- Others -->
                                <div class="col-3">
                                    <!-- Status -->
                                    <p class="text-primary"><span style="font-weight: bold;">STATUS:</span> CONFIRMED</p>
                                    <p>
                                        <span style="font-weight: bold;">Singapore Airlines | SQ216</span><br/>
                                        Airbus Industrie A380-800
                                    </p>
                                    <i class="fa-solid fa-suitcase"></i> Checked Baggage: -
                                </div>
                            </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>
  
<script>
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
    data() {
        return {
            toggle: 'upcoming'
        };
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
      }
    }
  };
</script>