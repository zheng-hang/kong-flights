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
    <div style="margin:0; box-shadow: 0 2px 4px 0 rgba(0,0,0,.2); 
        background-color: white; height: 65px;display: flex;align-items: center;justify-content: center;">
        <ul style="list-style-type: none; text-align: center;">
            <li style="display: inline; margin: 10px;"><a href="">Search Flights</a></li>
            <li style="display: inline; margin: 10px; font-weight: bold;"><a href="">My Flights</a></li>
            <li style="display: inline; margin: 10px;"><a href="">My Payment</a></li>
        </ul>
    </div>
    
    <!-- Selected Flight banner -->
        <BookingBanner :bookingData="bookingData"/>

    <!-- Title -->
    <div style="text-align: left; margin-left: 60px; margin-top: 20px">
        <h3>Passenger details</h3>
    </div>

    <form action="">

    <!-- Passenger Details -->

    <!--<PassengerDetail v-for="num in numPax" :key="bookData.numPax.adults"/> -->
    <PassengerDetail/>
    </form>


</body>
</template>

<script>
export default {
  data() {
    return {
        bookingData: {
            numPax: {
                adults: 2,
                children: 0
            },
        departDate: "28 Mar (Thu)",
        departTime: "SIN 08:05",
        departLoc: "Singapore",
        arrDate: "28 Mar (Thu)",
        arrTime: "NRT 15:45",
        arrLoc: "Tokyo",
        fare: "SGD 2,883.90",
        flightDuration: "6 hr 40 min"
        }
    }
  }
}
</script>
<style scoped>

</style>