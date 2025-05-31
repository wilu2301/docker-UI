<script lang="ts">
	import type { PageProps } from './$types';
	import TopInfoBar from '$root/components/TopInfoBar.svelte';
	import Section from '$root/routes/(app)/compose/detail/[app]/Section.svelte';
	import { Info } from '@lucide/svelte';

	const { data }: PageProps = $props();
</script>

<main>
	<TopInfoBar title={data.name} loading={false} />

	<div class="body">
		<Section icon={Info}>
			<h2>General</h2>
		</Section>
	</div>
	<div class="network">
		<h2>Networking</h2>
	</div>
	<div class="Volumes">
		<h2>Networking</h2>
	</div>
</main>

<style>
	main {
		width: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}
</style>
