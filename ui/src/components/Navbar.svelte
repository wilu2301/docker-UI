<script>
	import { House, Box, FileSliders, Settings2, LogOut } from '@lucide/svelte';
</script>

<main></main>
<div class="navbar">
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
				<a href="/"><Box /> Container</a>
			</li>
			<li>
				<a href="/"><FileSliders /> Compose</a>
			</li>
		</ul>
		<ul id="lower">
			<li>
				<a href="/"><Settings2 /> Settings</a>
			</li>
			<li>
				<a href="/"><LogOut /> Logout</a>
			</li>
		</ul>
	</div>
</div>

<style lang="scss">
	@use '../style/pallet.scss';

	.navbar {
		height: 100vh;
		width: 20%;

		padding-right: 1rem;

		display: flex;
		flex-direction: column;
		justify-content: center;

		background-color: pallet.$primary;
		color: pallet.$white;

		border-radius: 0 20px 20px 0;

		font-size: 1.2rem;


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

					&:hover {
						background-color: pallet.$secondary;
						border-radius: 5px;
						padding: 2rem;
						transition: 0.5s;
					}
				}
			}
		}
	}
</style>
