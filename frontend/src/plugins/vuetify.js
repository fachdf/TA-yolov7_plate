import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import VueAxios from 'vue-axios';
import axios from 'axios'; // this is all about to change

Vue.use(Vuetify);
Vue.use(VueAxios, axios);

export default new Vuetify({
});
