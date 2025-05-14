<script>
	import { fade } from 'svelte/transition';

	const { list, settings } = $props();
	let name = $derived(list.name);
	let children = $state(list.children);

	function addChild() {
		children.push({
			key: '',
			value: ''
		});
	}

	function removeChild(index) {
		children = children.filter((_, i) => i !== index);
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
				<input type="text" placeholder={settings.key.placeholder} />
				{#if true}
					{@const Value = settings.value.icon}
					<Value />
				{/if}
				<input type="text" placeholder={settings.value.placeholder} />
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
