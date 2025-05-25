<script module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	import Page from '$root/routes/(app)/compose/+page.svelte';

	const { Story } = defineMeta({
		title: 'AppsPage',
		component: Page
	});
</script>

<Story name="AppPage" />
