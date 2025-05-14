<script>
	import { fade } from 'svelte/transition';

	const { list, settings, onchange = () => {} } = $props();
	let name = $derived(list.name);
	let children = $state(list.children);

	function addChild() {
		children.push({
			key: '',
			value: '',
			inline: {}
		});
		handleChange()
	}

	function removeChild(index) {
		children = children.filter((_, i) => i !== index);
	}


	function handleChange(){
		onchange(children)
	}

</script>

<main>
	<div class="button">
		<label for={name}>
			{name}
		</label>
		<button id={name} onclick={addChild}>+</button>
	</div>
	<div class="children">
		{#each children as child, index (child)}
			<div class="child" transition:fade>
				<button
					onclick={() => {
						removeChild(index);
					}}
					>-
				</button>
				{#if true}
					{@const Key = settings.key.icon}
					<Key />
				{/if}
				<input type={settings.key.type}  placeholder={settings.key.placeholder} bind:value={child.key} oninput={() => handleChange()} />
				{#if true}
					{@const Value = settings.value.icon}
					<Value />
				{/if}
				<input type={settings.value.type} placeholder={settings.value.placeholder} bind:value={child.value} onchange={() => handleChange()} />
				{#if true}
					{@const Inline = settings.inlineComponent}
					<Inline inline={child.inline} onchange={handleChange} />
				{/if}
			</div>
		{/each}
	</div>
</main>

<style lang="scss">
	@use '$root/style/pallet.scss';
	main {
		.button {
			display: flex;
			gap: 1rem;
			align-items: center;
			font-size: 1.2rem;
			margin-bottom: 1rem;

			button {
				width: 2rem;
				height: 2rem;

				display: flex;
				justify-content: center;
				align-items: center;

				background-color: pallet.$primary;
				border: none;
				border-radius: 5px;

				color: white;
				font-size: 2rem;
			}
		}

		.child {
			margin-top: 1rem;

			display: flex;
			gap: 0.25rem;
			button {
				background-color: pallet.$primary;
				border: none;
				border-radius: 5px;
				color: white;
				font-size: 1rem;

				transition: 0.5s ease;
				&:hover {
					background-color: pallet.$accent;
				}
			}
		}
	}
</style>
