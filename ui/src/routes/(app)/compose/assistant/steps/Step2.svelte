<script>
	import Field from '$root/routes/(app)/compose/assistant/components/Field.svelte';
	import Validator from '$root/routes/(app)/compose/assistant/components/Validator.svelte';
	import KeyValue from '$root/routes/(app)/compose/assistant/components/KeyValue.svelte';
	import { Box, PcCase } from '@lucide/svelte';
	import PortsInline from '$root/routes/(app)/compose/assistant/components/PortsInline.svelte';

	let service = $derived({
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
					key: '80',
					value: '8080',
					inline: {
						tcp: true,
						udp: false
					}
				}
			]
		}
	});

	const portsSettings = {
		key: {
			icon: Box,
			placeholder: 'Container port',
			type: 'number'
		},
		value: {
			icon: PcCase,
			placeholder: 'Public port',
			type: 'number'
		},
		inlineComponent: PortsInline
	};

	function validatePorts(children) {
		const MAX_PORT = 65535;
		children.forEach((port) => {
			const containerPort = parseInt(port.key, 10);
			const publicPort = parseInt(port.value, 10);

			if (isNaN(containerPort) || containerPort > MAX_PORT || containerPort <= 0) {
				port.inline.notAvailable = true;
			} else if (isNaN(publicPort) || publicPort > MAX_PORT || publicPort <= 0) {
				port.inline.notAvailable = true;
			} else {
				port.inline.notAvailable = false;
			}
		});
	}
</script>

<main>
	<div class="Add">
		<button> + </button>
	</div>
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
			<KeyValue
				list={service.ports}
				settings={portsSettings}
				onchange={(children) => validatePorts(children)}
			/>
		</div>
	</div>
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
