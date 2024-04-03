<script setup>
import { onMounted } from 'vue';

const loadCss = (url) => {
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = url;
  if (url.includes('bootstrap')) {
    link.integrity = 'sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx';
    link.crossOrigin = 'anonymous';
    }
  document.head.appendChild(link);
};

const loadScript = (url) => {
  const script = document.createElement('script');
  script.src = url;
  script.async = true;
  if (url.includes('kit.fontawesome')) {
    script.crossOrigin = 'anonymous';
  }
  script.async = true;
  document.body.appendChild(script);
};

onMounted(() => {
  // Load Bootstrap CSS
  loadCss('https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css');
  
  // Load Font Awesome CSS
  loadCss('path/to/font-awesome/css/font-awesome.min.css');
  
  // Load Font Awesome JavaScript
  loadScript('https://kit.fontawesome.com/5ca5b3f212.js');
});
</script>

<template>
    <div class="p-4">
      <div class="container">
        <div class="row g-5">
            <div>
                <label class="d-block"><h4>Review your booking</h4></label>
                <small class="text-secondary">Review your booking and complete your payment and authentication, or this booking session may expire.</small>
            </div>
          <div class="col-md-8 col-sm-6 col-xs-12">
            <div>
              <div>
                  <label class="d-block"><h4>Payment Method</h4></label>
                  <small class="text-secondary">Choose your payment method</small>
                </div>
                  <br/>
                <!-- Paypal API -->
                <div id="paypal-button-container" ref="paypalButtonContainer"></div>
                <p id="result-message"></p>
            </div>
          </div>
          <div class="col-md-4">
            <label class="d-block"><h4>Purchase Summary</h4></label>
            <div style="background:#eff4f8;border-radius:16px;">
              <div id="ticket">
                <div class="d-flex p-4">
                    <table class="w-100" id="cartTable">
                  <tr>
                    <span class="text-secondary">Flight to Tokyo from Singapore</span>
                  </tr>
                  <tr>
                    <td><strong>Departure Date</strong></td>
                    <td>28 March 2024</td>
                  </tr>
                  <tr>
                    <td><strong>Departure Time</strong></td>
                    <td>XX:XX:XX</td>
                  </tr>
                  <tr>
                    <td><strong>Arrival Date</strong></td>
                    <td>28 March 2024</td>
                  </tr>
                  <tr>
                    <td><strong>Arrival Time</strong></td>
                    <td>YY:YY:YY</td>
                  </tr>
                  <tr>
                      <td><small class="text-secondary">Total to be paid</small></td>
                      <td><div class="fs-2"><strong>{{fare}}</strong></div></td>
                  </tr>
                </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
export default {
  data() {
    return {
      resultMessage: "",
      fare:'$999.99',
    };
  },
  mounted() {
    // Dynamically add PayPal SDK script to the DOM
    const script = document.createElement('script');
    script.src = 'https://www.paypal.com/sdk/js?client-id=AbZr2__i9EuqqR55lJlvSEuwBj-2Hhp-IFZg8MjZ_QeBIrHOZbIlUBy7Lf5YPB6_0IFznLH4Yv7ZJbe9&currency=USD';
    script.async = true;
    script.onload = () => {
      this.initPayPalButton();
    };
    document.body.appendChild(script);
  },
  methods: {
    async initPayPalButton() {
      try {
        window.paypal.Buttons({
          createOrder: async () => {
            try {
              const response = await fetch("/api/orders", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({
                  cart: [
                    {
                      id: "01",
                      quantity: "999",
                    },
                  ],
                }),
              });

              const orderData = await response.json();

              if (orderData.id) {
                return orderData.id;
              } else {
                const errorDetail = orderData?.details?.[0];
                const errorMessage = errorDetail
                  ? `${errorDetail.issue} ${errorDetail.description} (${orderData.debug_id})`
                  : JSON.stringify(orderData);

                throw new Error(errorMessage);
              }
            } catch (error) {
              console.error(error);
              this.resultMessage = `Could not initiate PayPal Checkout...<br><br>${error}`;
            }
          },
          onApprove: async (data, actions) => {
            try {
              const response = await fetch(`/api/orders/${data.orderID}/capture`, {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
              });

              const orderData = await response.json();

              const errorDetail = orderData?.details?.[0];

              if (errorDetail?.issue === "INSTRUMENT_DECLINED") {
                return actions.restart();
              } else if (errorDetail) {
                throw new Error(`${errorDetail.description} (${orderData.debug_id})`);
              } else if (!orderData.purchase_units) {
                throw new Error(JSON.stringify(orderData));
              } else {
                const transaction =
                  orderData?.purchase_units?.[0]?.payments?.captures?.[0] ||
                  orderData?.purchase_units?.[0]?.payments?.authorizations?.[0];
                this.resultMessage = `Transaction ${transaction.status}: ${transaction.id}<br><br>See console for all available details`;
                console.log("Capture result", orderData, JSON.stringify(orderData, null, 2));
              }
            } catch (error) {
              console.error(error);
              this.resultMessage = `Sorry, your transaction could not be processed...<br><br>${error}`;
            }
          },
        }).render(this.$refs.paypalButtonContainer);
      } catch (error) {
        console.error(error);
        this.resultMessage = `Error initializing PayPal button: ${error}`;
      }
    },
  },
  // Example function to show a result to the user. Your site's UI library can be used instead.
  resultMessage(message) {
    const container = document.querySelector("#result-message");
    container.innerHTML = message;
  }
};


</script>

<style scoped>

.form-control {
      min-height:48px;
      border-radius:8px;
    }
    button.btn {
      min-height:54px;
    }
    #cartTable td {
      padding:6px;
    }
    #cartTable td:nth-of-type(2){
      text-align:right
    }
    #ticket {
      background:#dde8f0;
      border-top:1px dashed #bdbdbd;
      position:relative;
    }
    #paypal-button-container{
        /* padding-left: 20px; */
    }
</style>