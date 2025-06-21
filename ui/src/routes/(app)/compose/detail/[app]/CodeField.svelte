<script lang="ts">
	import Monaco from 'svelte-monaco';
	import { File, GitCommitHorizontal, HardDriveDownload } from '@lucide/svelte';
	import { getAppConfig } from '$lib/api/api';
	import { onMount } from 'svelte';
	import { notificationState, NotificationType } from '$root/lib/state/notification.svelte';
	import { userState } from '$lib/state/user.svelte';
	import type { components } from '$lib/api/schema';

	type ConfigFileApi = components['schemas']['ConfigFile'];
	type ConfigFile = ConfigFileApi & { active?: boolean };

	let configFiles: ConfigFile[] = $state();

	let git: boolean = $state(true);
	let fieldLang: string = $state('.yaml');
	let fieldContent: string = $state();

	let indexFileActive: number = $state(0);

	let { appName } = $props();

	async function fetchData() {
		try {
			// Get general App data
			const appConfig = await getAppConfig({
				app_name: appName,
				token: userState.token
			});

			git = appConfig.data.git;
			configFiles = appConfig.data.config_files;

			loadFile(indexFileActive);
		} catch (error) {
			console.error('Error fetching app config:', error);
			if (error.status === 404) {
				// App config does not exist
				notificationState.addMessage(
					`Config of "${appName}" does not exist`,
					NotificationType.WARNING
				);
			}
		}
	}

	function loadFile(index: number) {
		if (index >= configFiles.length) return;

		let file = configFiles[index];

		// Remove active from last file
		configFiles[indexFileActive].active = false;

		indexFileActive = index;

		file.active = true;
		fieldLang = file.language;
		fieldContent = file.content;
	}

	onMount(async () => {
		if (!userState.token) {
			await new Promise((r) => setTimeout(r, 100));
		}
		await fetchData();
	});
</script>

{#snippet file(name = 'File', selected = false, index = 0)}
	<button class={selected ? 'item selected' : 'item'} onclick={() => loadFile(index)}>
		<File /><span>{name}</span>
	</button>
{/snippet}

<div class="collum">
	<div class="top">
		<div class="files">
			{#each configFiles as f, i}
				{@render file(f.name, f.active, i)}
			{/each}
		</div>

		<button onclick={fetchData} class="item">
			<HardDriveDownload />
			Reload
		</button>

		{#if git}
			<div class="item">
				<GitCommitHorizontal /> <span>Example commit</span>
			</div>
		{/if}
	</div>

	<div class="editor-container">
		<Monaco
			theme="cobalt"
			bind:value={fieldContent}
			options={{ language: fieldLang, automaticLayout: true }}
		/>
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

			.files {
				width: 70%;
				max-width: 1100px;

				display: flex;
				flex-direction: row;
				gap: 1rem;
				overflow-x: auto;
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

				border: none;
				background: none;
				color: white;

				transition:
					background 0.5s,
					border-radius 0.5s;
				&:hover {
					background: pallet.$white;
					color: pallet.$text;
					border-radius: 16px;
				}

				button {
					padding: 0.5rem 1rem;
					background: none;
					border: none;

					color: pallet.$white;

					&:hover {
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
