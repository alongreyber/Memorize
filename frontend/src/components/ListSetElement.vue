<template>
    <div class="card">
	<div class="card-content columns">
	    <div class="col is-size-4">
		{{ name }}
	    </div>
	    <div class="col has-text-dark" >
		{{ num_cards }} cards
	    </div>
	</div>
    </div>
</template>

<script>
import { getApi } from '../api';

export default {
    props: ['name', 'language', 'num_cards', '_id']
}
</script>

<style>
</style>
