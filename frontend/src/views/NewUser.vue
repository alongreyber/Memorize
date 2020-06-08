<template>
    <div>
<div class="title is-1">
    Create New User
</div>
    <br />

    <div class="control">
	<label class="label">
	    Username
	</label>
	<input class="input" type="text" v-model="username" >
    </div>
    <div class="control">
	<label class="label">
	    Password
	</label>
	<input class="input" type="password" v-model="password" >
    </div>

    <br />
    <br />

    <br />
    <br />
    <button class="button is-primary" @click="createUser()">Create</button>
    
</div>
</template>

<script>

import store from '../store';
import { postApiJson } from '../api';

export default {
    name: 'NewImport',
    data: function() {
	return {
	    "username" : '',
	    "password" : "",
	}
    },
    methods: {
	createUser: async function() {
	    let data = {"username" : this.username, "password" : this.password};
	    let result = await postApiJson("/user/new", data);
	    if(result.status == 'ok') {
		this.$store.commit('displayMessage', {'color' : 'is-success', 'text' : 'Created User'})
		this.$router.push("/users");
	    } else {
		console.log(result.msg)
	    }
	}
    },
}
</script>
