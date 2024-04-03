<script setup>
</script>

<template>
    <div class="banner"> 
        <div class="row">
            <div class="col-2 ms-5 ps-4 text-start">
                <h6 class="text-secondary">Departing</h6>
                <h6 class="fw-bold">{{ formatDate(bookingData.Date) }}</h6>
                <h4 class="blue fw-bold">{{ bookingData.DepartureTime }}</h4>
                <h6 class="fw-bold">{{ bookingData.DepartureLoc }}</h6>
            </div>
            <div class="col-1 pt-4 me-5 my-auto">
                <i class="fa fa-plane fa-2x d-flex justify-content-center"></i>
                <h6 class="text-secondary d-flex justify-content-center">{{ bookingData.flightDuration }}</h6>
            </div>
            <div class="col-2 ms-5 ps-4 text-start">
                <h6 class="text-secondary">Arrival</h6>
                <h6 class="fw-bold">{{ formatDate(bookingData.Date) }}</h6>
                <h4 class="blue fw-bold">{{ this.arrivalTime }}</h4>
                <h6 class="fw-bold">{{ bookingData.ArrivalLoc }}</h6>
            </div>
            <div class="col ms-5 ps-4 text-start">
                <h6 class="text-secondary">Total Fare</h6>
                <span class="h6 fw-bold">1 Adult</span>
                <h4 class="blue fw-bold">SGD {{ bookingData.Price.toLocaleString()}}</h4>
                <h6 class="fst-italic">Total fare includes discounts, taxes, and surcharges</h6>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        bookingData: {
            type: Object,
            required: true
        },
        arrivalTime: {
            type: String,
            required: true
        }
    },
    methods: {
        formatDate(dateInput) { 
        const dateObject = new Date(dateInput); 
        const options = { month: 'short', day: 'numeric', year: 'numeric', weekday: 'short' }; 
        return dateObject.toLocaleDateString('en-US', options); 
      }
    }
}
</script>

<style scoped>
.blue {
    color: #0DB4F3;
}

.banner {
    background-color: #EBEBEB;
    padding: 20px 0px;
}   
</style>