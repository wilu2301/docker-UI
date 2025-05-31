<script lang="ts">
	import Notification from '$root/components/Notification.svelte';
	import Navbar from '$root/components/Navbar.svelte';
</script>

<div class="layout">
	<div class="sidebar">
		<Navbar />
	</div>
	<div class="content">
		<slot></slot>
	</div>
	<div class="notification">
		<Notification />
	</div>
</div>

<style lang="scss">
  @use '$root/style/pallet.scss';
  @import '../../default.css';

	.layout {
		min-height: 100vh;
		display: flex;
      background: pallet.$background;


      .sidebar {
			width: max-content;
			flex-shrink: 0;
		}

		.content {
			flex: 1;
			height: 100%;
		}

		.notification {
			width: 20%;
			height: auto;
			position: fixed;
			top: 0;
			right: 0;
		}
	}
</style>
