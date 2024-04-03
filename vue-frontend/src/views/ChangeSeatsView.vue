<script setup>
import SeatChange from '../components/SeatChange.vue'
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
            <body style="background-color: #FAFAFA; margin:0; padding:0;"></body>
        <div class="container">
            <div class="legend rounded-3">
                <div class="col-4 d-flex justify-content-center">
                    <section class="seat available"></section>
                    <section class="seat-text">Standard Seat</section>
                </div>
                <div class="col-4 d-flex justify-content-center">
                    <section class="seat selected"></section>
                    <section class="seat-text">Selected Seat</section>
                </div>
                <div class="col-4 d-flex justify-content-center">
                    <section class="seat unavailable">X</section>
                    <section class="seat-text">Not Available</section>
                </div>
            </div>
        </div>
        <SeatSelector/>
    </template>

<script>

</script>

<style scoped>
    .container{
        display: flex;
        justify-content: center;
    }
    .legend{
        display: flex;
        align-items: center;
        margin-top: 10px;
        border-radius: 10%;
        height: 100px;
        border: solid;
        background-color: #b4b4b4;
        width: 92%
    }
    .seat {
        border-radius: 10%;
        height: 30px;
        width: 30px;
    }
    .seat-text {
        margin-left: 10px;
    }
    .available {
        background-color: #bada55;
    }
    .selected {
        background-color: #4d9dff;
    }
    .unavailable {
        background-color: #dddddd;
        font-weight: bold;
    }
</style>