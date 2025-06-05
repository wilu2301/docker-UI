<script>
	import Container from './Container.svelte';
	import { getServiceContainers } from '$lib/api/api.js';
	import { notificationState, NotificationType } from '$lib/state/notification.svelte.js';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { userState } from '$lib/state/user.svelte.js';

	const { appName, name } = $props();

	let container = $state();
	$inspect(container);

	async function fetchData() {
		try {
			const containerData = await getServiceContainers({
				app_name: appName,
				service_name: name.split('_')[name.split('_').length - 1],
				token: userState.token
			});

			container = containerData.data;
		} catch (error) {
			console.error('Error fetching containerData:', error);
		}
	}

	onMount(async () => {
		if (!userState.token) {
			await new Promise((r) => setTimeout(r, 100));
		}
		await fetchData();
	});
</script>

<main class="app">
	<div class="name">
		<span>{name.split('_')[name.split('_').length - 1]}</span>
	</div>
	<div class="container">
		{#each container as c, index (c)}
			{#if container.length === 1}
				<Container class="container" container={c} isLast={true} />
			{:else if index === 0}
				<Container class="container" container={c} isFirst={true} />
			{:else if index === container.length - 1}
				<Container class="container" container={c} isLast={true} />
			{:else}
				<Container class="container" container={c} />
			{/if}
		{/each}
	</div>
</main>

<style lang="scss">
	@use '$root/style/pallet';
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
