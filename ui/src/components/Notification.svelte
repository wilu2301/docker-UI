<script>
	import { Bell, X } from '@lucide/svelte';


	let open = $state(false);
	let messages = $state([]);

	function addMessage(message, ttl = 5000) {
		messages.push({
			id: messages.length + 1,
			message: message,
			expire: Date.now() + ttl,
			type: "info",
		});
	}

	function deleteMessage(id) {
		messages = messages.filter((message) => message.id !== id);
	}

	function timeClean() {
		const now = Date.now();

		messages.forEach((message) => {
			if (message.expire < now) {
				deleteMessage(message.id);
			}
		});
	}
	/*
	setInterval(() => {
		timeClean();
	}, 1000);
*/

	addMessage('No Permission');
	addMessage('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus, congue vel laoreet ac, dictum vitae odio. Fusce at massa nec sapien auctor gravida in in tellus.', 10000);
	function showNotifications() {
		open = true;
	}
</script>

<main class="notification">
	<div class="icon">
		<button onclick={() => (open = !open)}>
			<Bell size={32} />
		</button>
	</div>
	{#if open}
		<div class="menu">
			<div class="header">
				<h2>Notifications</h2>
				<button onclick={() => (open = false)}>
					<X size={32} />
				</button>
			</div>
			<div class="messages">
				{#each messages as message (message.id)}
					<div class="message">
						<p>{message.message}</p>
					</div>
				{/each}
			</div>
		</div>
	{/if}
</main>

<style lang="scss">
	@use '../style/pallet.scss';

	.notification {
		background: red;
		width: 100%;
		height: 100%;

		padding: 1rem;

		.menu {
			height: 100%;
			width: 100%;
			position: absolute;
			right: 0;
			top: 0;

			display: flex;
			flex-direction: column;

			z-index: 2;
			background-color: pallet.$secondary;

			.header {
				width: 100%;
				height: 8rem;

				padding: 1rem;

				background: aliceblue;
				display: flex;
				flex-direction: row;
				justify-content: end;
				align-items: center;

				button {
					margin-right: 2rem;
					background: none;
					border: none;
					cursor: pointer;
				}
			}
			.messages {
				background: green;
				width: 100%;
				height: 100%;

				display: flex;
				flex-direction: column;
				justify-content: start;
				align-items: center;

				.message{
					width: 90%;
					height: auto;

					background: white;
					border-radius: 16px;
					margin: 1rem 0;
					padding: 1rem;

					display: flex;
					justify-content: center;
					align-items: center;

					p {
						color: pallet.$text;
						font-size: 1.2rem;
						text-align: center;
						margin: 0;
					}
				}
			}
		}

		.icon {
			width: 90%;
			height: 4rem;

			display: flex;
			justify-content: right;
			align-items: start;

			button {
				width: 4rem;
				height: 4rem;

				background-color: pallet.$accent;

				border: none;
				border-radius: 16px;

				box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
			}
		}
	}
</style>
