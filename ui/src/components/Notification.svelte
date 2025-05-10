<script>
	import {
		Bell,
		X,
		CircleX,
		TriangleAlert,
		Info,
		CircleCheck,
		BrushCleaning
	} from '@lucide/svelte';

	import { slide, blur } from 'svelte/transition';

	const MessageType = {
		INFO: 'info',
		WARNING: 'warning',
		ERROR: 'error',
		SUCCESS: 'success'
	};

	let open = $state(false);
	let messages = $state([]);

	function addMessage(message, type = MessageType.INFO) {
		messages.push({
			id: messages.length + 1,
			createdAt: new Date(),
			message: message,
			type: type
		});
	}

	function deleteMessage(id) {
		messages = messages.filter((message) => message.id !== id);
	}

	function clearAll() {
		messages = [];
	}

	addMessage('No Permission', MessageType.WARNING);
	for (let i = 0; i < 10; i++) {
		addMessage(
			'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus, congue vel laoreet ac, dictum vitae odio. Fusce at massa nec sapien auctor gravida in in tellus.'
		);
	}
</script>

<main class="notification">
	<div class="icon">
		<button onclick={() => (open = !open)}>
			<Bell size={32} />
			{#if messages.length > 0}
				<span class="notification-count">{messages.length}</span>
			{/if}
		</button>
	</div>
	{#if open}
		<div class="menu" transition:slide>
			<div class="header">
				<h2>Notifications</h2>
				<button onclick={() => (open = false)}>
					<X size={32} />
				</button>
			</div>
			<div class="messages">
				{#each messages as message (message.id)}
					<div class="message" transition:blur>
						<p id="createdAt">{message.createdAt.toLocaleString()}</p>

						<div class="message-type">
							{#if message.type === MessageType.INFO}
								<Info size={32} color="var(--info)" />
							{:else if message.type === MessageType.WARNING}
								<TriangleAlert size={32} color="var(--warning)" />
							{:else if message.type === MessageType.ERROR}
								<CircleX size={32} color="var(--error)" />
							{:else if message.type === MessageType.SUCCESS}
								<CircleCheck size={32} color="var(--success)" />
							{/if}
						</div>
						<p>{message.message}</p>
						<button class="close" onclick={() => deleteMessage(message.id)}>
							<X size={32} />
						</button>
					</div>
				{/each}
				<div class="clear">
					<button onclick={clearAll}>
						<BrushCleaning />
						Clear All
					</button>
				</div>
			</div>
		</div>
	{/if}
</main>

<style lang="scss">
	@use '../style/pallet.scss';

	.notification {
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

			background: pallet.$primary;
			border-radius: 20px 0 0 20px;
			z-index: 2;

			.header {
				width: 100%;
				height: 8rem;

				padding: 1rem;

				background: pallet.$secondary;
				border-radius: 20px 20px 0 0;
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
				width: 100%;
				height: calc(100% - 10.5rem);

				overflow-y: auto;
				display: flex;
				flex-direction: column;
				justify-content: start;
				align-items: center;

				border-radius: 20px;

				.message {
					width: 80%;
					height: auto;

					background: white;
					border-radius: 16px;
					margin: 1rem 0;
					padding: 1rem;

					display: flex;
					justify-content: center;
					align-items: center;

					#createdAt {
						font-size: 1rem;
					}

					.message-type {
						width: 4rem;
						height: 4rem;
						margin: 0.5rem;

						display: flex;
						justify-content: center;
						align-items: center;
					}

					p {
						color: pallet.$text;
						font-size: 1.2rem;
						text-align: center;
						margin: 0;
					}

					.close {
						width: 2rem;
						height: 2rem;

						display: flex;
						justify-content: center;
						background: none;
						border: none;
					}
				}
			}
			.clear {
				width: 100%;
				height: 4rem;

				display: flex;
				justify-content: center;
				align-items: center;

				button {
					width: 80%;
					height: 4rem;

					position: absolute;
					bottom: 1rem;

					display: flex;
					gap: 0.5rem;
					flex-direction: row;
					justify-content: center;
					align-items: center;

					background-color: pallet.$accent;
					border-radius: 16px;
					border: none;

					font-size: 1.2rem;
					box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);

					transition: 0.5s;
					&:hover {
						background-color: pallet.$rojo;
						box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
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

			.notification-count {
				width: 2rem;
				height: 2rem;

				background-color: pallet.$rojo;
				color: white;
				border-radius: 50%;

				display: flex;
				justify-content: center;
				align-items: center;

				position: absolute;
				top: 0.5rem;
				right: 0.5rem;

				font-size: 1.2rem;
			}

			button {
				background-color: pallet.$primary;
				border-radius: 50%;
				border: none;

				display: flex;
				justify-content: center;
				align-items: center;

				cursor: pointer;

				transition: 0.5s;
			}

			button:hover {
				background-color: pallet.$secondary;
			}

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
