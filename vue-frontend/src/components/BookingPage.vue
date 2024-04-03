<script setup>
import BookingBanner from './BookingBanner.vue'
import PassengerDetail from './PassengerDetail.vue'
</script>

<template>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" 
    rel="stylesheet" 
    integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" 
    crossorigin="anonymous">

    <!-- Bootstrap Date-Picker Plugin -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.4.1/css/bootstrap-datepicker3.css"/>

    <!-- Fa fa Icon -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <body style="background-color: #FAFAFA; margin:0; padding:0;">
    <!-- Nav -->
    
    <!-- Selected Flight banner -->
        <BookingBanner :bookingData="bookingData"/>

    <!-- Title -->
    <div style="text-align: left; margin-left: 60px; margin-top: 20px">
        <h3>Passenger details</h3>
    </div>

    <form action="/seatsbooking">

    <!-- Passenger Details -->

    <!--<PassengerDetail v-for="num in numPax" :key="bookData.numPax.adults"/> -->
    <PassengerDetail/>

    <div class="d-flex justify-content-end mt-3">
        <input class="btn btn-primary px-4 mb-3 mt-1 me-5" type="submit" value="Next: Seat Selection" @click="seatSelection">
    </div>

    </form>


</body>
</template>

<script>
export default {
  data() {
    return {
        // FID, Airline, DepartureLoc, ArrivalLoc, Date, DepartureTime,Duration,Price,DepAirportCode,ArrAirportCode
        bookingData: {
            FID: "SQ 123",
            Date: "2024-04-15",
            DepartureTime: "10:30:00",
            DepartureLoc: "Singapore",
            ArrivalTime: "15:05:00",
            ArrivalLoc: "Berlin",
            Price: "1100",
            Duration: "1000"
        },
        // arrivalTime: "15:05:00"
    }
  },
  methods:{
    seatSelection(){
        this.$router.push('/seatsbooking');
    }
  }
}
</script>
<style scoped>

</style>