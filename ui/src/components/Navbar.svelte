<script lang="ts">
	import { House, Box, FileSliders, Settings2, LogOut, User, PanelLeftOpen } from '@lucide/svelte';
	import { userState } from '$lib/state/user.svelte.js';
	import { goto } from '$app/navigation';

	function logout(): void {
		userState.clear();
		goto('/login');
	}

	/*
	<div class="logo-section">
		<a href="/">
			<img class="logo" src="https://picsum.photos/400" alt="Logo" />
		</a>
	</div>
	 */
</script>

<main class="container-big">
	<div class="navbar fullscreen">
		<div class="size">
			<PanelLeftOpen class="icon" />
		</div>

		<div class="items">
			<ul id="upper">
				<li>
					<a href="/"><House /> Dashboard</a>
				</li>
				<li>
					<a href="/container"><Box /> Container</a>
				</li>
				<li>
					<a href="/compose"><FileSliders /> Compose</a>
				</li>
			</ul>
			<ul id="lower">
				<p>
					<User />
					{userState.username}
				</p>
				<hr />
				<li>
					<a href="/"><Settings2 /> Settings</a>
				</li>
				<li>
					<a href="#logout" onclick={logout}><LogOut /> Logout</a>
				</li>
			</ul>
		</div>
	</div>
</main>

<style lang="scss">
	@use '../style/pallet.scss';

	.container-big {
		height: 100vh;
		width: 20rem;
	}
	.container-small {
		height: 100vh;
		width: 5rem;
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

			color: pallet.$white;

			transition: 0.5s;
			&:hover {
				cursor: pointer;
				color: pallet.$accent;
				transform: rotate(180deg);
			}
		}

		.items {
			height: 80%;
			display: flex;
			flex-direction: column;
			justify-content: space-between;

			ul {
				display: flex;
				flex-direction: column;

				li {
					padding: 1rem;
					margin: 1rem 0;

					display: flex;
					align-items: center;

					list-style: none;

					transition: 0.5s;

					a {
						color: pallet.$white;
						text-decoration: none;
					}

					:global(svg) {
						vertical-align: top;
					}

					&:hover {
						padding: 2rem;

						background-color: pallet.$secondary;
						border-radius: 5px;
						box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);

						transition: 0.5s;
					}
				}

				p {
					color: pallet.$white;
					margin: 1rem;
					text-align: center;
				}

				hr {
					border: 1px solid pallet.$white;
					margin: 0 1rem;
				}
			}
		}
	}
</style>
