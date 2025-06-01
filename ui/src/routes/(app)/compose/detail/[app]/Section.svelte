<script lang="ts">
	const { children, icon, title } = $props();
</script>

<main>
	<div class="top-bar">
		<div class="icon">
			{#if true}
				{@const Icon = icon}
				<Icon />
			{/if}
		</div>
		<div class="title">
			<h2>{title}</h2>
		</div>
	</div>
	<hr />
	<div class="content">
		{#if children}
			{@render children?.()}
		{/if}
	</div>
</main>

<style lang="scss">
	@use '$root/style/pallet';

	main {
		width: 100%;

		background: pallet.$primary;
		color: pallet.$white;
		border-radius: 20px;

		.top-bar {
			display: flex;
			flex-direction: row;
			align-items: center;
			justify-content: center;
			gap: 1rem;
		}
		.content {
			padding: 2rem;
			display: flex;
			gap: 2rem;
			justify-content: center;
		}
	}
</style>
