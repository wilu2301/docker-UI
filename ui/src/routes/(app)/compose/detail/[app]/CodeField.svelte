<script lang="ts">
	import Monaco from 'svelte-monaco';
	import { File, GitCommitHorizontal, HardDriveDownload } from '@lucide/svelte';

	let git: boolean = $state(true);
</script>

<div class="collum">
	<div class="top">
		<div class="files">
		<div class="item selected">
			<File /><span>test_app.yaml</span>
		</div>
			<div class="item">
				<File /><span>test_app.yaml</span>
			</div>
			<div class="item">
				<File /><span>test_app.yaml</span>
			</div>
			<div class="item">
				<File /><span>test_app.yaml</span>
			</div>
			<div class="item">
				<File /><span>test_app.yaml</span>
			</div>
			<div class="item">
				<File /><span>test_app.yaml</span>
			</div>
			<div class="item">
				<File /><span>test_app.yaml</span>
			</div>
			<div class="item">
				<File /><span>test_app.yaml</span>
			</div>
			<div class="item">
				<File /><span>test_app.yaml</span>
			</div>
			<div class="item">
				<File /><span>test_app.yaml</span>
			</div>
			<div class="item">
				<File /><span>test_app.yaml</span>
			</div>
			<div class="item">
				<File /><span>test_app.yaml</span>
			</div>
			<div class="item">
				<File /><span>test_app.yaml</span>
			</div>
		</div>

		<div class="item">
			<HardDriveDownload />
			<button>Reload</button>
		</div>
		{#if git}
			<div class="item">
				<GitCommitHorizontal /> <span>Example commit</span>
			</div>
		{/if}
	</div>

	<div class="editor-container">
		<Monaco theme="cobalt" value="" options={{ language: 'yaml', automaticLayout: true }} />
	</div>
	<div class="bottom">
		{#if git}
			<div class="git">
				<input type="text" placeholder="Commit message" />
				<button>Commit</button>
			</div>
		{:else}
			<button>Save</button>
		{/if}
	</div>
</div>

<style lang="scss">
	@use '$root/style/pallet';
	.collum {
		width: 100%;
		display: flex;
		flex-direction: column;
		gap: 1rem;

		.top {
			width: 100%;
			display: flex;
			flex-direction: row;
			align-items: center;
			justify-content: space-between;

			.files{
				width: 70%;
				max-width: 1100px;


				display: flex;
				flex-direction: row;
				gap: 1rem;
				overflow-x: scroll;
			}
			::-webkit-scrollbar {
				height: 4px;
				border-radius: 16px;

				background-color: pallet.$secondary;
			}

			::-webkit-scrollbar-thumb {
				border-radius: 16px;

				background-color: pallet.$accent;
			}

			.item {
				padding: 16px;
				margin-bottom: 8px;

				display: flex;
				flex-direction: row;
				align-items: center;

				transition: background 0.5s, border-radius 0.5s;
				&:hover {
					background: pallet.$white;
					color: pallet.$text;
					border-radius: 16px;
				}

				button{
					padding: 0.5rem 1rem;
					background: none;
					border: none;

					color: pallet.$white;

					&:hover{
						color: pallet.$text;
					}

				}
		}
			.selected {
				background: pallet.$accent;
				border-radius: 16px;
			}
			}

		.bottom {
			width: 100%;

			display: flex;
			flex-direction: row;
			justify-content: right;

			.git {
				width: 100%;
				display: flex;
				flex-direction: row;

				border: solid 1px pallet.$secondary;
				border-radius: 16px;

				input {
					width: 100%;

					background: none;
					color: pallet.$white;

					text-align: center;

					border: none;
					outline: none;
				}

				button {
					padding: 1rem;
					background: pallet.$secondary;
					border: none;
					border-radius: 0 16px 16px 0;

					transition: background 0.5s;

					&:hover {
						background: pallet.$white;
					}
				}
			}

			button {
				padding: 1rem;
				background: pallet.$secondary;
				border: none;
				border-radius: 16px;

				transition: background 0.5s;

				&:hover {
					background: pallet.$white;
				}
			}
		}

		.editor-container {
			height: 300px;
			width: 100%;

			border-radius: 2px;
			border: 2px solid rgba(255, 255, 255, 0.1);
		}
	}
</style>
