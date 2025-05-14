<script>
	const { field, onchange } = $props();

	let name = $derived(field.name);
	let placeholder = $derived(field.placeholder);
	let value = $derived(field.value);
	let type = $derived(field.type);
</script>

<main>
	<div class="field">
		<label for={name}>{name}</label>
		<input {type} id={name} {placeholder} {value} oninput={(e) => onchange(e.target.value)} />
	</div>
</main>

<style lang="scss">
	@use '$root/style/pallet';

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
