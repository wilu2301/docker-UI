<script>
	import {fade} from "svelte/transition"
	import App from '$root/routes/(app)/compose/App.svelte';
</script>

<main>
	<div class="overview">
		<h1></h1>
	</div>
	<div class="apps" transition:fade>
	<App appName="test_app"/>
	<App appName="test_app"/>
	<App appName="test_app"/>
	<App appName="test_app"/>
	<App appName="test_app"/>
	<App appName="test_app"/>
	<App appName="test_app"/>
	<App appName="test_app"/>
	<App appName="test_app"/>
	<App appName="test_app"/>
	<App appName="test_app"/>
	</div>
</main>

<style>
	main {
		padding: 2rem;

			.apps{
					display: flex;
					flex-flow: row wrap;
					gap: 1rem;


			}
	}
</style>
