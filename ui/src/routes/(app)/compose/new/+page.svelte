<script>
	import Monaco from 'svelte-monaco';
</script>

<main>
	<div class="top">
		<h1>New App</h1>
		<input type="text" placeholder="App Name" />
		<select>
			<option> Git </option>
			<option> Local </option>
		</select>
	</div>
	<div class="code">
		<Monaco theme="cobalt" options={{ language: 'yaml', automaticLayout: true }} />
	</div>
</main>

<style>
	main {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 16px;
		height: 100%;
		width: 100%;

		.code {
			width: 80%;
			height: 32rem;
		}
	}
</style>
