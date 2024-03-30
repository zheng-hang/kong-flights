<template>
    <!-- <div class="container">
        <button type="button" class="btn" style="background-color: #4d9dff; color:white;"></button>
    </div> -->
    
    <ol class="cabin fuselage">
        <li class="row">
        <ol class="seats" type="A">
            <li v-for="(column, index) in columns" :key="index" class="seat" id="{{ row }}{{ column }}">   
                <input type="checkbox"/>
                <label for="1A">{{ row }}{{ column }}</label>
            </li>
        </ol>
        </li>
    </ol>
</template>

<script>
export default {
    data() {
        return {
            columns: ["A", "B", "C", "D", "E", "G", "H", "J", "K"],
            status: "",
            seatData: 
                [
                    {
                        fid: "SQ 123",
                        seatcol: "A",
                        seatnum: "1",
                        available: 0,
                        price: 30,
                        class: "first"
                    },
                    {
                        fid: "SQ 123",
                        seatcol: "B",
                        seatnum: "1",
                        available: 1,
                        price: 30,
                        class: "first"
                    },
                    {
                        fid: "SQ 123",
                        seatcol: "C",
                        seatnum: "1",
                        available: 1,
                        price: 30,
                        class: "first"
                    }
                ]

            }
        },
    
    methods: {
        toggleSeatColor() {
            this.checkboxColor = this.isChecked ? 'green' : 'black';
        }
    }
}

</script>

<style scoped>
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

.row {
  
}

.seats {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: flex-start;  
}

.seat {
  display: flex;
  flex: 0 0 14.28571428571429%;
  padding: 5px;
  position: relative;  
  &:nth-child(3), &:nth-child(6) {
    margin-right: 14.28571428571429%;
  }
  input[type=checkbox] {
    position: absolute;
    opacity: 0;
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
</style>