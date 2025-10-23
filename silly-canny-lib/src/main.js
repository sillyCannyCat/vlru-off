import { createApp } from 'vue'
import App from './App.vue'
import MyLib from './lib.js'

const app = createApp(App)
app.use(MyLib).mount('#app')
