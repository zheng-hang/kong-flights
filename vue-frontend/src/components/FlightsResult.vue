<template>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" 
    rel="stylesheet" 
    integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" 
    crossorigin="anonymous">

    <!-- Fa fa Icon -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

    <!-- Display Flight Details from SearchFlights.html-->
    <div id="displayBox" style="padding: 15px; background-color: #5554;">
        <div class="row">
            <div class="col-md-4 custom-col">
                <div class="row">
                    <div class="row">
                        <div class="col-md">
                            <div class="row">
                                <h6> Departing: {{departDate}}</h6>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <p>{{departLoc}}</p>
                                </div>
                                <div class="col-2" style=" text-align: center;">
                                    <i class="fa fa-fighter-jet" aria-hidden="true" style="font-size:20px; padding-top: 5px;"></i>
                                </div>
                                <div class="col">
                                    <p>{{arrLoc}}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-2 custom-col" style="padding-left: 20px;">
                <div class="row" style="text-align: left;">
                    <h6>Class</h6>
                    <p>{{type_class}}</p>
                </div>
            </div>

            <div class="col" style="padding-left: 20px;">
                <div class="row" style="text-align: left;">
                    <h6>Number of Passengers</h6>
                    <p>{{numPax}}</p>
                </div>
            </div>
            <div class="col" style="padding-top:20px;">
                <button type="button" class="btn btn-outline-dark rounded-pill" @click="changeSearch()">Edit Search</button>
                <!-- <div v-if="showSearch" class="accordion">
                  <input type="text" placeholder="Search..." v-model="searchQuery">
                </div> -->
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
    <!-- <div for="matchedFlights"> -->
        <div id="displayBox" style="padding-right: 25px; padding-left: 25px; padding-top: 20px; height:200px; margin-top:10px">
            <AvailableFlights :departDate="departDate" :departLoc="departLoc" :departTime="departTime"
                                :arrDate="arrDate" :arrLoc="arrLoc" :arrTime="arrTime" :fare="fare" :flightDuration="flightDuration"/>
        </div>
    <!-- </div> -->
</template>

<script>
import AvailableFlights from './AvailableFlights.vue';

export default {
    components: {AvailableFlights}, 
    // props: ['formData'],
    data() {
        return {
                numPax:"1 adult",
                departDate: "28 MAR (THU)",
                departLoc: "Singapore",
                arrLoc: "Tokyo",
                type_class: "Economy",
                departTime: "SIN 08:05",
                arrDate: "28 MAR (THU)",
                arrTime: "NRT 15:45",
                fare: "SGD 2,883.90",
                flightDuration: "6 hr 40 min",
                showSearch: false,
                searchQuery: '',
                receivedData: '', 
            }
        },
    methods: {
        changeSearch(){
            this.showSearch = !this.showSearch;
        }
    },
    // created() {
    //     this.receivedData = this.$route.query.data;
    // }
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