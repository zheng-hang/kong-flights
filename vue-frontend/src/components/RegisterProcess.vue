<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';


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

const submitForm = async() =>{
    errorMessage.value = "";

    const email = document.querySelector("input[type='text']").value;
    const password = document.querySelector("input[type='password']").value;
    try {
        const response = await axios.post('http://localhost:5000/register', {
            email: email,
            password: password
        })
        if(response && response.data && response.status === 200){
            console.log('Register successful');
            this.$router.push('/login');
        } 
        else {
            errorMessage.value = 'Invalid credentials. Please try again.';
        }
    }
    catch (error) {
        if (error.response && error.response.data.error) {
            errorMessage.value = error.response.data.error;
        } else {
            errorMessage.value = "Register request failed";
        }
        console.error("Register error:", error);
    }
};
const errorMessage = ref("");
</script>

<template>
    <div class="background">
        <div class="rounded-rectangle">
            <div class="columns" >
                <div class="col-md-6">
                    <img src="../assets/SMOOth Airlines Logo - Square.png" style="height: 60%;">
                </div>
                <div class="col-md-6">
                  <form @submit.prevent="submitForm">
                    <h2 style="font-weight: bold; padding-top:20px; padding-bottom: 10px;">Join Us Onboard!</h2>
                    <h5 style="font-weight: bold; padding-bottom: 10px;">Register for an account today!</h5>
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
                      <button type="button" class="btn btn-success rounded-pill" style="width: 100%;margin-top: 10px;" @click="register"><span>Register</span></button>
                  </form>
                </div>
            </div>
        </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password: ''
    };
  }
}
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