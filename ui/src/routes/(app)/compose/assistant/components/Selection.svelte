<script>
	const { selection, onchange } = $props();
	let options = $derived(selection.options);
</script>

<main>
	<div class="buttons">
		<span>{selection.name}</span>
		{#each options as option (option)}
			<button
				class="option"
				onclick={() => onchange(option)}
				class:selected={option === selection.value}
			>
				{option}
			</button>
		{/each}
	</div>
</main>

<style lang="scss">
	@use '$root/style/pallet';

	main {
		width: 80%;

		span {
			font-size: 1.5rem;
			width: 150px;
			text-align: right;
			flex-shrink: 0;
		}

		.buttons {
			display: flex;
			flex-direction: row;
			justify-content: flex-start;
			align-items: center;
			gap: 1rem;

			.selected {
				background-color: pallet.$selected;
			}

			button {
				width: 100%;
				padding: 1rem;
				border: 1px solid black;
				border-radius: 4px;
				background-color: white;
				cursor: pointer;
			}
		}
	}
</style>
