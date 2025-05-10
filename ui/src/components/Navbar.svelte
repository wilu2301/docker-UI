<script>
	import { House, Box, FileSliders, Settings2, LogOut, User } from '@lucide/svelte';
	import { userState } from '$lib/state/user.svelte.js';
	import { goto } from '$app/navigation';

	function logout() {
		userState.clear();
		goto('/login');
	}
</script>

<main class="navbar">
	<div class="logo">
		<a href="/">
			<img src="https://picsum.photos/200" alt="Logo" />
		</a>
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
				<a href="/"><FileSliders /> Compose</a>
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
</main>

<style lang="scss">
	@use '../style/pallet.scss';

	.navbar {
		height: 100vh;
		width: 20%;

		padding-right: 1rem;

		display: flex;
		flex-direction: column;
		justify-content: center;

		position: fixed;

		background-color: pallet.$primary;

		border-radius: 0 20px 20px 0;

		font-size: 1.2rem;

		box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.1);

		.logo {
			height: 20%;

			display: flex;
			justify-content: center;
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
