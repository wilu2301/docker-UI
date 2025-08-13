<script>
	import TopInfoBar from '$root/components/TopInfoBar.svelte';
	import { getAppConfig, getContainerLogs } from '$lib/api/api.js';
	import { userState } from '$lib/state/user.svelte.js';
	import { notificationState, NotificationType } from '$lib/state/notification.svelte.js';
	import { onMount } from 'svelte';
	import Monaco from 'svelte-monaco';

	let { data } = $props();
	let isLoading = $state(true);
	let logs = $state();

	async function fetchData() {
		try {
			// Get general App data
			const containerLogs = await getContainerLogs({
				container_id: data.name,
				token: userState.token
			});

			logs = containerLogs.data.logs;
			isLoading = false;
		} catch (error) {
			console.error('Error loading container logs:', error);
			if (error.status === 404) {
				// Container does not exist
				notificationState.addMessage(
					`Container  "${data.name}" does not exist`,
					NotificationType.WARNING
				);
			}
		}
	}

	onMount(async () => {
		if (!userState.token) {
			await new Promise((r) => setTimeout(r, 100));
		}
		await fetchData();
	});
</script>

<main>
	<TopInfoBar title={data.name} loading={isLoading} id="top" />

	<div class="logs">
		{#if !isLoading}
			<Monaco
				theme="cobalt"
				bind:value={logs}
				options={{ language: 'log', automaticLayout: false, readOnly: true }}
			/>
		{/if}
	</div>
</main>

<style>
	main {
		width: 100%;
		height: 100vh;
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	.logs {
		margin-top: 4rem;

		width: 80%;
		height: 48rem;
	}
</style>
