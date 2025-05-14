<script>
	import Field from '$root/routes/(app)/compose/assistant/components/Field.svelte';
	import Validator from '$root/routes/(app)/compose/assistant/components/Validator.svelte';
	import KeyValue from '$root/routes/(app)/compose/assistant/components/KeyValue.svelte';
	import { Box, PcCase } from '@lucide/svelte';

	let services = $derived([
		{
			containerName: {
				field: {
					name: 'Container name',
					value: ''
				},
				validator: {
					name: 'Container name',
					conditions: [
						{
							goal: 'Test',
							met: false
						}
					]
				}
			},
			image: {
				field: {
					name: 'Image',
					value: ''
				},
				validator: {
					name: 'Image',
					conditions: [
						{
							goal: 'Image is valid',
							met: false
						}
					]
				}
			},
			ports: {
				name: 'Ports',
				children: [
					{
						key: '',
						value: ''
					}
				]
			}
		}
	]);

	const portsSettings = {
		key: {
			icon: Box,
			placeholder: 'Container port'
		},
		value: {
			icon: PcCase,
			placeholder: 'Public port'
		}
	};
</script>

<main>
	<div class="Add">
		<button> + </button>
	</div>
	{#each services as service (service)}
		<div class="service">
			<div class="line">
				<Field field={service.containerName.field}></Field>
				<Validator validator={service.containerName.validator} />
			</div>
			<div class="line">
				<Field field={service.image.field}></Field>
				<Validator validator={service.image.validator} />
			</div>

			<div class="line">
				<KeyValue list={service.ports} settings={portsSettings} />
			</div>
		</div>
	{/each}
</main>

<style lang="scss">
	@use '$root/style/pallet.scss';
	main {
		width: 100%;
		.service {
			width: auto;
			margin: 1rem;
			padding-bottom: 1rem;
			padding-top: 1rem;

			display: flex;
			justify-content: center;
			align-items: center;
			flex-direction: column;
			gap: 2rem;

			border: black dashed 1px;

			hr {
				width: 20%;
				border-color: pallet.$primary;
				margin-left: 1rem;
				margin-right: auto;
			}

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
