<script lang="ts">
	import Monaco from 'svelte-monaco';
</script>

<div class="editor-container">
	<Monaco theme="cobalt" value="" options={{ language: 'yaml', automaticLayout: true }} />
</div>

<style>
	.editor-container {
		height: 300px;
		width: 100%;

		border-radius: 2px;
		border: 2px solid rgba(255, 255, 255, 0.1);
	}
</style>
