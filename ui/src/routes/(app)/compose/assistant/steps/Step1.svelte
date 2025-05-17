<script>
	import Field from '$root/routes/(app)/compose/assistant/components/Field.svelte';
	import Selection from '$root/routes/(app)/compose/assistant/components/Selection.svelte';
	import Validator from '$root/routes/(app)/compose/assistant/components/Validator.svelte';

	import { fade } from 'svelte/transition';
	import { API_URL } from '$lib';
	import { userState } from '$lib/state/user.svelte.js';
	import { notificationState, NotificationType } from '$lib/state/notification.svelte.js';

	import { apiCall } from '$root/routes/(app)/compose/assistant/utils.svelte.js';

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
			type: 'password',
			name: 'Git Token',
			value: ''
		}
	});

	$effect(async () => {
		if (userState && userState.token) {
			await get_saved_fields();
		}
	});

	async function get_saved_fields() {
		const result = await apiCall(
			`${API_URL}apps/creation?token=${userState.token}`,
			null,
			null,
			'GET'
		);
		if (result === null) return;

		validateName(result.name);
		if (result.git) {
			changeStorage('Git');
		} else {
			changeStorage('Local');
		}
		fGitUrl.field.value = result.git_url;
		fGitBranch.field.value = result.git_branch;
		fGitFolder.field.value = result.git_folder;
		fGitUsername.field.value = result.git_username;
		fGitToken.field.value = result.git_token;

		await validateGitUrl();
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
		if (fGitUrl.field.value === '') return;
		if (!fGitUrl.field.value.startsWith('https://')) return;
		if (!fGitUrl.field.value.endsWith('.git')) return;

		const apiURL = `${API_URL}apps/setup_git?token=${userState.token}
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
				if (result.invalidAt && Array.isArray(result.invalidAt)) {
					fGitUrl.validator.conditions[0].met = result.invalidAt.includes('url');
					fGitUrl.validator.conditions[1].met = result.invalidAt.includes('branch');
					fGitUrl.validator.conditions[2].met = result.invalidAt.includes('auth_clone');
					fGitUrl.validator.conditions[3].met = result.invalidAt.includes('auth_push');
					fGitUrl.validator.conditions[4].met = result.invalidAt.includes('auth_push');
					fGitUrl.validator.conditions[5].met = result.invalidAt.includes('folder');
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
	<div class="content">
		<div class="line">
			<Field field={fName.field} onchange={validateName} />
			<Validator validator={fName.validator} />
		</div>
		{#if fName.validator.conditions.every((condition) => condition.met)}
			<div class="line" in:fade>
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
		{/if}
	</div>
</main>

<style lang="scss">
	@use '$root/style/pallet.scss';
	main {
		width: 100%;
		.content {
			width: auto;
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
	}
</style>
