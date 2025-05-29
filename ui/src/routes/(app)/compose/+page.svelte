<script>
	import App from '$root/routes/(app)/compose/App.svelte';
</script>

<main>
	<a href="/compose/assistant"> Assistant </a>

	<App appName="test_app"/>
	<App appName="test_app"/>
	<App appName="test_app"/>
</main>

<style>
	main {
		padding: 2rem;
	}
</style>
