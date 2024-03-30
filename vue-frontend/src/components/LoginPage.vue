<script setup>
// import axios from 'axios';
</script>

<template>
    <div class="background">
        <div class="rounded-rectangle">
            <div class="columns" >
                <div class="col-md-6">
                    <img src="../assets/SMOOth Airlines Logo - Square.png" style="height: 60%;">
                </div>
                <div class="col-md-6">
                    <h2 style="font-weight: bold; padding-top:20px">Welcome Onboard!</h2>
                    <h4 style="font-weight: bold; padding-bottom: 10px; padding-top: 10px;">Log in to your account</h4>
                    <form @submit.prevent="submitForm">
                        <div class="input-group mb-3">
                            <div class="input-group-prepend">
                                <span class="input-group-text"><i class="fa fa-envelope-o" aria-hidden="true" style="font-size: 160%;"></i></span>
                            </div>
                            <input type="text" class="form-control" placeholder="Email" aria-label="Email" aria-describedby="basic-addon1" v-model="email" required>
                        </div>
                        <div class="input-group mb-3">
                            <div class="input-group-prepend">
                                <span class="input-group-text"><i class="fa fa-lock" aria-hidden="true" style="font-size: 160%;"></i></span>
                            </div>
                            <input type="password" class="form-control" placeholder="Password" aria-label="Password" aria-describedby="basic-addon1" v-model="password" required>
                        </div>
                    </form>
                    <p class="text-muted"> No account? <a href="/register">Create an account</a></p>
                    <button type="button" class="btn btn-success rounded-pill" style="width: 100%;" @click="login"><span>Login</span></button>
                </div>
            </div>
        </div>
  </div>
</template>

<script>
export default {
    async mounted() {
      // Load Bootstrap CSS
      this.loadCss('https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css');
       // Load Font Awesome CSS and JavaScript
       this.loadCss('path/to/font-awesome/css/font-awesome.min.css');
      this.loadScript('https://kit.fontawesome.com/5ca5b3f212.js');
    },
    data() {
        return {
            email: '',
            password: ''
        };
    },
    methods: {
        async submitForm() {
            try {
                const response = await fetch('http://localhost:8080/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password
                    }),
                    mode: 'cors' // no-cors, *cors, same-origin
                });

                if(response){
                    console.log('Login successful');
                    window.location.href = '/searchFlights';
                } 
                else {
                    throw new Error('Failed to login');
                }

            } catch (error) {
                console.error('Error logging in:', error.message);

            }
        },
        loadCss(url) {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = url;
            if (url.includes('bootstrap')) {
            link.integrity = 'sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx';
            link.crossOrigin = 'anonymous';
            }
            document.head.appendChild(link);
        },
        loadScript(url) {
            const script = document.createElement('script');
            script.src = url;
            if (url.includes('kit.fontawesome')) {
            script.crossOrigin = 'anonymous';
            }
            script.async = true;
            document.body.appendChild(script);
        },
        login(){
            this.submitForm(); 
        }
    }
};


</script>

<style scoped>
.background {
  background-color: #0DB4F3;
  height: 100vh; /* Adjust height as needed */
  display: flex;
  justify-content: center;
  align-items: center;
}

.rounded-rectangle {
  background-color: white;
  border-radius: 20px; /* Adjust border-radius for desired roundness */
  padding: 20px; /* Adjust padding as needed */
  height:400px;
}
.columns {
  display: flex;
  height: fit-content;
  width: fit-content;
}
.input-group-text{
    background-color: white;
    color:#0DB4F3;
    border-right:none; 
}
</style>