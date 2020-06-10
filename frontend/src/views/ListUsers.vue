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

</div>
</template>

<script>

import { getApi } from '../api';

import ListUserElement from '../components/ListUserElement';

export default {
    data: function() {
	return {
	    users: [],
	}
    },
    mounted: async function() {
	let result = await getApi('/users');
	this.users = result;
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
    },
    components: {
	ListUserElement
    }
}
</script>
