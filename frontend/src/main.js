// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import TDesign from 'tdesign-vue';
import http from './utils/http'
import router from './router'
import 'tdesign-vue/es/style/index.css';

Vue.config.productionTip = false
Vue.prototype.$http = http
Vue.use(TDesign)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
