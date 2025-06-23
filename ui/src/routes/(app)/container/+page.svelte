<script>
</script>

<main>
	<h1>Container</h1>
	<div class="apps">
		<h2>Under Construction</h2>
	</div>
</main>

<style lang="scss">
	@use '$root/style/pallet.scss';
	main {
		background-color: pallet.$background;
		padding: 2rem;
		width: calc(100% - 4rem);
		height: calc(100vh - 4rem);
	}
	.apps {
		row-gap: 1rem;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;

		background-color: pallet.$background;
	}
</style>
