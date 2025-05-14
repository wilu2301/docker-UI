<script>
	import Navbar from '../../components/Navbar.svelte';
	import Notification from '$root/components/Notification.svelte';
</script>

<div class="layout">
	<Navbar />
	<div class="content">
		<slot></slot>
	</div>
	<div class="notification">
		<Notification />
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

	.notification {
		width: 20%;
		height: auto;

		position: fixed;
		top: 0;
		right: 0;
	}
</style>
