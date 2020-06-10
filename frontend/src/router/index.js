import Vue from 'vue'
import VueRouter from 'vue-router'

import ListSets from '../views/ListSets.vue'
import ListUsers from '../views/ListUsers.vue'
import NewSet from '../views/NewSet.vue'
import NewUser from '../views/NewUser.vue'
import Login from '../views/Login.vue'

import store from '../store';
import { getApi } from '../api';

function loginGuard(to, from, next) {
    if(store.state.loggedIn == false) {
	next('/login');
    } else {
	next();
    }
}

function adminGuard(to, from, next) {
    if(store.state.loggedIn == false) {
	next('/login');
    } else if(!store.state.user.is_admin) {
	next('/');
    } else {
	next();
    }
}

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'ListSets',
    component: ListSets,
    beforeEnter: loginGuard
  },
  {
    path: '/users',
    name: 'ListUsers',
    component: ListUsers,
    beforeEnter: adminGuard
  },
  {
    path: '/newUser',
    name: 'NewUser',
    component: NewUser,
    beforeEnter: adminGuard
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/newSet',
    name: 'NewSet',
    component: NewSet,
    beforeEnter: loginGuard
  },
]

const router = new VueRouter({
  routes
})

router.afterEach((to, from) => {
    store.commit('clearAllMessages');
})

export default router
