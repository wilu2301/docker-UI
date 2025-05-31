<script module>
	import { defineMeta } from '@storybook/addon-svelte-csf';
	import Section from '$root/routes/(app)/compose/detail/[app]/Section.svelte';
	import { Info } from '@lucide/svelte';

	const { Story } = defineMeta({
		title: 'Section',
		component: Section
	});
</script>

<Story name="Normal">
	<Section title="Info" icon={Info}>
		<h2>General</h2>
	</Section>
</Story>
