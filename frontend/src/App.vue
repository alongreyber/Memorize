<template>
  <div id="app">
      <nav v-if="loggedIn" class="navbar is-primary">
	  <div class="navbar-brand">
	    <div class="navbar-item has-text-weight-bold">
		Memorize App
	    </div>
	  </div>

	  <div class="navbar-menu">
	    <div class="navbar-start">
		<a class="navbar-item" @click="$router.push('/')">
		    My Sets
		</a>
		<a class="navbar-item" v-if="this.$store.state.user.is_admin" @click="$router.push('/users')">
		    Users
		</a>
	    </div>

	    <div class="navbar-end">
	      <div class="navbar-item">
		  Welcome {{ $store.state.user.username }}
	      </div>
	      <div class="navbar-item">
		<div class="buttons">
		  <button class="button is-light" v-on:click="logOut()">
		    Log Out
		  </button>
		</div>
	      </div>
	    </div>
	  </div>
	</nav>
      <div class="container" id="main-container">
	  <div class="modal" :class="{'is-active' : $store.state.modal }">
	      <div class="modal-background"></div>
	      <div class="modal-card">
		  <header class="modal-card-head">
		      <p class="modal-card-title">{{ $store.state.modal ? $store.state.modal.title : '' }}</p>
		      <button class="delete" @click="$store.commit('clearModal')"></button>
		  </header>
		  <section class="modal-card-body">
		      {{ $store.state.modal ? $store.state.modal.text : '' }}
		  </section>
	      </div>
	  </div>
	  <div v-for="n in $store.state.messages" class="notification" :class="n.color">
	      <button class="delete" @click="$store.commit('clearMessage', n)"></button>
	      {{ n.text }}
	  </div>
	
	<router-view/>
      </div>
  </div>
</template>

<style lang="scss">

#main-container {
    margin-top: 40px;
}
</style>

<script>

import { getApi } from './api';

export default {
    computed: {
	loggedIn() {
	    return this.$store.state.loggedIn;
	}
    },
    methods: {
	async logOut() {
	    let result = await getApi('/logout');
	    if( result.status == 'ok' ) {
		this.$store.commit('logOut');
		this.$router.push("/login");
	    }
	}
    }
}
</script>
