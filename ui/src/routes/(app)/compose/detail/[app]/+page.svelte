<script lang="ts">
	import type { PageProps } from './$types';
	import TopInfoBar from '$root/components/TopInfoBar.svelte';
	import Section from '$root/routes/(app)/compose/detail/[app]/Section.svelte';
	import {
		EthernetPort,
		Info,
		ChevronsLeftRightEllipsis,
		PcCase,
		Cylinder,
		Box
	} from '@lucide/svelte';
	import { Tooltip } from '@svelte-plugins/tooltips';
	import { settingsState } from '$lib/state/settings.svelte';
	import { CacheService } from '$lib/utils/cache';
	import { getApp } from '$lib/api/api';
	import { userState } from '$lib/state/user.svelte';
	import type { components } from '$lib/api/schema';
	import { onMount } from 'svelte';
	import Service from '$root/components/Service.svelte';
	import { notificationState, NotificationType } from '$root/lib/state/notification.svelte';
	import { goto } from '\$app/navigation';

	const { data }: PageProps = $props();

	type AppOverview = components['schemas']['AppOverview'];
	type Port = components['schemas']['Port'];

	let isLoading = $state(true);
	let app: AppOverview = $state();

	async function fetchAppData() {
		try {
			const cacheKey = `apps_app_${data.name}`;
			const cachedData = CacheService.get<AppOverview>(cacheKey);

			if (cachedData) {
				app = cachedData;
				isLoading = false;

				console.log('Using cached data');
				return;
			}

			const response = await getApp({
				app_name: data.name,
				token: userState.token
			});
			app = response.data;
			isLoading = false;

			CacheService.set(cacheKey, response.data);
		} catch (error) {
			console.error('Error fetching app:', error);
			if (error.status === 404) {
				// App does not exist
				notificationState.addMessage(`App "${data.name}" does not exist`, NotificationType.ERROR);
				await goto('/compose');
			}
		}
	}

	onMount(async () => {
		if (!userState.token) {
			await new Promise((r) => setTimeout(r, 100));
		}
		await fetchAppData();
	});
</script>

{#snippet Port(port, tcp, udp, ingress)}
	<td>
		<span class="port">
			{#if ingress}
				<Tooltip content="Ingress">
					<ChevronsLeftRightEllipsis />
				</Tooltip>
			{:else}
				<Tooltip content="Host">
					<PcCase />
				</Tooltip>
			{/if}
			<a href={`${settingsState.host}:${port}`} target="_blank">
				{port}
			</a>
			{#if tcp}
				TCP
			{:else if udp}
				UDP
			{/if}
		</span>
	</td>
{/snippet}

<main>
	<TopInfoBar title={data.name} loading={isLoading} />
	{#if !isLoading}
		<div class="body">
			<Section icon={Info} title="General">
				<table>
					<tbody>
						<tr>
							<td class="key">Status:</td>
							<td>{app.status}</td>
						</tr>
						<tr>
							<td class="key">Containers Running:</td>
							<td>{app.usage.containers_running}</td>
						</tr>
						<tr>
							<td class="key">Volumes Count:</td>
							<td>{app.usage.volumes_count}</td>
						</tr>
					</tbody>
				</table>
			</Section>
			<Section icon={EthernetPort} title="Network">
				<table>
					<tbody>
						<tr>
							<td class="key">Ports Exposed:</td>
							{#each app.usage.ports_exposed as port}
								{@render Port(port.public_port, port.tcp, port.udp, port.ingress)}
							{/each}
						</tr>
						<tr>
							<td class="key">Networks</td>
							<td></td>
						</tr>
					</tbody>
				</table>
			</Section>
			<Section icon={Cylinder} title="Volumes"></Section>
			<Section icon={Box} title="Container">
				<div class="services">
					<Service name="BusyBox" />
					<Service name="BusyBox" />
				</div>
			</Section>
		</div>
	{/if}
</main>

<style lang="scss">
	@use '$root/style/pallet';

	main {
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;

		.body {
			width: 90%;
			padding: 20px;

			display: flex;
			flex-direction: column;
			gap: 2rem;

			table {
				width: 60%;

				.key {
					font-weight: bold;
				}
				.port {
					display: flex;
					flex-direction: row;
					justify-content: center;
					align-items: center;
					gap: 1rem;

					a {
						text-decoration: none;
						color: pallet.$accent;

						transition: 0.5s;
						&:hover {
							text-decoration: underline;
						}
					}
				}
			}
		}
	}
	.services {
		width: 100%;
		display: flex;
		flex-direction: column;
		gap: 2rem;
	}
</style>
