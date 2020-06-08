import Vue from 'vue'
import VueRouter from 'vue-router'

import NewImport from '../views/NewImport.vue'
import ListImports from '../views/ListImports.vue'
import ListUsers from '../views/ListUsers.vue'
import NewUser from '../views/NewUser.vue'
import Login from '../views/Login.vue'
import WaitParse from '../views/WaitParse.vue'
import WaitRun from '../views/WaitRun.vue'
import EditImport from '../views/EditImport.vue'

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
    name: 'ListImports',
    component: ListImports,
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
    path: '/newImport',
    name: 'NewImport',
    component: NewImport,
    beforeEnter: loginGuard
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/waitParse/:id',
    name: 'WaitParse',
    component: WaitParse,
    beforeEnter: loginGuard
  },
  {
    path: '/waitRun/:id',
    name: 'WaitRun',
    component: WaitRun,
    beforeEnter: loginGuard
  },
  {
    path: '/editImport/:id',
    name: 'EditImport',
    component: EditImport,
    beforeEnter: loginGuard
  }
]

const router = new VueRouter({
  routes
})

router.afterEach((to, from) => {
    store.commit('clearAllMessages');
})

export default router
