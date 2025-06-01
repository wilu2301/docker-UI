<script>
	import { Dot, ScrollText, ChevronRight, Info, RotateCcw } from '@lucide/svelte';
	import { Tooltip } from '@svelte-plugins/tooltips';

	const { isFirst, isLast, container_id } = $props();

	const ContainerState = {
		RUNNING: 'running',
		STOPPED: 'stopped',
		STARTING: 'starting'
	};

	let container_state = $state(ContainerState.RUNNING);
</script>

<main>
	<div class:first={isFirst} class:last={isLast} class:middle={!isFirst && !isLast}>
		<div class="container">
			<div class="container-state">
				{#if container_state === ContainerState.RUNNING}
					<Tooltip content="Running">
						<Dot class="status" size="100" color="green" />
					</Tooltip>
				{:else if container_state === ContainerState.STARTING}
					<Tooltip content="Starting">
						<Dot class="status" size="100" color="yellow" />
					</Tooltip>
				{:else if container_state === ContainerState.STOPPED}
					<Tooltip content="Stopped">
						<Dot class="status" size="100" color="red" />
					</Tooltip>
				{/if}
			</div>
			<span class="name">Container</span>
			<div class="actions">
				<Tooltip content="Logs">
					<ScrollText class="action" size="32" color="var(--white)" />
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
			<span class="node">Node</span>
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
