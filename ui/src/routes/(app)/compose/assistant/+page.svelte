<script>
	import { ChevronLeft, ChevronRight } from '@lucide/svelte';
	import {fade} from 'svelte/transition';

	import Step1 from '$root/routes/(app)/compose/assistant/steps/Step1.svelte';
	import Step2 from '$root/routes/(app)/compose/assistant/steps/Step2.svelte';

	let stage = $state(1);

	function nextStage() {
		stage += 1;
	}

	function previousStage() {
		stage -= 1;
	}
</script>

<main>
	<div class="top-bar">
		<ChevronLeft size={48} />
		<h1>Assistant:</h1>
		<div class="stage">
			<h1 class="number">Step {stage}</h1>
			<h1>Create</h1>
		</div>
	</div>
	<div class="content" in:fade>
		{#if stage === 1}
			<Step1/>
		{:else if stage === 2}
			<Step2 />
		{/if}
	</div>
	<div class="controls">
		<div class="buttons">
			{#if stage > 1}
				<button onclick={previousStage}>
					<ChevronLeft />
					Previous
				</button>
			{/if}
			<button onclick={nextStage}>
				Next
				<ChevronRight />
			</button>
		</div>
	</div>
</main>

<style lang="scss">
	@use '$root/style/pallet.scss';
	main {
		padding: 2rem;

		.top-bar {
			width: 100%;
			height: 5rem;

			display: flex;
			flex-direction: row;
			justify-content: left;
			gap: 1rem;
			align-items: center;

			background: pallet.$secondary;
			border-radius: 1rem;

			.stage {
				display: flex;
				gap: 1rem;

				.number {
					background-color: pallet.$accent;
					padding: 0 1rem;
					border-radius: 8rem;
				}
			}
		}
		.content {
			width: 100%;
			margin: 1rem;

			display: flex;
			justify-content: center;
			align-items: center;
			flex-direction: column;
			gap: 2rem;

			.line {
				width: 90%;
				display: flex;
				justify-content: flex-start;
				align-items: center;
				flex-direction: row;

				.center {
					width: 100%;
					display: flex;
					justify-content: center;
					align-items: center;
				}
			}
		}
		.controls {
			position: absolute;
			bottom: 1rem;
			right: 1rem;

			.buttons {
				display: flex;
				flex-direction: row;
				gap: 1rem;
				button {
					width: 10rem;
					height: 3rem;

					display: flex;
					justify-content: center;
					align-items: center;

					background: pallet.$primary;
					color: pallet.$white;
					border-radius: 4px;
					border: none;
					cursor: pointer;
				}
				:hover {
					transition: background-color 0.3s;
					background-color: pallet.$accent;
				}
			}
		}
	}
</style>
