<template>
<div>
    <div class="title is-1">
	Login
    </div>

    <div class="field">
      <label class="label">Username</label>
      <div class="control">
	<input class="input" type="text" v-model="username" v-on:input="clearErrors" v-on:keyup.enter="login()" :autofocus="'autofocus'" >
      </div>
      <p class="help is-danger is-size-6" v-if="usernameErr">Username is required</p>
    </div>
    <div class="field">
      <label class="label">Password</label>
      <div class="control">
	<input class="input" type="password" v-model="password" v-on:input="clearErrors" v-on:keyup.enter="login()">
      </div>
      <p class="help is-danger is-size-6" v-if="passwordErr">Password is required</p>
    </div>

    <div class="field">
      <p class="control">
	<button class="button is-success" v-on:click="login()" v-on:keyup.enter="login()">
	  Login
	</button>
      </p>
      <p class="help is-danger is-size-6" v-if="responseErr">Incorrect Username or Password</p>
    </div>
</div>

</template>

<script>

import { postApiJson } from '../api.js';

export default {
    name: 'Login',
    data: function() {
	return {
	    username: "",
	    usernameErr: false,
	    password: "",
	    passwordErr: false,
	    responseErr: false,
	}
    },
    methods: {
	clearErrors: function() {
	    this.usernameErr = false;
	    this.passwordErr = false;
	    this.responseErr = false;
	},
	login: async function() {
	    if(!this.username) {
		this.usernameErr = true;
		return;
	    }
	    if(!this.password) {
		this.passwordErr = true;
		return;
	    }
	    let loginData = { username: this.username, password: this.password };
	    let result = await postApiJson('/login', loginData);
	    if( !result.error ) {
		this.$store.commit("logIn", result.user);
		this.$router.push("/");
	    } else {
		this.responseErr = true;
	    }
	}
    }
}
</script>
