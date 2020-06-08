<template>
<div class="column" v-if="item">
    {{ external_id }}
    <input class="input" v-bind:class="{ 'is-warning' : loading, 'is-danger' : !valid && !loading, 'is-success' : valid }" v-model="internal_id" type="text" v-on:input="verify" v-bind:size="text_width">
</div>
</template>

<script>
import { getApi } from '../api';

export default {
    props: ['item_id', 'order_id'],
    data: function() {
	return {
	    loading: false,
	    timeout: null
	}
    },
    computed: {
	item: {
	    set(body) {
		this.$store.commit('setItem',  {
		    _id: this.item_id,
		    value: body
		});
	    },
	    get() {
		return this.$store.state.items[this.item_id];
	    }
	},
	internal_id: {
	    set(body) { this.item = {...this.item, internal_id : body} },
	    get() { return this.item.internal_id }
	},
	_id: {
	    get() { return this.item._id }
	},
	external_id: {
	    get() { return this.item.external_id }
	},
	valid: {
	    set(body) { this.item = {...this.item, valid : body} },
	    get() { return this.item.valid }
	},
	text_width: function() {
	    return this.internal_id ? this.internal_id.toString().size : 2;
	}
    },
    methods: {
	verify: async function() {
	    // Validate field
	    // Note that javascript has weird rules about what is an integer
	    var isNumeric = !isNaN(parseInt(this.internal_id));
	    if(!isNumeric) {
		this.valid = false;
		return;
	    }
	    // Look up
	    this.loading = true;
	    clearTimeout(this.timeout);
	    this.timeout = setTimeout(async function() {
		let result = await getApi(
		    `/order/${this.order_id}/item/${this._id}/modify_id?internal_id=${this.internal_id}`);
		this.valid = result.status == 'valid';
		this.loading = false;
	    }.bind(this), 1000);
	}
    }
}
</script>
