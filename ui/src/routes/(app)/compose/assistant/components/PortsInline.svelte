<script>
	let { inline } = $props();
	let tcp = $derived(inline.tcp);
	let udp = $derived(inline.udp);

	function handleChange(){
		if (onchange) onchange()
	}

function changeTcp(){
	tcp = !tcp
	handleChange()
}
	function changeUdp(){
		tcp = !tcp
		handleChange()
	}
</script>

<main>
	<button class:selected={tcp} onclick={changeTcp} >TCP</button>
	<button class:selected={udp} onclick={changeUdp}>UDP</button>
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
