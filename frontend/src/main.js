import Vue from 'vue'
import Vuex from "vuex"
import App from './App.vue'
import router from './router'
import store from './store';

Vue.config.productionTip = false

// Add FontAwesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUserSecret, faUpload, faCheck, faTimes, faAngleDown, faAngleLeft, faCircle, faSync } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
library.add(faUserSecret)
library.add(faUpload)
library.add(faCheck)
library.add(faTimes)
library.add(faAngleDown)
library.add(faAngleLeft)
library.add(faCircle)
library.add(faSync)
Vue.component('font-awesome-icon', FontAwesomeIcon)

// Add multiselect
import Multiselect from 'vue-multiselect';
Vue.component('multiselect', Multiselect);

// Add bulma
import 'bulma/css/bulma.css'

new Vue({
  router,
  store: store,
  render: h => h(App)
}).$mount('#app')

document.title = "CC Import Utility"
