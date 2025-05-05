<script>
	import Navbar from '../components/Navbar.svelte';
</script>

<div class="layout">
	<Navbar />
	<div class="content">
		<slot></slot>
	</div>
</div>

<style>
	@import '../default.css';

	.layout {
		display: flex;
		flex-direction: row;
	}

	.content {
		flex: 1;
		padding: 1rem;
	}
</style>
