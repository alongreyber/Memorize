<template>
    <div>
<div class="title is-1">
    Start New Import
</div>
    <br />

    <div class="control">
	<label class="label">
	    Choose Import Type
	</label>
	    <div v-for="import_type in import_types" >
		<label class="radio">
		    <label v-bind:for="import_type">{{import_type}}</label>
		    <input type="radio" v-bind:value="import_type" v-model="form.import_type" v-bind:id="import_type">
		</label>
	    </div>
    </div>

    <br />
    <br />

   <div class="field">
       <label class="label">
	   Upload File
       </label>
       <div class="file" v-bind:class="{ 'is-success': form.import_file != '' }" >
	  <label class="file-label">
	      <input class="file-input" v-on:change="handleFileInput()" ref="import_file" type="file">
	    <span class="file-cta">
	      <span class="file-icon">
		  <font-awesome-icon icon="upload"></font-awesome-icon>
	      </span>
	      <span class="file-label">
		Choose a file…
	      </span>
	    </span>
	  </label>
	</div> 
   </div>
    <br />
    <br />
    <button class="button is-primary" v-on:click="submitForm()">Parse</button>
    
</div>
</template>

<script>

import store from '../store';
import { postApiForm } from '../api';

export default {
    name: 'NewImport',
    data: function() {
	return {
	    import_types: [ "Brandwise / Brandwise Batch (XML)", "Whole Foods Regional (XLS)", "Whole Foods Reorder (XML)"],
	    form: {
		import_type: "",
		import_file: ""
	    }
	}
    },
    methods: {
	handleFileInput: function() {
	    this.form.import_file = this.$refs.import_file.files[0];
	},
	submitForm: async function() {
	    let formData = new FormData();
	    for ( var key in this.form ) {
		formData.append(key, this.form[key]);
	    }
	    // Submit
	    let result = await postApiForm("/submitImport", formData);
	    if(result.import_id) {
		this.$router.push("/waitParse/" + result.import_id);
	    }
	}
    },
}
</script>
