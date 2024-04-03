<template>
    <div class="row">
        <div class="col">
            <div class="row">
                <p>Non-stop - {{flightDuration}}</p>
            </div>
            <div class="row">
                <div class="col-md-3">
                    <h3>{{departTime}}</h3>
                        <p>{{departLoc}}</p>
                        <p>{{departDate}}</p>
                </div>
                <div class="col" >
                    <p style="font-size: 60px;">------------------</p>
                </div>
                <div class="col-md-4">
                    <h3>{{arrTime}}</h3>
                    <p>{{arrLoc}}</p>
                    <p>{{arrDate}}</p>
                </div>
            </div>
        </div>
                
        <div class="col-md-2" style="border-left: 0.5px solid black; text-align: center;">
            <p style="color: grey;">From SGD</p>
                <h4>{{fare}}</h4>
                <p style="color: grey;">per ticket</p>
                <button type="button" class="button btn btn-outline-dark rounded-pill" style="width: 150px;" @click="bookingPage()"><span>Select</span></button>
            </div>
        </div>
</template>

<script>
    export default {
        props:['departTime', 'departDate', 'departLoc', 'arrDate', 'arrTime', 'arrLoc', 'fare', 'flightDuration'],
        methods: {
            bookingPage(){
                this.$router.push({name: '/booking'});
            }
        }
    }
</script>

<style scoped>
    /* button animations */
    .button span {
        cursor: pointer;
        display: inline-block;
        position: relative;
        transition: 0.5s;
    }
    .button span:after {
        content: '\00bb';
        position: absolute;
        opacity: 0;
        top: -9px;
        right: -20px;
        transition: 0.5s;
        font-size: 24px; 
    }
    .button:hover{
        background-color: green;
    }
    .button:hover span {
        padding-right: 25px;
    }

    .button:hover span:after {
        opacity: 1;
        right: 0;
        
    }
</style> 