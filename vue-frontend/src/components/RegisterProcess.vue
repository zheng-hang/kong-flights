<template>
   <div>
    <h2>Sign up</h2>
    <form @submit.prevent="submitForm">
      <div>
         <label for="username">Name:</label>
         <input type="text" id="username" v-model="username" required />
      </div>
      
      <div>
         <label for="email">Email:</label>
         <input type="email" id="email" v-model="email" required />
      </div>

      <div>
         <label for="password">Password:</label>
         <input type="password" id="password" v-model="password" required />
      </div>


      <button type="submit">Register</button>
    </form>
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
  },
  methods: {
    async submitForm() {
      try {
        const response = await fetch('http://localhost:5000/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password
          }),
          mode: 'cors' // no-cors, *cors, same-origin
        });

        if (!response.ok) {
          throw new Error('Failed to register');
        }

        console.log('Registration successful');
        // Optionally, you can redirect the user to another page upon successful registration
        window.location.href = '/login';
      } catch (error) {
        console.error('Error registering:', error.message);

        // Display error message to the user here ()
        

      }
    }
  }
};
</script>