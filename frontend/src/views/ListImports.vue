<template>
<div>

<div class="level">
    <div class="level-left">
	<div class="title is-1">
	    My Imports
	</div>
    </div>
    <div class="level-right">
	<button class="button is-primary" :class="{ 'is-loading' : loadingImports }" style="margin-right: 10px" @click='loadImports'>
	    <span class="icon is-medium has-text-white rotate-icon" v-if="!loadingImports">
		<font-awesome-icon :icon="'sync'">
		</font-awesome-icon>
	    </span>
	</button>
	<button @click="newImport" class="button is-medium is-link">
	    New Import
	</button>
    </div>
</div>

<table class="table">
    <thead>
	<tr>
	    <th>Created</th>
	    <th>Type</th>
	    <th>Status</th>
	    <th>Actions</th>
	</tr>
    </thead>
    <tbody>
	<list-import-element v-for="import_obj in imports" v-bind="import_obj" @deleted="handleDelete"></list-import-element>
    </tbody>
</table>
    
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

import ListImportElement from '../components/ListImportElement';

export default {
    data: function() {
	return {
	    imports: [],
	    loadingImports: false,
	}
    },
    mounted: async function() {
	this.loadImports()
	this.loadingImports = false;
    },
    methods: {
	loadImports: async function() {
	    this.loadingImports = true;
	    let result = await getApi('/imports');
	    if(result) {
		this.imports = result.reverse();
		// Convert to datetime object
		for(var i = 0; i < this.imports.length; i++) {
		    var d = new Date(Date.parse(this.imports[i].creation_date));
		    this.$set(this.imports, i, {...this.imports[i], creation_date : d });
		}
	    }
	    // Wait to mark this as loaded to give user visual feedback
	    setTimeout(function() { this.loadingImports = false; }.bind(this) , 1000);
	    
	},
	newImport: function() {
	    this.$router.push("/newImport");
	},
	handleDelete: function(oid) {
	    for(var i = 0; i < this.imports.length; i++) {
		if(this.imports[i]._id == oid)
		    this.imports.splice(i, 1);
	    }
	},
    },
    components: {
	ListImportElement
    }
}
</script>
