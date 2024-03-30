<script setup>
    import PlaneSeat from '../components/PlaneSeat.vue'
</script>

<template>
    <div class="plane">
        <div class="cockpit">
                <h1>DRUA Project Seat Selection</h1>
        </div>
        <!-- Front Exit -->
        <div class="exit exit--front fuselage"></div>
        
        <PlaneSeat v-for="(row, index) in rows" :key="index"></PlaneSeat>
        <!-- Middle Exit -->
        <div class="exit exit--front fuselage"></div>
    </div>

</template>

<script>
    export default {
    data() {
        return {
        rows: 73
        };
    }
    };
</script>

<style scoped>
    *,*:before,*:after {
    box-sizing: border-box;
    }
    html {
    font-size: 16px;
    }

    .plane {
    margin: 30px auto;
    max-width: 300px;
    }

    .cockpit {
        height: 250px; 
        position: relative;
        overflow: hidden;
        text-align: center;
        border-bottom: 5px solid #d8d8d8;
        &:before {
            content: "";
            display: block;
            position: absolute;
            top: 0;
            left: 0;
            height: 500px;
            width: 100%;
            border-radius: 50%;
            border-right: 5px solid #d8d8d8;
            border-left: 5px solid #d8d8d8;
        }
        h1 {
            width: 60%;
            margin: 100px auto 35px auto;
        }
    }

    .exit {
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
        &:before {
            left: 0;
        }
        &:after {
            right: 0;
        }
    }

    .fuselage {
        border-right: 5px solid #d8d8d8;
        border-left: 5px solid #d8d8d8;
    }


</style>