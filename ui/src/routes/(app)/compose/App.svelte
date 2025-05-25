<script lang="ts">
	import { Dot, Cpu, MemoryStick, Box, EthernetPort, Cylinder } from '@lucide/svelte';
	import type { AppState } from './types';
	import { AppStatus } from './types';
	import { Tooltip } from '@svelte-plugins/tooltips';

	let app: AppState = $state({
		status: AppStatus.Stopped,
		name: 'App Name',
		cpuUsage: 0,
		memoryUsage: 0,
		containerCount: 0,
		portsCount: 0,
		volumesCount: 0
	});
</script>

<main class="app">
	<div class="head">
		{#if app.status === AppStatus.Running}
			<Tooltip content="Running">
				<Dot class="status running" size={64} style="color: var(--success)" />
			</Tooltip>
		{:else}
			<Tooltip content="Running">
				<Dot class="status running" size={64} style="color: var(--error)" />
			</Tooltip>
		{/if}
		<h2>{app.name}</h2>
	</div>
	<div class="body">
		<ul>
			<li>
				<Cpu class="icon" />
				<span>{app.cpuUsage}%</span>
			</li>
			<li>
				<MemoryStick class="icon" />
				<span>{app.memoryUsage} MiB</span>
			</li>
			<li>
				<Box class="icon" />
				<span>{app.containerCount}</span>
			</li>
			<li>
				<EthernetPort class="icon" />
				<span>{app.portsCount}</span>
			</li>
			<li>
				<Cylinder class="icon" />
				<span>{app.volumesCount}</span>
			</li>
		</ul>
	</div>
</main>

<style lang="scss">
	@use '$root/style/pallet';
	.app {
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

					span {
						color: pallet.$text;
					}
				}
			}
		}
	}
</style>
