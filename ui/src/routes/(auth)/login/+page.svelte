<main>
	<div class="login">
		<h1>Welcome Back!</h1>
		<input type="text" id="username" placeholder="Username" />
		<input type="password" id="password" placeholder="Password" />
		<button type="submit">Login</button>
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
		}
		background-image: url('https://picsum.photos/1920/1080?blur');
	}
</style>
