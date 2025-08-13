<script lang="ts">
	import { Dot, ScrollText, ChevronRight, Info, RotateCcw } from '@lucide/svelte';
	import { Tooltip } from '@svelte-plugins/tooltips';
	import type { components } from '$lib/api/schema.js';
	import { goto } from '\$app/navigation';

	type ContainerOverview = components['schemas']['ContainerOverview'];

	const { isFirst, isLast, container } = $props<{
		isFirst: boolean;
		isLast: boolean;
		container: ContainerOverview;
	}>();


	function getLogs(){
		goto(`/container/logs/${container.name}`)
	}
</script>

<main>
	<div class:first={isFirst} class:last={isLast} class:middle={!isFirst && !isLast}>
		<div class="container">
			<div class="container-state">
				{#if container.status === 'running'}
					<Tooltip content="Running">
						<Dot class="status" size="100" color="green" />
					</Tooltip>
				{:else if container.status === 'created'}
					<Tooltip content="status">
						<Dot class="status" size="100" color="yellow" />
					</Tooltip>
				{:else if container.status === 'dead' || container.status === 'exited'}
					<Tooltip content="Stopped">
						<Dot class="status" size="100" color="red" />
					</Tooltip>
				{/if}
			</div>
			<span class="name">{container.name}</span>
			<div class="actions">
				<Tooltip content="Logs">
					<ScrollText class="action" size="32" color="var(--white)" onclick={getLogs} />
				</Tooltip>
				<Tooltip content="Attach">
					<ChevronRight class="action" size="32" color="var(--white)" />
				</Tooltip>
				<Tooltip content="Info">
					<Info class="action" size="32" color="var(--white)" />
				</Tooltip>
				<Tooltip content="Restart">
					<RotateCcw class="action" size="32" color="var(--white)" />
				</Tooltip>
			</div>
			<span class="node">{container.node}</span>
		</div>
	</div>
</main>

<style lang="scss">
	@use '$root/style/pallet';

	.first {
		background-color: pallet.$primary;
		border-top-right-radius: 10px;

		border-bottom: white solid 1px;
	}

	.middle {
		background-color: pallet.$primary;
		border-bottom: none;
		border-bottom: white solid 1px;
	}

	.last {
		background-color: pallet.$primary;
		border-bottom: none;
		border-bottom-right-radius: 10px;
	}
	main {
		width: 100%;

		.container {
			background-color: pallet.$primary;
			width: 90%;
			display: flex;
			flex-direction: row;
			justify-content: space-between;
			align-items: center;
			.container-state {
				:global(.tooltip) {
					margin-top: -40px !important;
				}
			}

			.actions {
				display: flex;
				flex-direction: row;
				gap: 1rem;
			}

			span {
				font-size: 1.2rem;
				color: pallet.$white;
			}
		}
	}
</style>
