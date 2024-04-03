<script setup>
// import axios from 'axios';
import {onMounted } from 'vue';
// import AvailableFlights from './AvailableFlights.vue';

const loadCss = (url) => {
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = url;
  if (url.includes('bootstrap')) {
    link.integrity = 'sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx';
    link.crossOrigin = 'anonymous';
    }
  document.head.appendChild(link);
};

const loadScript = (url) => {
  const script = document.createElement('script');
  script.src = url;
  script.async = true;
  if (url.includes('kit.fontawesome')) {
    script.crossOrigin = 'anonymous';
  }
  script.async = true;
  document.body.appendChild(script);
};

onMounted(() => {
  // Load Bootstrap CSS
  loadCss('https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css');
  
  // Load Font Awesome CSS
  loadCss('path/to/font-awesome/css/font-awesome.min.css');
  
  // Load Font Awesome JavaScript
  loadScript('https://kit.fontawesome.com/5ca5b3f212.js');
});
</script>

<template>
    <!-- Display Flight Details from SearchFlights.html-->
    <div id="displayBox" style="padding: 15px; background-color: #5554;">
        <div class="row">
            <div class="col-md-4 custom-col">
                <div class="row">
                    <div class="row">
                        <div class="col-md">
                            <div class="row">
                                <h6> Departing: {{$route.params.departDate}}</h6>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <p>{{$route.params.departLoc}}</p>
                                </div>
                                <div class="col-2" style=" text-align: center;">
                                    <i class="fa fa-fighter-jet" aria-hidden="true" style="font-size:20px; padding-top: 5px;"></i>
                                </div>
                                <div class="col">
                                    <p>{{$route.params.arrLoc}}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-2 custom-col" style="padding-left: 20px;">
                <div class="row" style="text-align: left;">
                    <h6>Class</h6>
                    <p>Economy</p>
                </div>
            </div>

            <div class="col" style="padding-left: 20px;">
                <div class="row" style="text-align: left;">
                    <h6>Number of Passengers</h6>
                    <p>1 Adult</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Display Departure Location to Arrival Location -->
    <div class="locationDisplay">
        {{departLoc}}  
        <i class="fa fa-plane" aria-hidden="true"></i>
        {{arrLoc}}
    </div>
    <!-- Display Matched Flights -->
    <!-- <div v-for="(flight, i) in availableFlights.data.flights" :key="i">
        <div id="displayBox" style="padding-right: 25px; padding-left: 25px; padding-top: 20px; height:200px; margin-top:10px">
            <AvailableFlights :departDate="flight.departDate" :departLoc="flight.DepartureLoc" :departTime="flight.DepartureTime"
                                :arrDate="formatDate(getArrivalDate(flight.Date, flight.Duration))" :arrLoc="flight.ArrivalLoc" 
                                :arrTime="calculateArrivalTime(flight.DepartureTime, flight.Duration)" :fare="f.fare" :flightDuration="flight.Duration"/>
        </div>
    </div> -->
</template>

<script>
export default {
    // components: {AvailableFlights}, 
    props: ['formData'],
    data() {
        return {
                departDate: "",
                departLoc: "",
                arrLoc: "",
                departTime: "",
                arrDate: "",
                arrTime: "",
                fare: "",
                flightDuration: "",
                // availableFlights: '',
                receivedData: ''
            }
        },
    mounted() {
    // Access form data passed from the previous page
        this.receivedData = this.$route.params.data;
    }
}

</script>

<style scoped>
    #displayBox {
        height: auto;
        margin-top: 60px;
        margin-left: 60px;
        margin-right:60px;
        background: #fff;
        border-radius: 20px;
        box-shadow: 1px 5px 10px 1px rgba(0, 0, 0, 0.2); 
    }
    .locationDisplay{
        margin-top: 40px;
        margin-left: 60px;
        font-size: 20px;
        font-weight: bold;
        text-align: left;
    
    }
    /* results from prev page -- grey border between categories */
    .custom-col{
        border-right: 0.5px solid grey
    }
    /* bolden category names */
    h6{
        font-weight: bold;
    }
    /* accordian */
    .accordion {
        display: none; /* Initially hide accordion */
    }
    .accordion.show {
    display: block; /* Show accordion when it's active */
    }
</style>