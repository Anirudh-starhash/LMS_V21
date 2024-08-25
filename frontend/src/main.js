// import './assets/main.css'

import { createApp } from 'vue'

import App from './App.vue'

import router from './router'

const app = createApp(App)


import axios from 'axios'

const instance=axios.create({
  baseURL:"http://127.0.0.1:5000",
});


app.config.globalProperties.$http=instance;
app.use(router)
app.mount('#app')