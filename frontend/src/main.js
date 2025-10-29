import { createApp } from 'vue'
import { createYmaps } from 'vue-yandex-maps'
import App from './App.vue'
import router from './router'

import './styles/style.css'
import './styles/typography.css'
import './styles/variables.css'

const ymapSettings = {
  apikey: '513b75be-f0e6-46f9-9d12-0379745422ea',
}

const app = createApp(App)

app.use(router)
app.use(createYmaps(ymapSettings))
app.mount('#app')
