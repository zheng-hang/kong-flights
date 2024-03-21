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

    <!-- Back to Search Flights button -->
    <button class="back-button" @click="goBack()"> Back to Search Flights</button>

    <!-- Display Flight Details from SearchFlights.html-->
    <div class="accordion" id="displayBox" style="padding-right: 25px; padding-left: 25px; padding-top: 20px;">
        <div class="row">
            <div class="col-md-3 custom-col">
                <div class="row">
                    <div class="row">
                        <div class="col-md">
                            <div class="row">
                                <h6>{{departDate}}</h6>
                            </div>
                            
                            <div class="row">
                                <div class="col">
                                    <p>{{departLoc}}</p>
                                </div>
                                <div class="col-2" style=" text-align: center;">
                                    <i class="fa fa-arrow-right" aria-hidden="true" style="font-size:20px; padding-top: 5px;"></i>
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
                <div class="row">
                    <h6>Class</h6>
                    <p>Economy</p>
                </div>
            </div>
            <div class="col" style="padding-left: 20px;">
                <div class="row">
                    <h6>Number of Passengers</h6>
                    <p>1 Adult</p>
                </div>
            </div>
            <div class="col" style="padding-top:20px;">
                <button type="button" class="btn btn-outline-dark rounded-pill">Edit Search</button>
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
        <div id="displayBox" style="padding-right: 25px; padding-left: 25px; padding-top: 20px; height:200px">
            <div class="row">
                <!-- Flight Detail -->
                <div class="col">
                    <div class="row">
                        <p>Non-stop - 9hrs 30min</p>
                    </div>
                    <div class="row">
                        <div class="col-md-3">
                            <h3>SIN 08:05</h3>
                            <p>Singapore</p>
                            <p>28 March (Thur)</p>
                        </div>
                        <div class="col" >
                            <p style="font-size: 60px;">·-----------·</p>
                        </div>
                        <div class="col-md-4">
                            <h3>NKT 18:35</h3>
                            <p>Singapore</p>
                            <p>28 March (Thur)</p>
                        </div>
                    </div>
                </div>
                <!-- Ticket Price -->
                <div class="col-md-2" style="border-left: 0.5px solid black; text-align: center;">
                    <p style="color: grey;">From SGD</p>
                    <h4>{{fare}}</h4>
                    <p style="color: grey;">per ticket</p>
                    <button type="button" class="button btn btn-outline-dark rounded-pill" style="width: 150px;"><span>Select</span></button>
                </div>
            </div>
        </div>
    <!-- </div> -->

    </body>
</template>

<script>
export default {
    data() {
        return {
                numPax:
                    {
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
        },
    methods: {
        goBack() {
            window.history.back();
        }
    }
}
</script>

<style scoped>
#displayBox {
        height: 100px;
        margin-top: 20px;
        margin-left: 60px;
        margin-right: 60px;
        background: #fff;
        border-radius: 20px;
        box-shadow: 1px 5px 10px 1px rgba(0, 0, 0, 0.2); 
    }
    .back-button{
        background-color: transparent;
        border: none;
        cursor: pointer;
        font-size: 16px;
        color: grey;
        padding: 10px 60px;
    }
    .locationDisplay{
        margin-top: 20px;
        margin-left: 60px;
        font-size: 20px;
        font-weight: bold;
    
    }
    .custom-col{
        border-right: 0.5px solid grey
    }
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