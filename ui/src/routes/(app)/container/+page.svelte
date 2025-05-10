<script>
	import App from './App.svelte';
</script>

<main>
	<div class="apps">
		<App class="app" />
		<App class="app" />
		<App class="app" />
	</div>
</main>

<style lang="scss">
		@use '$root/style/pallet.scss';
	main {
		background-color: pallet.$background;
		width: 100%;
		height: 100vh;
	}
	.apps {
		height: 100%;

    row-gap: 1rem;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
</style>
