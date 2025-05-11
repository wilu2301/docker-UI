<script>
	import { CircleCheck, CircleX } from '@lucide/svelte';
	import { fade } from 'svelte/transition';

	const { validator } = $props();

	let name = $derived(validator.name);
	let conditions = $derived(validator.conditions);

	let isValid = $derived(conditions.every((condition) => condition.met));
</script>

<main>
	{#if isValid}
		<div class="valid validator" in:fade>
			<CircleCheck size={45} color="green" />
			<span>{name} Valid</span>
		</div>
	{:else}
		<div class="invalid validator" in:fade>
			<CircleX size={45} color="red" />
			<div class="conditions">
				{#each conditions as condition (condition)}
					<div class:met={condition.met} class:not-met={!condition.met}>
						<span>{condition.goal}</span>
					</div>
				{/each}
			</div>
		</div>
	{/if}
</main>

<style lang="scss">
	@use '$root/style/pallet.scss';

	.validator {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 1rem;

		.conditions {
			.not-met {
				color: pallet.$error;
				&::before {
					content: '✗';
					color: pallet.$error;
				}
			}

			.met {
				color: pallet.$success;
				&::before {
					content: '✓';
					color: pallet.$success;
				}
			}
		}
	}
</style>
