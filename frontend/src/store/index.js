import Vue from 'vue'
import Vuex from "vuex"

import { getApi } from '../api';

// Add Vuex
Vue.use(Vuex);

const store = new Vuex.Store(
    {
        state: {
            loggedIn: false,
	    user: {},
	    imports: {},
	    orders: {},
	    items: {},
	    terms: {},
	    customers: {},
	    messages: [],
	    modal: null,
        },
        mutations: {
            logIn(state, user) {
                state.loggedIn = true;
		state.user = user;
            },
            logOut(state) {
                state.loggedIn = false;
            },
	    displayMessage(state, msg) {
		state.messages.push(msg);
	    },
	    clearMessage(state, msg) {
		var index = state.messages.indexOf(msg);
		if (index !== -1) state.messages.splice(index, 1);
	    },
	    clearAllMessages(state) {
		state.messages.splice(0, state.messages.length);
	    },
	    displayModal(state, msg) {
		state.modal = msg;
	    },
	    clearModal(state) {
		state.modal = null; 
	    },
	    updateImport(state, import_obj) {
		console.log("Import object")
		console.log(import_obj)
		// Save to state
		Vue.set(state.imports, import_obj._id, import_obj);
	    },
	    updateOrder(state, order_obj) {
		var len = order_obj.items.length;
		for(var j = 0; j < len; j++) {
		    // Save to state
		    Vue.set(state.items, order_obj.items[j]._id, order_obj.items[j])
		    // Add valid
		    state.items[ order_obj.items[j]._id ].valid = !!state.items[ order_obj.items[j]._id ].internal_id;
		    // Remove nesting
		    order_obj.items[j] = order_obj.items[j]._id;
		}
		// Save to state
		Vue.set(state.orders, order_obj._id, order_obj);
		// Add valid
		state.orders[order_obj._id].customer_valid = !!state.orders[order_obj._id].customer_id
		state.orders[order_obj._id].salesrep_valid = state.orders[order_obj._id].salesrep_id
		
	    },
	    updateTerms(state, data) {
		for(var i = 0; i < data.length; i++) {
		    Vue.set(state.terms, data[i].internal_id, data[i].name)
		}
	    },
	    setOrder(state, data) {
		Vue.set(state.orders, data._id, data.value);
	    },
	    setItem(state, data) {
		Vue.set(state.items, data._id, data.value);
	    }
        },
	getters: {
	    getOrders: (state) => (import_id) => {
		return state.imports[import_id].orders;
	    }
	},
	actions: {
	    async getImportAPI(context, data) {
		let result = await getApi("/import/" + data.import_id);
		context.commit('updateImport', result);
		for(var i = 0; i < result.orders.length; i++) {
		    context.dispatch('getOrderAPI', { order_id : result.orders[i] } );
		}
	    },
	    async getOrderAPI(context, data) {
		let result = await getApi("/order/" + data.order_id);
		console.log("Order object:")
		console.log(result)
		context.commit('updateOrder', result);
	    },
	    async getTermAPI(context, data) {
		let result = await getApi("/terms");
		context.commit('updateTerms', result)
	    }
	}
    }
);

export default store
