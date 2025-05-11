<script>
	const { field, onchange } = $props();

	let name = $derived(field.name);
	let placeholder = $derived(field.placeholder);
</script>

<main>
	<div class="field">
		<label for={name}>{name}</label>
		<input type="text" id={name} {placeholder} oninput={(e) => onchange(e.target.value)} />
	</div>
</main>

<style lang="scss">
	@use '$root/style/pallet.scss';

	main {
		width: 70%;
		.field {
			width: 100%;
			display: flex;
			flex-direction: row;
			justify-content: flex-start;
			align-items: center;
			gap: 1rem;
		}

		label {
			font-size: 1.5rem;
			width: 150px;
			text-align: right;
			flex-shrink: 0;
		}

		input {
			width: 70%;
			height: 3rem;
			padding: 0 1rem;
			border: 1px solid pallet.$black;
			border-radius: 4px;
			box-sizing: border-box;
		}
	}
</style>
