<script>
	import Container from './Container.svelte';
</script>

<main class="app">
	<div class="name">
		<h1>App</h1>
	</div>
	<div class="containers">
		<Container isFirst={true} />
		<Container />
		<Container isLast={true} />
	</div>
</main>

<style lang="scss">
	@use '$root/style/pallet.scss';
	.app {
		width: 90%;

		display: grid;
		grid-template-columns: 1fr 4fr;


		background-color: pallet.$secondary;
		border-radius: 10px;

		.name {
			display: flex;
			justify-content: center;
			align-items: center;
		}
	}
</style>
