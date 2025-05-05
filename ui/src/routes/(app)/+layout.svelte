<script>
	import Navbar from '../../components/Navbar.svelte';
</script>

<div class="layout">
	<Navbar />
	<div class="content">
		<slot></slot>
	</div>
</div>

<style>
	@import '../../default.css';

	.layout {
		display: flex;
	}

	.content {
		margin-left: 20%;
		width: 80%;
	}
</style>
