<template>
    <tr >
	<th>{{ creation_date.toLocaleString('en-US') }}</th>
	<th>{{ source }}</th>
	<th :class="{'has-text-danger' : error}">{{ import_status }}</th>
	<th>
	    <button class="button is-warning addSideSpacing" v-if="error" @click="showError" >View Details</button>
	    <button class="button is-primary addSideSpacing" :disabled="!parsed && !in_progress" @click="statusButton">{{ in_progress ? "View Status" : "Edit" }}</button>
	    <button class="button is-danger addSideSpacing" :class="{'is-loading' : loadingDelete }" @click="deleteImport" :disabled="in_progress" >Delete</button>
	</th>
    </tr>
</template>

<style>
.addSideSpacing {
    margin-left: 5px;
    margin-right: 5px;
}
</style>

<script>
import { getApi } from '../api';

export default {
    props: ['creation_date', 'source', 'parsed', 'run', '_id', 'error', 'in_progress'],
    data: function() {
	return {
	    loadingDelete: false
	}
    },
    computed:  {
	import_status: function() {
	    if(this.error) {
		if(this.parsed)
		    return "Failed to Import"
		else
		    return "Failed to Parse"
	    }
	    if(this.in_progress) {
		if(!this.parsed)
		    return "Parsing"
		else
		    return "Importing"
	    } else {
		if(!this.run)
		    return "Ready to Import"
		else
		    return "Imported"
	    }
	}
    },
    methods: {
	statusButton: function() {
	    if(this.in_progress) {
		if(this.parsed)
		    this.$router.push('/waitRun/' + this._id)
		else
		    this.$router.push('/waitParse/' + this._id)
	    } else {
		this.$router.push('/editImport/' + this._id)
	    }
	},
	deleteImport: async function() {
	    this.loadingDelete = true;
	    let result = await getApi(`/import/${this._id}/delete`);
	    this.loadingDelete = false;
	    if(result.status == 'ok')
		this.$emit("deleted", this._id);
	},
	showError: function() {
	    this.$store.commit('displayModal', { text: this.error, title: 'Error' });
	}
    }
}
</script>
