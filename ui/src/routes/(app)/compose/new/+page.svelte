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
	<div class="stack">
		<div class="files">
			<div class="file">
				<span>app.yaml</span>
			</div>
			<div class="file">
				<span>app.yaml</span>
			</div>
		</div>
		<div class="code">
			<Monaco theme="cobalt" value="" options={{ language: 'yaml', automaticLayout: true }} />
			<input type="text" placeholder="App Name" /> <span>.yaml</span>
			<button>Add File</button>
			<button>Deploy</button>
		</div>
	</div>
	<h3 style="color: red; font-weight: bolder">Work in progress</h3>
</main>

<style lang="scss">
	@use '$root/style/pallet';
	main {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 16px;
		height: 100%;
		width: 100%;

		.stack {
			display: flex;
			flex-direction: column;
			justify-content: center;
			align-items: center;
			width: 100%;
			height: 100%;

			.files {
				display: flex;
				gap: 4rem;
			}

			.code {
				width: 80%;
				height: 32rem;

				background: pallet.$primary;
			}
		}
	}
</style>
