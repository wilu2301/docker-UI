<script lang="ts">
	import { House, Box, FileSliders, Settings2, LogOut, User, PanelLeftOpen } from '@lucide/svelte';
	import { userState } from '$lib/state/user.svelte.js';
	import { goto } from '$app/navigation';
	import { slide, fade } from 'svelte/transition';

	function logout(): void {
		userState.clear();
		goto('/login');
	}

	let isOpen: boolean = $state(false);
</script>

<main
	class:container-big={isOpen}
	class:container-small={!isOpen}
	transition:fade={{ duration: 300 }}
>
	<div class="navbar">
		<div class="size">
			<button onclick={() => (isOpen = !isOpen)}>
				<PanelLeftOpen class="icon" style={isOpen ? 'transform: rotate(180deg)' : ''} />
			</button>
		</div>
		<div class="items">
			<ul id="upper">
				<li>
					<a href="/">
						<House size={32} />
						{#if isOpen}
							<span transition:slide={{ duration: 300, axis: 'x' }}>Dashboard</span>
						{/if}
					</a>
				</li>
				<li>
					<a href="/container">
						<Box size={32} />
						{#if isOpen}
							<span transition:slide={{ duration: 300, axis: 'x' }}>Containers</span>
						{/if}
					</a>
				</li>
				<li>
					<a href="/compose">
						<FileSliders size={32} />
						{#if isOpen}
							<span transition:slide={{ duration: 300, axis: 'x' }}>Compose</span>
						{/if}
					</a>
				</li>
			</ul>
			<ul id="lower">
				<li>
					<User size={32} />
					{#if isOpen}
						<span transition:slide={{ duration: 300, axis: 'x' }}>{userState.username}</span>
					{/if}
				</li>
				<li>
					<a href="/">
						<Settings2 size={32} />
						{#if isOpen}
							<span transition:slide={{ duration: 300, axis: 'x' }}>Settings</span>
						{/if}
					</a>
				</li>
				<li>
					<a href="#logout" onclick={logout}>
						<LogOut size={32} />
						{#if isOpen}
							<span transition:slide={{ duration: 300, axis: 'x' }}>Logout</span>
						{/if}
					</a>
				</li>
			</ul>
		</div>
	</div>
</main>

<style lang="scss">
	@use '../style/pallet.scss';

	.container-big,
	.container-small {
		transition:
			width 0.3s ease-out,
			opacity 0.3s ease-out;
		height: 100vh;
	}

	.container-big {
		width: 20rem;
		opacity: 1;
	}

	.container-small {
		width: 6rem;
		opacity: 0.95;
	}

	.navbar {
		height: 100vh;
		width: inherit;
		display: flex;
		flex-direction: column;
		justify-content: center;
		position: fixed;
		background-color: pallet.$primary;
		overflow: hidden;
		border-radius: 0 20px 20px 0;
		font-size: 1.2rem;
		box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.1);

		.size {
			position: absolute;
			bottom: calc(100% - 3rem);
			left: calc(100% - 3rem);
			display: flex;

			button {
				background-color: transparent;
				border: none;
				color: pallet.$white;
				transition: 0.5s;
				&:hover {
					cursor: pointer;
					color: pallet.$accent;
				}
			}
		}

		.items {
			width: auto;
			height: 80%;
			display: flex;
			flex-direction: column;
			justify-content: space-between;

			ul {
				width: auto;
				display: flex;
				justify-content: start;
				flex-direction: column;
				gap: 2rem;

				li {
					width: auto;
					display: flex;
					align-items: center;
					list-style: none;
					color: pallet.$white;
					transition: 0.5s;

					a {
						display: flex;
						align-items: center;
						gap: 0.75rem;
						color: pallet.$white;
						text-decoration: none;
						transition: 0.5s;

						&:hover {
							transform: scale(1.05);
							border-radius: 5px;
							color: pallet.$accent;
						}
					}

					:global(svg) {
						vertical-align: bottom;
					}
				}
			}
		}
	}
</style>
