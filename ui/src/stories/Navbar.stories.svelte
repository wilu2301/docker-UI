<script module>
	import { defineMeta } from '@storybook/addon-svelte-csf';

	import Navbar from '$root/components/Navbar.svelte';

	const { Story } = defineMeta({
		title: 'Navigation',
		component: Navbar
	});
</script>

<Story name="Navigation" />
