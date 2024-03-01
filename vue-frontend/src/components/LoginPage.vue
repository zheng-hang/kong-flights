<template>
    <div>
        <h2>Login</h2>
        <form @submit.prevent="submitForm">
        <div>
            <label for="username">email</label>
            <input type="text" id="email" v-model="email" required />
        </div>
    
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" required />
        </div>
    
        <button type="submit">Login</button>
        </form>
    </div>

    <div>
    <button @click="login">Login Using Google</button>
    <div v-if="userDetails">
      <h2>User Details</h2>
      <p>Name: {{ userDetails.name }}</p>
      <p>Email: {{ userDetails.email }}</p>
      <p>Profile Picture: <img :src="userDetails.picture" alt="Profile Picture"></p>
    </div>
  </div>


</template>

<script>
export default {
    data() {
        return {
            email: '',
            password: ''
        };
    },
    methods: {
        async submitForm() {
            try {
                const response = await fetch('http://localhost:5000/login', {
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

                if (!response.ok) {
                    throw new Error('Failed to login');
                }

                console.log('Login successful');
                // Optionally, you can redirect the user to another page upon successful login
                window.location.href = '/';
            } catch (error) {
                console.error('Error logging in:', error.message);

            }
        }
    }
};


</script>