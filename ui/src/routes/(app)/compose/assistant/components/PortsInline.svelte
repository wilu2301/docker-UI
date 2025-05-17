<script>
	let { inline, onchange = () => {} } = $props();
	$effect(() => {
		if (inline.tcp == null) {
			inline.tcp = false;
		}
		if (inline.udp == null) {
			inline.udp = false;
		}
	});

	function handleChange() {
		if (onchange) onchange();
	}

	function changeTcp() {
		inline.tcp = !inline.tcp;
		handleChange();
	}
	function changeUdp() {
		inline.udp = !inline.udp;
		handleChange();
	}
</script>

<main>
	<button class:selected={inline.tcp} onclick={changeTcp}>TCP</button>
	<button class:selected={inline.udp} onclick={changeUdp}>UDP</button>
	{#if inline.notAvailable}
		<span id="error">Port not available</span>
	{/if}
</main>

<style lang="scss">
	@use '$root/style/pallet.scss';
	button {
		height: 100%;

		background-color: pallet.$primary;
		border: none;
		border-radius: 5px;
		color: white;
		font-size: 1rem;

		transition: 0.5s ease;
		&:hover {
			background-color: pallet.$secondary;
			color: pallet.$text;
		}
	}
	.selected {
		background-color: pallet.$secondary;
		color: pallet.$text;
	}

	#error {
		color: pallet.$error;
	}
</style>
