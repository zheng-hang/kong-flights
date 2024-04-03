<script setup>
    // import PlaneSeat from '../components/PlaneSeat.vue'
    import axios from 'axios'
</script>

<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-1"></div>
                <!-- Front Exit -->
                <div class="col-10">
                    <!-- <h1>Seat Selection</h1> -->
                    <!-- <div class="exit exit--front fuselage"></div> -->
                    
                    <ol v-for="(row, index) in rows" :key="index" class="cabin fuselage">
                        <li class="row">
                            <ol class="seats" type="A">
                                <li v-for="(column, index) in columns" :key="index" class="seat" :id="row + column">
                                    <input type="checkbox" :id="'checkbox-' + row + column" @click="selectSeat" :disabled="disableSeat(row+column)"/>
                                    <label :for="'checkbox-' + row + column">{{ row }}{{ column }}</label>
                                </li>
                            </ol>
                            <!-- Galley -->
                                <div v-if="row%15==0" class="galley">
                                    GALLEY
                                </div>  
                        </li>
                    </ol>

                <!-- Middle Exit -->
                <!-- <div class="exit exit--front fuselage"></div> -->
            </div>
            <div class="col-1"></div>
        </div>
    </div>

    <div class="d-flex justify-content-end">
        <input class="btn btn-primary me-4 mb-4" type="submit" value="Submit" @click="sendBooking">
    </div>
</template>

<script>
    // console.log(document.getElementById("1A"));
    export default {
        data() {
        return {
            numSeatsSelected: 0,
            isChecked: false,
            selectedSeat: "",
            sessionSeat: "", // simulate session['seat']
            isAvailable: false,
            rows: 72,
            flightId: "SQ 124",
            columns: ["A", "B", "C", "D", "E", "G", "H", "J", "K"],
            seatData: ""
            }
        },
        beforeMount() {
            this.getAvailableSeats()
            // this.loadSelectedSeat()
        },
        mounted() {
            this.loadSelectedSeat()
        },
    
    methods: {
        getAvailableSeats(){
            axios.get('http://localhost:5003/seat', {
        })
            .then(response => {
                this.seatData = response.data.data
                console.log(Array.from(response.data.data));
                console.log(typeof(Array.from(response.data.data)))
            })
            .catch( error => {
                console.error(error);
            })

        },
        disableSeat(seatPosition){
            for(let seat of this.filteredSeats){
                let seatId = seat.seatnum + seat.seatcol
                if(seatId == seatPosition){
                    // console.log(seatId + ": " + seat.available);
                    // console.log(seatPosition);
                    return true
                }
            }
        },
        selectSeat(event) {
            if(this.numSeatsSelected == 1){
                // If >1 seat selected, uncheck previously selected seat.
                this.isChecked="false";
                document.getElementById(this.selectedSeat).checked = false;
                this.numSeatsSelected--;
            }
            this.isChecked=event.target.checked;
            this.numSeatsSelected++;
            this.selectedSeat = event.target.id; 
        },
        loadSelectedSeat(){
            if(this.sessionSeat != ""){
                document.getElementById("checkbox-" + this.sessionSeat).checked = true;
            }
        },
        async sendBooking() {
            try {
                const data = { 
                    "email": "emily.jones987@example.org",
                    "fid": this.flightId,
                    "seatnum": this.selectedSeat[0],
                    "seatcol": this.selectedSeat[1]
                 };
                const response = await axios.post('http://localhost:5103', data);
                console.log(response.data); // Handle response from the microservice
            } catch (error) {
                console.error('Error sending data to microservice:', error);
            }
        }
    },
    computed: {
        filteredSeats() {
            var flightSeats = [];
            for(let seat of this.seatData){
                if(seat.fid == this.flightId){
                    flightSeats.push(seat)
                    console.log(flightSeats);
                }
            }
            return flightSeats;
        }
    }
    // 
        // filteredSeats() {
        //     const filtered = {};
        //     for (const key in this.seatData) {
        //         if (Object.prototype.hasOwnProperty.call(this.seatData, key) && this.seatData[key].fid === this.flightId) {
        //             filtered[key] = this.seatData[key];
        //         }
        //     }
        //     return filtered;
        // }

        // checkAvailability() {
            
        //     var seat = this.getSeatData();
        //     seat.availability
        // }
    // }
    }
</script>

<style scoped>
    *,*:before,*:after {
    box-sizing: border-box;
    }
    html {
    font-size: 16px;
    }

    /* .exit {
        position: relative;
        height: 50px;
        &:before,
        &:after {
            content: "EXIT";
            font-size: 14px;
            line-height: 18px;
            padding: 0px 2px;
            font-family: "Arial Narrow", Arial, sans-serif;
            display: block;
            position: absolute;
            background: green;
            color: white;
            top: 50%;
            transform: translate(0, -50%);
        }
        &:after {
            margin-right: 3%;
        }
        &:before {
            left: 0;
        }
        &:after {
            right: 0;
        }
    } */

    *,*:before,*:after {
  box-sizing: border-box;
    }
    html {
    font-size: 16px;
    }

    ol {
    list-style :none;
    padding: 0;
    margin: 0;
    }

    /* .row {
        margin: 0px auto;
    } */

    .seats {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: flex-start;  
    /* overflow: hidden; */
    }

    .seat {
    display: flex;
    flex: 0 0 7%;
    padding: 5px;
    position: relative;
    margin: 5px;
    height: 55px;
    &:nth-child(3), &:nth-child(6) {
        margin-right: 14.28571428571429%;
    }
    input[type=checkbox] {
        position: absolute;
        opacity: 0;
        + label {
        background: #bada55;      
        -webkit-animation-name: rubberBand;
            animation-name: rubberBand;
        animation-duration: 300ms;
        animation-fill-mode: both;
        }
    }
    input[type=checkbox]:checked {
        + label {
        background: #4d9dff;      
        -webkit-animation-name: rubberBand;
            animation-name: rubberBand;
        animation-duration: 300ms;
        animation-fill-mode: both;
        }
    }
    input[type=checkbox]:disabled {
        + label {
        background: #dddddd;
        text-indent: -9999px;
        overflow: hidden;
        &:after {
            content: "X";
            text-indent: 0;
            position: absolute;
            top: 4px;
            left: 50%;
            transform: translate(-50%, 0%);
        }
        &:hover {
            box-shadow: none;
            cursor: not-allowed;
        }
        }
    }
    label {    
        display: block;
        position: relative;    
        width: 100%;    
        text-align: center;
        font-size: 14px;
        font-weight: bold;
        line-height: 1.5rem;
        padding: 4px 0;
        background: #bada55;
        border-radius: 5px;
        animation-duration: 300ms;
        animation-fill-mode: both;
        
        &:before {
        content: "";
        position: absolute;
        width: 75%;
        height: 75%;
        top: 1px;
        left: 50%;
        transform: translate(-50%, 0%);
        background: rgba(255,255,255,.4);
        border-radius: 3px;
        }
        &:hover {
        cursor: pointer;
        box-shadow: 0 0 0px 2px #5C6AFF;
        }
        
    }
    }

    @-webkit-keyframes rubberBand {
    0% {
        -webkit-transform: scale3d(1, 1, 1);
                transform: scale3d(1, 1, 1);
    }

    30% {
        -webkit-transform: scale3d(1.25, 0.75, 1);
                transform: scale3d(1.25, 0.75, 1);
    }

    40% {
        -webkit-transform: scale3d(0.75, 1.25, 1);
                transform: scale3d(0.75, 1.25, 1);
    }

    50% {
        -webkit-transform: scale3d(1.15, 0.85, 1);
                transform: scale3d(1.15, 0.85, 1);
    }

    65% {
        -webkit-transform: scale3d(.95, 1.05, 1);
                transform: scale3d(.95, 1.05, 1);
    }

    75% {
        -webkit-transform: scale3d(1.05, .95, 1);
                transform: scale3d(1.05, .95, 1);
    }

    100% {
        -webkit-transform: scale3d(1, 1, 1);
                transform: scale3d(1, 1, 1);
    }
    }

    @keyframes rubberBand {
    0% {
        -webkit-transform: scale3d(1, 1, 1);
                transform: scale3d(1, 1, 1);
    }

    30% {
        -webkit-transform: scale3d(1.25, 0.75, 1);
                transform: scale3d(1.25, 0.75, 1);
    }

    40% {
        -webkit-transform: scale3d(0.75, 1.25, 1);
                transform: scale3d(0.75, 1.25, 1);
    }

    50% {
        -webkit-transform: scale3d(1.15, 0.85, 1);
                transform: scale3d(1.15, 0.85, 1);
    }

    65% {
        -webkit-transform: scale3d(.95, 1.05, 1);
                transform: scale3d(.95, 1.05, 1);
    }

    75% {
        -webkit-transform: scale3d(1.05, .95, 1);
                transform: scale3d(1.05, .95, 1);
    }

    100% {
        -webkit-transform: scale3d(1, 1, 1);
                transform: scale3d(1, 1, 1);
    }
    }

    .rubberBand {
    -webkit-animation-name: rubberBand;
            animation-name: rubberBand;
    }
    .btn {
        &:hover {
            cursor: pointer;
            box-shadow: 0 0 0px 2px #5C6AFF;
        }
    }
    /* .fuselage {
        border-right: 5px solid #d8d8d8;
        border-left: 5px solid #d8d8d8;
    } */


    .galley {
        margin: 20px auto;
    }
</style>