<script>
	import { ChevronLeft } from '@lucide/svelte';
	import Field from '$root/routes/(app)/compose/assistant/Field.svelte';
	import Selection from '$root/routes/(app)/compose/assistant/Selection.svelte';
	import Validator from '$root/routes/(app)/compose/assistant/Validatior.svelte';

	import { fade } from 'svelte/transition';
	import axios from 'axios';
	import { API_URL } from '$lib';

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
					met: true
				},
				{
					goal: 'Git Branch is valid',
					met: false
				},
				{
					goal: 'Git Folder is valid',
					met: false
				},
				{
					goal: 'User has access to the repository',
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

	function nameAvailable(name) {
		axios.post(API_URL + `apps/name_available?name=${name}`).then((res) => {
			if (res.status === 200) {
				if (res.data.available === true) {
					fName.validator.conditions[1].met = true

				} else {
					fName.validator.conditions[1].met = false
				}
			}
		});
		return false
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

	function validateGitUrl(NewValue) {
		fGitUrl.field.value = NewValue;

		// TODO: validate
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
				<Field field={fGitUrl.field} />
			</div>
			<div class="line" in:fade>
				<Field field={fGitBranch.field} onchange={validateGitUrl} />
			</div>
			<div class="line" in:fade>
				<Field field={fGitFolder.field} onchange={validateGitUrl} />
			</div>
			<div class="line" in:fade>
				<Field field={fGitUsername.field} onchange={validateGitUrl} />
			</div>
			<div class="line" in:fade>
				<Field field={fGitToken.field} onchange={validateGitUrl} />
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
