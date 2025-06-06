<script lang="ts">
	import { Dot, Cpu, MemoryStick, Box, EthernetPort, Cylinder } from '@lucide/svelte';
	import { Tooltip } from '@svelte-plugins/tooltips';
	import { fade } from 'svelte/transition';
	import { getApp } from '$lib/api/api';
	import { userState } from '\$root/lib/state/user.svelte';
	import { CacheService } from '$lib/utils/cache';
	import type { components } from '$lib/api/schema';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	type AppOverview = components['schemas']['AppOverview'];

	const { appName, appLoaded = () => {} } = $props();

	let isLoading = $state(true);

	let app: AppOverview = $state({
		name: 'Loading',
		status: 'running',
		usage: {
			cpu_usage: 0,
			memory_usage: 0,
			containers_running: 0,
			volumes_count: 0,
			ports_exposed: []
		}
	});

	async function fetchAppData(appName: string) {
		try {
			const cacheKey = `apps_app_${appName}`;
			const cachedData = CacheService.get<AppOverview>(cacheKey);

			if (cachedData) {
				app = cachedData;
				isLoading = false;
				appLoaded();

				console.log('Using cached data');
				return;
			}

			const response = await getApp({
				app_name: appName,
				token: userState.token
			});
			app = response.data;
			isLoading = false;
			appLoaded();
			CacheService.set(cacheKey, response.data);
		} catch (error) {
			console.error('Error fetching app:', error);
		}
	}

	function seeDetails() {
		goto(`/compose/detail/${appName} `);
	}

	onMount(async () => {
		if (!userState.token) {
			await new Promise((r) => setTimeout(r, 100));
		}
		await fetchAppData(appName);
	});
</script>

{#if !isLoading}
	<button class="app" transition:fade onclick={seeDetails}>
		<div class="head">
			{#if app.status === 'running'}
				<Tooltip content="Running">
					<Dot class="status" size={64} style="color: var(--success)" />
				</Tooltip>
			{:else if app.status === 'degraded'}
				<Tooltip content="Degraded">
					<Dot class="status" size={64} style="color: var(--warning)" />
				</Tooltip>
			{:else}
				<Tooltip content="Unknown">
					<Dot class="status" size={64} style="color: var(--white)" />
				</Tooltip>
			{/if}
			<h2>{app.name}</h2>
		</div>
		<div class="body">
			<ul>
				<li>
					<Cpu class="icon" />
					<span>{app.usage.cpu_usage}%</span>
				</li>
				<li>
					<MemoryStick class="icon" />
					<span>{app.usage.memory_usage} MiB</span>
				</li>
				<li>
					<Box class="icon" />
					<span>{app.usage.containers_running}</span>
				</li>
				<li>
					<EthernetPort class="icon" />
					<span>{app.usage.ports_exposed.length}</span>
				</li>
				<li>
					<Cylinder class="icon" />
					<span>{app.usage.volumes_count}</span>
				</li>
			</ul>
		</div>
	</button>
{/if}

<style lang="scss">
	@use '$root/style/pallet';
	.app {
		padding: 0;
		border: none;

		width: max-content;
		display: flex;
		justify-content: center;
		flex-direction: column;

		border-radius: 0.5rem;
		background-color: pallet.$secondary;

		.head {
			display: flex;
			align-items: center;

			border-top-left-radius: 0.5rem;
			border-top-right-radius: 0.5rem;
			background-color: pallet.$primary;

			:global(.tooltip) {
				margin-top: 40px !important;
			}

			h2 {
				color: pallet.$white;
				margin-right: 2rem;
			}
		}
		.body {
			display: flex;
			flex-direction: column;
			padding: 1rem;

			ul {
				padding: 0;
				margin: 0;

				display: flex;
				flex-direction: column;
				gap: 0.5rem;

				list-style: none;

				li {
					display: flex;
					align-items: center;
					gap: 0.5rem;

					.icon {
						color: pallet.$text;
					}
				}
			}
		}

		transition: 0.5s ease;
		&:hover {
			color: pallet.$white;
			transform: scale(1.1);
			background-color: pallet.$selected;
		}
	}
</style>
