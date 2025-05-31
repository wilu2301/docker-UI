<script lang="ts">
	const { children, icon } = $props();
</script>

<main>
	<div class="icon">
		{#if true}
			{@const Icon = icon}
			<Icon />
		{/if}
	</div>
	{@render children?.()}
</main>

<style>
	main {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 1rem;
	}
</style>
