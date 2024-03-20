<script setup>
</script>

<template>
    <div class="banner"> 
        <div class="row">
            <div class="col-2 ms-5 ps-4 text-start">
                <h6 class="text-secondary">Departing</h6>
                <h6 class="fw-bold">{{ bookingData.departDate }}</h6>
                <h4 class="blue fw-bold">{{ bookingData.departTime }}</h4>
                <h6 class="fw-bold">{{ bookingData.departLoc }}</h6>
            </div>
            <div class="col-2 pt-4 my-auto">
                <i class="fa fa-plane fa-2x d-flex justify-content-center"></i>
                <h6 class="text-secondary d-flex justify-content-center">{{ bookingData.flightDuration }}</h6>
            </div>
            <div class="col-2 ms-5 ps-4 text-start">
                <h6 class="text-secondary">Departing</h6>
                <h6 class="fw-bold">{{ bookingData.arrDate }}</h6>
                <h4 class="blue fw-bold">{{ bookingData.arrTime }}</h4>
                <h6 class="fw-bold">{{ bookingData.arrLoc }}</h6>
            </div>
            <div class="col ms-5 ps-4 text-start">
                <h6 class="text-secondary">Total Fare</h6>
                <span class="h6 fw-bold">{{ bookingData.numPax.adults }} Adults</span>
                <span v-show="bookingData.numPax.children > 0" class="h6 fw-bold"> + {{ bookingData.numPax.children }} Children</span> 
                <h4 class="blue fw-bold">SGD 2,883.90</h4>
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