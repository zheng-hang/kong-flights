import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import VueSession from 'vue-session';

const app = createApp(App);
app.use(router);
app.use(VueSession, { persist: true });

app.mount('#app');
