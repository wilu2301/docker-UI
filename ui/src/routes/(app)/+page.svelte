<script lang="ts">
	import { ping } from '$lib/api/api';

	const apiCallPromise: Promise<{ data?: any; error?: any; response: Response }> = ping();
</script>

<main>
	<div class="dashboard">
		<h1>Dashboard</h1>
		<p>Welcome to the dashboard!</p>
		{#await apiCallPromise}
			<p>Loading</p>
		{:then result}
			{result.data.ping}
		{/await}
	</div>
</main>

<style lang="scss">
	@use '../../style/pallet';
	.dashboard {
		padding: 2rem;
		background-color: pallet.$background;
		height: calc(100vh - 4rem);
	}
</style>
