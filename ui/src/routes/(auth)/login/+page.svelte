<script>
	import { userState } from '$lib/state/user.svelte.js';
	import { goto } from '$app/navigation';

	const credentials = $state({
		username: '',
		password: ''
	});

	let error = $state(false);

	async function handleLogin() {
		error = false;

		const result = await userState.login(credentials.username, credentials.password);
		if (result) {
			await goto('/');
		} else {
			error = true;
		}
	}
</script>

<main>
	<div class="login">
		<h1>Welcome Back!</h1>
		<input type="text" id="username" placeholder="Username" bind:value={credentials.username} />
		<input type="password" id="password" placeholder="Password" bind:value={credentials.password} />
		<button type="submit" onclick= {handleLogin}> Login</button>
		{#if error}
			<p class="error">Wrong Username || passoword</p>
		{/if}
	</div>
</main>

<style lang="scss">
	@use '../../../style/pallet.scss';
	main {
		height: 100vh;

		display: flex;
		justify-content: center;
		align-items: center;

		.login {
			padding: 4rem;
			width: 50%;

			display: flex;
			flex-direction: column;
			justify-content: center;
			align-items: center;

			background: pallet.$secondary;
			border-radius: 20px;
			text-align: center;

			box-shadow: 0 32px 15px -6px rgba(0, 0, 0, 0.5);

			input {
				width: 80%;

				margin: 1rem 0;
				padding: 1rem;

				border-radius: 10px;
				border: 1px solid pallet.$primary;

				font-size: 1.2rem;
			}
			button {
				width: 80%;

				padding: 1rem;

				border-radius: 5px;
				border: none;

				background: pallet.$primary;
				color: pallet.$white;

				cursor: pointer;

				transition: 0.3s;

				&:hover {
					background: pallet.$accent;
				}
			}
			.error {
				color: pallet.$error;
				font-size: 1.2rem;
				font-size: 1.2rem;
				margin-top: 1rem;
			}
		}
		background-image: url('https://picsum.photos/1920/1080?blur');
	}
</style>
