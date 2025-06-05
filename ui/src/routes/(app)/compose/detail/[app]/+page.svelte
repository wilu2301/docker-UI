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
		Box,
		HardDrive,
		Cog
	} from '@lucide/svelte';
	import { Tooltip } from '@svelte-plugins/tooltips';
	import { settingsState } from '$lib/state/settings.svelte';
	import { getApp, getAppVolumes, getServices } from '$lib/api/api';
	import { slide } from 'svelte/transition';
	import { userState } from '$lib/state/user.svelte';
	import type { components } from '$lib/api/schema';
	import { onMount } from 'svelte';
	import Service from '$root/components/Service.svelte';
	import { notificationState, NotificationType } from '$root/lib/state/notification.svelte';
	import { goto } from '\$app/navigation';
	import App from '$root/routes/(app)/compose/App.svelte';

	const { data }: PageProps = $props();

	type AppOverview = components['schemas']['AppOverview'];
	type Volume = components['schemas']['Volume'];

	let isLoading = $state(true);
	let app: AppOverview = $state();
	let volumes: Volume[] = $state();
	let services: string[] = $state();

	async function fetchData() {
		try {
			// Get general App data
			const appOverview = await getApp({
				app_name: data.name,
				token: userState.token
			});
			app = appOverview.data;

			// Get Volumes
			const appVolumes = await getAppVolumes({
				app_name: data.name,
				token: userState.token
			});
			volumes = appVolumes.data;

			// Get Services

			const appServices = await getServices({
				app_name: data.name,
				token: userState.token
			});

			services = appServices.data;

			isLoading = false;
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
		await fetchData();
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

{#snippet Volume(name, mountpoint, created_at, driver)}
	<tr>
		<td>
			<div class="middle">
				<Box />
				{name}
			</div>
		</td>
		<td>
			<div class="middle">
				<HardDrive />
				{mountpoint}
			</div>
		</td>
		<td>
			<div class="middle">
				<Cog />
				{driver}
			</div>
		</td>
	</tr>
{/snippet}

<main>
	<TopInfoBar title={data.name} loading={isLoading} />
	{#if !isLoading}
		<div class="body" transition:slide={{ duration: 1000 }}>
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
			<Section icon={Cylinder} title="Volumes">
				<table>
					<tbody>
						{#each volumes as volume}
							{@render Volume(volume.name, volume.mountpoint, volume.created_at, volume.driver)}
						{/each}
					</tbody>
				</table>
			</Section>
			<Section icon={Box} title="Container">
				<div class="services">
					{#each services as service}
						<Service appName={data.name} name={service} />
					{/each}
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

				.middle {
					display: flex;
					align-items: center;
					gap: 1rem;
				}

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
