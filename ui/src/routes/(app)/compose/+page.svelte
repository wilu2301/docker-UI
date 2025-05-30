<script lang="ts">
	import { fade } from 'svelte/transition';
	import App from '$root/routes/(app)/compose/App.svelte';
	import { Loader } from '@lucide/svelte';
	import { CacheService } from '$lib/utils/cache.js';
	import { getApps } from '$lib/api/api.js';
	import { userState } from '$lib/state/user.svelte';
	import { onMount } from 'svelte';
	import type { components } from '$lib/api/schema';

	type App = components['schemas']['App'];

	let apps: App[] = $state();
	let loading = $state(true);

	let appsLoaded = 0;
	function appLoaded() {
		appsLoaded += 1;

		if (appsLoaded === apps.length) {
			loading = false;
			return;
		}
	}

	async function fetchApps() {
		try {
			const response = await getApps({
				token: userState.token
			});
			apps = response.data;
		} catch (error) {
			console.error('Error fetching app:', error);
		}
	}

	onMount(async () => {
		if (!userState.token) {
			await new Promise((r) => setTimeout(r, 100));
		}
		await fetchApps();
	});
</script>

<main>
	<div class="overview">
		{#if loading}
			<div class="loader">
				<Loader />
			</div>
			<h2>fetching Apps</h2>
		{:else}
			<h1>Apps</h1>
		{/if}
	</div>
	<div class="apps">
		{#each apps as app}
			<App appName={app.name} {appLoaded} />
		{/each}
	</div>
</main>

<style lang="scss">
	@use '$root/style/pallet.scss';

	main {
		width: 100%;

		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;

		.overview {
			height: 4rem;
			width: 80%;

			display: flex;
			justify-content: center;
			align-items: center;
			gap: 1rem;

			background: pallet.$primary;
			color: pallet.$white;

			border-radius: 0 0 20px 20px;
		}

		.apps {
			padding: 1rem;

			display: flex;
			flex-flow: row wrap;
			justify-content: center;
			gap: 1rem;
		}
	}

	.loader {
		display: flex;
		align-items: center;
		justify-content: center;
		animation: spin 2s infinite ease-in-out;
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
