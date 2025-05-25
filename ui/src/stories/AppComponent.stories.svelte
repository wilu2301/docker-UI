<script module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	import App from '$root/routes/(app)/compose/App.svelte';

	const { Story } = defineMeta({
		title: 'AppComponent',
		component: App
	});
</script>

<Story name="Normal" />
