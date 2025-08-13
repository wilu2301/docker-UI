<script lang="ts">
	import { Bot, CirclePlus } from '@lucide/svelte';
	import App from '$root/routes/(app)/compose/App.svelte';
	import { getApps } from '$lib/api/api.js';
	import { userState } from '$lib/state/user.svelte';
	import { onMount } from 'svelte';
	import type { components } from '$lib/api/schema';
	import { Tooltip } from '@svelte-plugins/tooltips';
	import { goto } from '$app/navigation';
	import TopInfoBar from '$root/components/TopInfoBar.svelte';
	import { notificationState, NotificationType } from '$root/lib/state/notification.svelte';

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

			if (response.data.length === 0) {
				loading = false;
			}
		} catch (error) {
			console.error('Error fetching app:', error);
			notificationState.addMessage(`Error fetching apps: "${error}"`, NotificationType.ERROR);
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
	<TopInfoBar title="Apps" {loading} />
	<div class="apps">
		{#each apps as app}
			<App appName={app.name} {appLoaded} />
		{/each}
	</div>

	<div class="floating-action-button">
		<Tooltip content="Create with assistant" position="left">
			<button class="disabled">
				<Bot />
			</button>
		</Tooltip>
		<Tooltip content="Create new app" position="left">
			<button onclick={() => goto('/compose/new')}>
				<CirclePlus />
			</button>
		</Tooltip>
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

		.apps {
			padding: 1rem;

			display: flex;
			flex-flow: row wrap;
			justify-content: center;
			gap: 1rem;
		}

		.floating-action-button {
			position: fixed;
			bottom: 2rem;
			right: 2rem;

			display: flex;
			flex-direction: column;
			gap: 0.5rem;

			.disabled {
				opacity: 0.5;
				pointer-events: none;
			}

			button {
				background-color: pallet.$primary;
				color: pallet.$white;
				border: none;
				border-radius: 50%;
				width: 3rem;
				height: 3rem;
				display: flex;
				align-items: center;
				justify-content: center;

				transition: 0.5s;
				&:hover {
					transform: scale(1.2);
				}
			}
		}
	}
</style>
