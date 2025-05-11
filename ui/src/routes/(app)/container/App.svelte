<script>
	import Container from './Container.svelte';

	const { name, id } = $props();

	const container = $state([
		{
			id: 1
		},
		{
			id: 2
		},
		{
			id: 3
		},
		{
			id: 4
		}
	]);
</script>

<main class="app">
	<div class="name">
		<span>{name}</span>
	</div>
	<div class="containers">
		{#each container as id, index  (id)}
			{#if index === 0}
			<Container class="container" {id} isFirst={true} />
			{:else if index === container.length - 1}
			<Container class="container" {id} isLast={true} />
			{:else}
			<Container class="container" {id} />
			{/if}

		{/each}
	</div>
</main>

<style lang="scss">
	@use '$root/style/pallet.scss';
	.app {
		width: 90%;

		display: grid;
		grid-template-columns: minmax(150px, 1fr) 4fr;
		grid-auto-flow: row;
		grid-gap: 0;

		background-color: pallet.$secondary;

		border-radius: 10px;

		.name {
			min-width: 0;

			display: flex;
			justify-content: center;
			align-items: center;

			padding: 0.5rem;
			text-overflow: ellipsis;

			overflow: hidden;

			span {
				max-width: 100%;

				font-size: clamp(0.75rem, 4vw, 1.5rem);

				text-align: center;
				word-wrap: break-word;
				overflow-wrap: break-word;
				word-break: break-word;
			}
		}
	}
</style>
