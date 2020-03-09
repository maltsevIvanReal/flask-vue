import 'bootstrap/dist/css/bootstrap.css';
import Vue from 'vue';
import App from './App.vue';
import router from './router';
import VModal from 'vue-js-modal'
import BootstrapVue from 'bootstrap-vue';
import {IconsPlugin} from 'bootstrap-vue'


Vue.use(IconsPlugin);

Vue.use(BootstrapVue);

Vue.use(VModal);


Vue.config.productionTip = false;


new Vue({
    router,
    render: (h) => h(App),
}).$mount('#app');

