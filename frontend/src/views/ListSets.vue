<template>
<div>

<div class="level">
    <div class="level-left">
	<div class="title is-1">
	    My Study Sets
	</div>
    </div>
    <div class="level-right">
	<button @click="newSet" class="button is-medium is-link">
	    New Set
	</button>
    </div>
</div>

<list-set-element v-for="set in sets" v-bind="set"></list-set-element>
    
</div>
</template>

<style>

.rotate-icon {
    transition-duration: 0.8s;
    transition-property: transform;
}
.rotate-icon:hover {
    transform: rotate(180deg);
    -webkit-transform: rotate(180deg);
}
</style>


<script>

import { getApi } from '../api';
import ListSetElement from '../components/ListSetElement.vue';

export default {
    data: function() {
	return {
	    sets: [],
	}
    },
    mounted: async function() {
	let result = await getApi('/sets');
	this.sets = result;
	this.loadingImports = false;
    },
    methods: {
	newSet: function() {
	    this.$router.push("/newSet");
	},
    },
    components: {
	ListSetElement
    }
}
</script>
