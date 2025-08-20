<script>
	import Field from '$root/routes/(app)/compose/assistant/components/Field.svelte';
	import Validator from '$root/routes/(app)/compose/assistant/components/Validator.svelte';
	import KeyValue from '$root/routes/(app)/compose/assistant/components/KeyValue.svelte';
	import { Box, PcCase } from '@lucide/svelte';
	import PortsInline from '$root/routes/(app)/compose/assistant/components/PortsInline.svelte';
	import { apiCall } from '$root/routes/(app)/compose/assistant/utils.svelte.js';
	import { API_URL } from '$lib/index.js';
	import { userState } from '$lib/state/user.svelte.js';

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
			children: []
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

	async function validatePorts(children) {
		const previousChildren = service.ports.children;

		// Check for deleted ports
		for (const prevPort of previousChildren) {
			const stillExists = children.some(
				(port) => port.key === prevPort.key && port.value === prevPort.value
			);

			if (!stillExists) {
				// Port was deleted, remove from server
				const publicPort = parseInt(prevPort.value, 10);
				await apiCall(
					`${API_URL}apps/delete_port?token=${userState.token}&host_port=${publicPort}`,
					'deleted',
					null,
					'DELETE'
				);
			}
		}

		const MAX_PORT = 65535;
		for (const [index, port] of children.entries()) {
			// Check which ports changed
			const previousPort = previousChildren[index];
			const hasChanged =
				!previousPort ||
				port.key !== previousPort.key ||
				port.value !== previousPort.value ||
				port.inline.tcp !== previousPort.inline.tcp ||
				port.inline.udp !== previousPort.inline.udp;

			// Only validate if there's a change
			if (hasChanged) {
				// console.log(`Port at index ${index} has changed`);

				const containerPort = parseInt(port.key, 10);
				const publicPort = parseInt(port.value, 10);
				const tcp = port.inline.tcp;
				const udp = port.inline.udp;

				// Basic validation
				if (
					isNaN(containerPort) ||
					containerPort > MAX_PORT ||
					containerPort <= 0 ||
					isNaN(publicPort) ||
					publicPort > MAX_PORT ||
					publicPort <= 0
				) {
					port.inline.notAvailable = true;
					continue;
				}

				if (previousPort) {
					const prevPublicPort = parseInt(previousPort.value, 10);
					await apiCall(
						`${API_URL}apps/delete_port?token=${userState.token}&host_port=${prevPublicPort}`,
						null,
						null,
						'DELETE'
					);
				}

				// Validate on the Server

				const resultClaim = await apiCall(
					`${API_URL}apps/setup/claim_port?token=${userState.token}&host_port=${publicPort}&container_port=${containerPort}&tcp=${tcp}&udp=${udp}`,
					'claimed',
					null,
					'POST'
				);

				// Update port status
				if (resultClaim) {
					port.inline.notAvailable = false;

					service.ports.children[index] = {
						key: port.key,
						value: port.value,
						inline: {
							tcp: port.inline.tcp,
							udp: port.inline.udp,
							notAvailable: false
						}
					};
				} else {
					port.inline.notAvailable = true;
				}
			}
		}
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
			<button>Pull</button>
			<Validator validator={service.image.validator} />
		</div>

		<div class="line">
			<KeyValue
				list={service.ports}
				settings={portsSettings}
				onchange={(children) => validatePorts(children)}
			/>
		</div>
		<h3 style="color: red; font-weight: bolder">Work in progress</h3>
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
	button {
		width: 6rem;
		height: 4rem;

		margin-right: 2rem;

		background: pallet.$primary;
		color: pallet.$white;

		border: none;
		border-radius: 1rem;

		font-size: large;

		transition: 0.2s;
		&:hover {
			background-color: pallet.$secondary;
			color: pallet.$text;
		}
	}
</style>
