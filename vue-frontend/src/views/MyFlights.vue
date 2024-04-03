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
            <div v-for="(flight, i) in pastFlights.data.flights" :key="i">
                <div v-if="getArrivalDate(flight.Date, flight.Duration) <= new Date().toUTCString()" class="row" style="display:flex; justify-content: center; margin:250px; margin-top: 20px; margin-bottom: 20px;">
                    <!--Booking-->
                    <table class="table table-bordered" style="border-style:solid; border-color: #0D6FE5; border-width: thin;">
                        <thead style="background-color: #0DB4F3;">
                        <tr>
                            <th class="d-flex justify-content-between" style="padding: 20px;padding-bottom:10px;">
                                <h6 style="font-weight: bold">{{ flight.FID }} | {{ flight.DepartureLoc }} to {{ flight.ArrivalLoc }}</h6>
                                <h6 style="font-weight: bold">Economy | <a href="#" style="color:black" @click="changeSeat()"><i class="fas fa-edit"></i> Change Seat</a></h6>
                            </th>
                        </tr>
                        </thead>
                        <tbody style="background-color: white;">
                        <tr>
                            <td style="padding: 40px; padding-top:20px;">
                                <!-- Add flight duration -->
                                <span style="font-weight: bold;">{{ convertMinutes(flight.Duration) }}</span>
                                <div class="row" style="margin-top: 15px">
                                    <!-- Departure -->
                                    <div class="col-3">
                                        <p class="text-primary" style="font-weight: bold;">DEPARTURE</p>
                                        <h3>{{ flight.DepAirportCode }} {{ flight.DepartureTime }}</h3>
                                        <p>
                                            <span style="font-weight: bold;">{{ flight.DepartureLoc }}</span><br/>
                                            {{ formatDate(flight.Date) }}
                                        </p>
                                    </div>
                                    <div class="col-1 d-flex align-items-center justify-content-start">
                                        <!-- <font-awesome-icon icon="plane" /> -->
                                        <i class="fa-solid fa-plane fa-2xl"></i>
                                    </div>
                                    <!-- Arrival -->
                                    <div class="col-5">
                                        <p class="text-primary" style="font-weight: bold;">ARRIVAL</p>
                                        <h3>{{ flight.ArrAirportCode }} {{ calculateArrivalTime(flight.DepartureTime, flight.Duration) }}</h3>
                                        <p>
                                            <span style="font-weight: bold;">{{flight.ArrivalLoc}}</span><br/>
                                            {{ formatDate(getArrivalDate(flight.Date, flight.Duration)) }}
                                        </p>
                                    </div>
                                    <!-- Others -->
                                    <div class="col-3">
                                        <!-- Status -->
                                        <p class="text-primary"><span style="font-weight: bold;">STATUS:</span> CONFIRMED</p>
                                        <p>
                                            <span style="font-weight: bold;">{{ flight.Airline }} | {{ flight.FID }}</span><br/>
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
            <div v-for="(flight, i) in pastFlights.data.flights" :key="i">
                <div v-if="getArrivalDate(flight.Date, flight.Duration) > new Date().toUTCString()" class="row" style="display:flex; justify-content: center; margin:250px; margin-top: 20px; margin-bottom: 20px;">
                    <!--Booking-->
                    <table class="table table-bordered" style="border-style:solid; border-color: #0D6FE5; border-width: thin;">
                        <thead style="background-color: #0DB4F3;">
                        <tr>
                            <th class="d-flex justify-content-between" style="padding: 20px;padding-bottom:10px;">
                                <h6 style="font-weight: bold">{{ flight.FID }} | {{ flight.DepartureLoc }} to {{ flight.ArrivalLoc }}</h6>
                                <h6 style="font-weight: bold">Economy | Flight Completed</h6>
                            </th>
                        </tr>
                        </thead>
                        <tbody style="background-color: white;">
                        <tr>
                            <td style="padding: 40px; padding-top:20px;">
                                <!-- Add flight duration -->
                                <span style="font-weight: bold;">{{ convertMinutes(flight.Duration) }}</span>
                                <div class="row" style="margin-top: 15px">
                                    <!-- Departure -->
                                    <div class="col-3">
                                        <p class="text-primary" style="font-weight: bold;">DEPARTURE</p>
                                        <h3>{{ flight.DepAirportCode }} {{ flight.DepartureTime }}</h3>
                                        <p>
                                            <span style="font-weight: bold;">{{ flight.DepartureLoc }}</span><br/>
                                            {{ formatDate(flight.Date) }}
                                        </p>
                                    </div>
                                    <div class="col-1 d-flex align-items-center justify-content-start">
                                        <!-- <font-awesome-icon icon="plane" /> -->
                                        <i class="fa-solid fa-plane fa-2xl"></i>
                                    </div>
                                    <!-- Arrival -->
                                    <div class="col-5">
                                        <p class="text-primary" style="font-weight: bold;">ARRIVAL</p>
                                        <h3>{{ flight.ArrAirportCode }} {{ calculateArrivalTime(flight.DepartureTime, flight.Duration) }}</h3>
                                        <p>
                                            <span style="font-weight: bold;">{{flight.ArrivalLoc}}</span><br/>
                                            {{ formatDate(getArrivalDate(flight.Date, flight.Duration)) }}
                                        </p>
                                    </div>
                                    <!-- Others -->
                                    <div class="col-3">
                                        <!-- Status -->
                                        <p class="text-primary"><span style="font-weight: bold;">STATUS:</span> CONFIRMED</p>
                                        <p>
                                            <span style="font-weight: bold;">{{ flight.Airline }} | {{ flight.FID }}</span><br/>
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
    </div>
</template>
  
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
    data() {
        return {
            toggle: 'upcoming',
            pastFlights: ""
        };
    },
    beforeMount() {
        this.loadPastFlights();
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
      formatDate(dateInput) {
        const dateObject = new Date(dateInput);
        const options = { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' };
        return dateObject.toLocaleDateString('en-US', options);
      },
      calculateArrivalTime(departureTime, duration){
        // Split the time string into hours, minutes, and seconds
        const [hours, minutes, seconds] = departureTime.split(':').map(Number);

        // Calculate total minutes
        let totalMinutes = hours * 60 + minutes + duration;

        // Calculate new hours and minutes
        const newHours = Math.floor(totalMinutes / 60) % 24;
        const newMinutes = totalMinutes % 60;

        // Format the result
        const formattedResult = `${String(newHours).padStart(2, '0')}:${String(newMinutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

        return formattedResult;
      },
      getArrivalDate(departureTime, duration){
        // Convert the date string to a Date object
        const date = new Date(departureTime);

        // Add the minutes to the date
        date.setMinutes(date.getMinutes() + duration);

        // Format the date back into the desired string format
        const formattedDate = date.toUTCString();

        return formattedDate;
      },
      loadPastFlights() {
            // Make a GET request to the URL
            axios.get('http://localhost:5001/flight')
            .then(response => {
                // Handle the response data
                this.pastFlights = response.data;
                console.log(response.data);
            })
            .catch(error => {
                // Handle errors
                console.error(error);
            });
        }, 
      convertMinutes(minutes) {
            let hours = Math.floor(minutes / 60);
            let remainingMinutes = minutes % 60;
            return `${hours} hr ${remainingMinutes} min`;
      }        ,
      changeSeat() {
        this.$router.push('/seatsbooking');
      }       
    }
  };
</script>