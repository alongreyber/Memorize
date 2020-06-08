<template>
<div class="message" :class="'is-' + color">
    <div class="message-header">
	{{log.msg.action ? log.msg.action : log.msg}}
    </div>
    <div class="message-body">
	<div :id=" 'jsoneditor-' + log._id.$oid" style="width: 100%; height: 400px;"></div>
    </div>
</div>
</template>

<script>
import JSONEditor from 'jsoneditor';
// Add styling for json editor
import 'jsoneditor/dist/jsoneditor.css';

export default {
    props: ['log'],
    mounted: function() {
        const container = document.getElementById("jsoneditor-" + this.log._id.$oid)
        const options = {}
        const editor = new JSONEditor(container, options)
        editor.set(this.log)
    },
    computed: {
	color: function() {
	    if(this.log.levelno >= 40)
		return 'danger'
	    if(this.log.levelno >= 30)
		return 'warning'
	    else
		return 'success'
	}
    }
}
</script>
