<template>
    <div>
<div class="title is-1">
    Create New Set
</div>
    <br />

    <div class="control">
	<label class="label">
	    Name
	</label>
	<input class="input" type="text" v-model="name" >
    </div>
    <div class="control">
	<label class="label">
	    Language
	</label>
	<multiselect v-model="language_selected" :options="language_list()">
	</multiselect>
    </div>

    <br />
    <br />

    <br />
    <br />
    <button class="button is-primary" @click="createSet()">Create</button>
    
</div>
</template>

<script>

import store from '../store';
import { postApiJson } from '../api';

export default {
    name: 'NewImport',
    data: function() {
	return {
	    language_map: {
		"Spanish" : "es",
		"Arabic" : "ar",
		"Hebrew" : "he",
		"French" : "fr-fr",
		"Korean" : "ko"
	    },
	    language_selected: null,
	    name: ""
	}
    },
    methods: {
	language_list: function() {
	    return Object.keys(this.language_map);
	},
	createSet: async function() {
	    let language_code = this.language_map[this.language_selected];
	    let data = { name : this.name, language: language_code };
	    let result = await postApiJson("/sets", data);
	    if(result.status == 'fail') {
		this.$store.commit('displayMessage',
		    {'color' : 'is-warning', 'text' : result.data});
		return;
	    }
	    this.$store.commit('displayMessage',
		{'color' : 'is-success', 'text' : 'Created Set'});
	    this.$router.push("/");
	}
    }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
