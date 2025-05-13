<script>
	import { ChevronLeft } from '@lucide/svelte';
	import Field from '$root/routes/(app)/compose/assistant/Field.svelte';
	import Selection from '$root/routes/(app)/compose/assistant/Selection.svelte';
	import Validator from '$root/routes/(app)/compose/assistant/Validatior.svelte';

	import { fade } from 'svelte/transition';
	import axios from 'axios';
	import { API_URL } from '$lib';
	import { userState } from '$lib/state/user.svelte.js';
	import { notificationState, NotificationType } from '$lib/state/notification.svelte.js';

	let fName = $state({
		field: {
			name: 'Name',
			value: ''
		},
		validator: {
			name: 'Name',
			conditions: [
				{
					goal: 'Name is not empty',
					met: false
				},
				{
					goal: 'Name is unique',
					met: false
				},
				{
					goal: 'Name is not too long',
					met: false
				}
			]
		}
	});

	let fStorage = $state({
		selection: {
			name: 'Storage',
			options: ['Local', 'Git'],
			value: 'Local'
		}
	});

	let fGitUrl = $state({
		field: {
			name: 'Git URL',
			value: ''
		},
		validator: {
			name: 'Git URL',
			conditions: [
				{
					goal: 'Git URL is valid',
					met: false
				},
				{
					goal: 'Git Branch is valid',
					met: false
				},
				{
					goal: 'Can clone repository',
					met: false
				},
				{
					goal: 'Git credentials are valid',
					met: false
				},
				{
					goal: 'User has write permissions ',
					met: false
				},
				{
					goal: 'Git folder can be created',
					met: false
				},
				{
					goal: 'Folder is empty',
					met: false
				}
			]
		}
	});
	let fGitFolder = $state({
		field: {
			name: 'Git Folder',
			value: ''
		}
	});
	let fGitBranch = $state({
		field: {
			name: 'Git Branch',
			value: ''
		}
	});
	let fGitUsername = $state({
		field: {
			name: 'Git Username',
			value: ''
		}
	});
	let fGitToken = $state({
		field: {
			name: 'Git Token',
			value: ''
		}
	});

	async function apiCall(url, responseField, currentResult) {
		let result = currentResult;
		try {
			const response = await axios.post(url);

			console.log(response.data);
			if (response.status === 200) {
				if (responseField == null) {
					result = response.data;
				} else {
					result = response.data[responseField];
				}
			}
		} catch (error) {
			if (error.status === 403) {
				notificationState.addMessage('Permission denied', NotificationType.WARNING);
			} else {
				notificationState.addMessage('Connection issues with the server', NotificationType.ERROR);
				throw Error;
			}
		}
		return result;
	}

	async function nameAvailable(name) {
		const url = `${API_URL}apps/name_available?name=${name}&token=${userState.token}`;

		fName.validator.conditions[1].met = await apiCall(
			url,
			'available',
			fName.validator.conditions[1].met
		);
	}

	function changeGitUrl(NewValue) {
		fGitUrl.field.value = NewValue;
		validateGitUrl();
	}
	function changeGitBranch(NewValue) {
		fGitBranch.field.value = NewValue;
		validateGitUrl();
	}
	function changeGitFolder(NewValue) {
		fGitFolder.field.value = NewValue;
		validateGitUrl();
	}
	function changeGitUsername(NewValue) {
		fGitUsername.field.value = NewValue;
		validateGitUrl();
	}
	function changeGitToken(NewValue) {
		fGitToken.field.value = NewValue;
		validateGitUrl();
	}

	function validateName(NewValue) {
		fName.field.value = NewValue;

		fName.validator.conditions[0].met = fName.field.value.length > 0;
		nameAvailable(NewValue);
		fName.validator.conditions[2].met = fName.field.value.length < 20;
	}
	function changeStorage(NewValue) {
		fStorage.selection.value = NewValue;
	}

	async function validateGitUrl() {
		// Validate Git Url
		if (fGitUrl.field.value === '') return;
		if (!fGitUrl.field.value.startsWith('https://')) return;
		if (!fGitUrl.field.value.endsWith('.git')) return;

		console.log(fGitUsername.field.value)

		const apiURL = `${API_URL}apps/test_connection?token=${userState.token}
		&name=${fName.field.value}
		&git_url=${fGitUrl.field.value}
		&git_folder=${fGitFolder.field.value}
		&git_branch=${fGitBranch.field.value}
		&git_username=${fGitUsername.field.value}
		&git_token=${fGitToken.field.value}`;

		try {
			const result = await apiCall(apiURL, null);

			// Reset all permissions
			fGitUrl.validator.conditions.forEach((condition) => (condition.met = false));

			if (!result.status) {
				console.log(result.valid)
				if (result.valid && Array.isArray(result.valid)) {
					console.log("still valid")
					fGitUrl.validator.conditions[0].met = result.valid.includes('url');
					fGitUrl.validator.conditions[1].met = result.valid.includes('branch');
					fGitUrl.validator.conditions[2].met = result.valid.includes('auth_clone');
					fGitUrl.validator.conditions[3].met = result.valid.includes('auth_push');
					fGitUrl.validator.conditions[4].met = result.valid.includes('auth_push');
					fGitUrl.validator.conditions[5].met = result.valid.includes('folder');
				}
			} else {
				// Success case
				fGitUrl.validator.conditions.forEach((condition) => (condition.met = true));
			}
		} catch (error) {
			console.error('Error validating Git URL:', error);
			notificationState.addMessage('Connection failed', NotificationType.ERROR);
		}
	}
</script>

<main>
	<div class="top-bar">
		<ChevronLeft size={48} />
		<h1>Assistant:</h1>
		<div class="stage">
			<h1 class="number">Step 1 / 5</h1>
			<h1>Create</h1>
		</div>
	</div>
	<div class="content">
		<div class="line">
			<Field field={fName.field} onchange={validateName} />
			<Validator validator={fName.validator} />
		</div>
		<div class="line">
			<Selection selection={fStorage.selection} onchange={changeStorage} />
		</div>
		{#if fStorage.selection.value === 'Git'}
			<div class="line" in:fade>
				<Field field={fGitUrl.field} onchange={changeGitUrl} />
			</div>
			<div class="line" in:fade>
				<Field field={fGitBranch.field} onchange={changeGitBranch} />
			</div>
			<div class="line" in:fade>
				<Field field={fGitFolder.field} onchange={changeGitFolder} />
			</div>
			<div class="line" in:fade>
				<Field field={fGitUsername.field} onchange={changeGitUsername} />
			</div>
			<div class="line" in:fade>
				<Field field={fGitToken.field} onchange={changeGitToken} />
			</div>
			<div class="line" in:fade>
				<div class="center">
					<Validator validator={fGitUrl.validator} />
				</div>
			</div>
		{:else}
			<p in:fade>Config will be stored locally.</p>
		{/if}
	</div>
	<div class="controls">
		<div class="buttons">
			<button>Next</button>
		</div>
	</div>
</main>

<style lang="scss">
	@use '$root/style/pallet.scss';
	main {
		padding: 2rem;

		.top-bar {
			width: 100%;
			height: 5rem;

			display: flex;
			flex-direction: row;
			justify-content: left;
			gap: 1rem;
			align-items: center;

			background: pallet.$secondary;
			border-radius: 1rem;

			.stage {
				display: flex;
				gap: 1rem;

				.number {
					background-color: pallet.$accent;
					padding: 0 1rem;
					border-radius: 8rem;
				}
			}
		}
		.content {
			width: 100%;
			margin: 1rem;

			display: flex;
			justify-content: center;
			align-items: center;
			flex-direction: column;
			gap: 2rem;

			.line {
				width: 90%;
				display: flex;
				justify-content: flex-start;
				align-items: center;
				flex-direction: row;

				.center {
					width: 100%;
					display: flex;
					justify-content: center;
					align-items: center;
				}
			}
		}
		.controls {
			position: absolute;
			bottom: 1rem;
			right: 1rem;

			.buttons {
				button {
					width: 10rem;
					height: 3rem;
					background: pallet.$primary;
					color: pallet.$white;
					border-radius: 4px;
					border: none;
					cursor: pointer;
				}
			}
		}
	}
</style>
