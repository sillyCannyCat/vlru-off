import UiButton from './components/UiButton.vue'
import './style.css'

export { UiButton }

export default {
  install(app) {
    app.component('Button', UiButton)
  },
}
