import Vue from 'vue';
import VueRouter from 'vue-router';
import Users from '../components/Users.vue';
import Roles from '../components/Roles.vue';
import Groups from '../components/Groups.vue';

Vue.use(VueRouter);

export default new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/users',
            name: 'Users',
            component: Users,
        },
        {
            path: '/groups',
            name: 'Groups',
            component: Groups,
        },
        {
            path: '/roles',
            name: 'Roles',
            component: Roles,
        },

    ],
});
