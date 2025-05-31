<script>
	import { Loader } from '@lucide/svelte';

	const { loading, title } = $props();
</script>

<div class="top-bar">
	{#if loading}
		<div class="loader">
			<Loader />
		</div>
		<h2>fetching..</h2>
	{:else}
		<h1>{title}</h1>
	{/if}
</div>

<style lang="scss">
	@use '$root/style/pallet';

	.top-bar {
		height: 4rem;
		width: 80%;

		display: flex;
		justify-content: center;
		align-items: center;
		gap: 1rem;

		background: pallet.$primary;
		color: pallet.$white;

		border-radius: 0 0 20px 20px;

		.loader {
			display: flex;
			align-items: center;
			justify-content: center;
			animation: spin 2s infinite ease-in-out;
		}
	}

	@keyframes spin {
		from {
			transform: rotate(0deg);
		}
		to {
			transform: rotate(360deg);
		}
	}
</style>
