<template>
<div>

<div class="level">
    <div class="level-left">
	<div class="title is-1">
	    Users
	</div>
    </div>
    <div class="level-right">
	<button @click="newUser" class="button is-medium is-link">
	    New User
	</button>
    </div>
</div>

<table class="table">
    <thead>
	<tr>
	    <th>Username</th>
	    <th>Admin?</th>
	    <th>Actions</th>
	</tr>
    </thead>
    <tbody>
	<list-user-element v-for="user in users" v-bind="user" @deleted="handleDelete" :key="user.id"></list-user-element>
    </tbody>
</table>

<div class="title is-1">
    Actions
</div>

<div class="button is-primary" @click="refreshCache" :class="{'is-loading' : refreshCacheLoading}">Refresh Cache</div>
<p> Use this if an item, customer, employee, or term has changed in Netsuite. This will refresh the cache in this tool and allow the new version to be used instead.</p>

<br/>
<br/>
<br/>
<br/>

<div class="title is-1">
    Logs
</div>

<log-msg v-for="log in logs" :log="log"></log-msg>
    
</div>

</template>


<script>

import { getApi } from '../api';

import ListUserElement from '../components/ListUserElement';
import LogMsg from '../components/LogMsg';


export default {
    data: function() {
	return {
	    users: [],
	    logs: [],
	    refreshCacheLoading: false,
	}
    },
    mounted: async function() {
	let result = await getApi('/users');
	this.users = result;

	let logs_result = await getApi('/logs');
	this.logs = logs_result.reverse();

    },
    methods: {
	newUser: function() {
	    this.$router.push("/newUser");
	},
	handleDelete: function(oid) {
	    for(var i = 0; i < this.users.length; i++) {
		if(this.users[i]._id.$oid == oid)
		    this.users.splice(i, 1);
	    }
	},
	refreshCache: async function() {
	    this.refreshCacheLoading = true;
	    let result = await getApi('/cache/refresh')
	    this.refreshCacheLoading = false;
	},
    },
    components: {
	ListUserElement,
	LogMsg
    }
}
</script>
