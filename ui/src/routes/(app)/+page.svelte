<script lang="ts">
	import { notificationState } from '\$root/lib/state/notification.svelte';
	import Section from '$root/routes/(app)/compose/detail/[app]/Section.svelte';
	import { Axe, Calendar, Cog } from '@lucide/svelte';
	import { API_URL_NEW } from '\$root/lib';
	import { fade } from 'svelte/transition';

	let bigScreenshot = $state(false);
	let bigScreenshotUrl = $state('');

	function hideBigScreenshot() {
		bigScreenshot = false;
	}

	function showBigScreenshot(url) {
		bigScreenshotUrl = url;
		bigScreenshot = true;
	}
</script>

<main>
	<div class="dashboard">
		<h1>Welcome to the preview</h1>
		<div class="welcome">
			<p>
				Servus and welcome to my project.
				<br />
				<br />
				In the last couple of hours, (≈ 74h) I build this little Docker UI from scratch.
				<br />
				Using Fastapi, Sqlmodel and the Docker SDK on the backend along with Svelte on the Frontend,
				<br />
				I tried my best to implement as much as possible by myself and with as little AI as possible.
				<br />
				<br />
				It was my first huge project and also my first typescript and svelte experience.
				<br />
				The whole project is structured in a modular manner, so if you wanna take a look at the
				<a href="https://github.com/wilu2301/docker-UI" target="_blank">source code</a>, go for it
				:)
				<br />
				<br />
				Unfortunately are some features not yet completely ready, so consider this as a demo.
				<br />
				<br />
				Thanks for reviewing my project,
				<br />
				~ wilu
			</p>
		</div>

		<Section title="Features" icon={Cog}>
			<ul>
				<li>Advanced Permission System</li>
				<li>
					Notification System <button
						onclick={() => {
							notificationState.addMessage('Notifications Work :)');
						}}>Test</button
					>
				</li>
				<li><a href="/compose">See Running Docker Compose Files / Apps</a></li>
				<li><a href="compose/detail/test_app">Inspect Apps</a></li>
				<li><a href="container/logs/test container">See Docker logs</a></li>
				<li><a href="/api">Swagger UI endpoint</a></li>
			</ul>
		</Section>
		<Section title="Work in Progress" icon={Axe}>
			<ul>
				<li><a href="/compose/assistant">App Creation Wizard</a></li>
				<li><a href="/compose/new">Manual App Creation</a></li>
			</ul>
		</Section>
		<Section title="Planed Features" icon={Calendar}>
			<ul>
				<li>Container view</li>
				<li>Settings and Account page</li>
				<li>Git integration for stack deployments</li>
				<li>Docker Swarm integration</li>
			</ul>
		</Section>
		<h2>Screenshots</h2>
		<div class="screenshots">
			<div
				class="screenshot"
				onclick={() => {
					showBigScreenshot(API_URL_NEW + '/screenshots/apps.png');
				}}
			>
				<img src={API_URL_NEW + '/screenshots/apps.png'} alt="Apps View" />
				<p>Apps View</p>
			</div>
			<div
				class="screenshot"
				onclick={() => {
					showBigScreenshot(API_URL_NEW + '/screenshots/details.png');
				}}
			>
				<img src={API_URL_NEW + '/screenshots/details.png'} alt="Apps View" />
				<p>App details</p>
			</div>
			<div
				class="screenshot"
				onclick={() => {
					showBigScreenshot(API_URL_NEW + '/screenshots/details2.png');
				}}
			>
				<img src={API_URL_NEW + '/screenshots/details2.png'} alt="Apps View" />
				<p>Container View</p>
			</div>
			<div
				class="screenshot"
				onclick={() => {
					showBigScreenshot(API_URL_NEW + '/screenshots/git.png');
				}}
			>
				<img src={API_URL_NEW + '/screenshots/git.png'} alt="Apps View" />
				<p>Git support for changing docker stacks</p>
			</div>
		</div>
	</div>
</main>
{#if bigScreenshot}
	<div class="big-screenshot" transition:fade>
		<img src={bigScreenshotUrl} alt="Apps View" />
		<button id="close" onclick={hideBigScreenshot}>X</button>
	</div>
{/if}

<style lang="scss">
	@use '../../style/pallet';
	.dashboard {
		padding: 2rem;
		background-color: pallet.$background;
		height: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;

		ul {
			gap: 1rem;
			width: 100%;
			height: 100%;
			display: flex;
			flex-direction: column;
			justify-content: center;
			align-items: center;

			font-size: large;
			text-decoration: none;
			list-style: none;
			li {
				a {
					color: pallet.$info;
					text-decoration: none;
				}
			}
		}

		.welcome {
			width: 60%;
			padding: 1rem;
			background-color: pallet.$secondary;
			border-radius: 16px;
			font-size: large;
		}
		button {
			background: pallet.$accent;
			border: none;
			padding: 1rem 2rem;
			border-radius: 16px;
		}
	}
	.screenshots {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		justify-content: center;
		gap: 2rem;

		.screenshot {
			width: 48rem;
			display: flex;
			flex-direction: column;
			align-items: center;
			img {
				width: 100%;
			}
		}
	}

	.big-screenshot {
		z-index: 4;
		position: fixed;
		top: 50vh;
		left: 50vw;
		transform: translate(-50vw, -50vh);
		width: 100%;
		height: 100%;

		display: flex;
		justify-content: center;
		align-items: center;
		background-color: rgba(0, 0, 0, 0.7);
		img {
			max-width: 80%;
		}

		button {
			z-index: 1001;
			position: absolute;
			top: 2rem;
			right: 2rem;
			background: pallet.$accent;
			font-size: xx-large;
			border-radius: 16px;
			border: none;
			padding: 1rem 2rem;

			&:hover {
				background: pallet.$secondary;
				color: white;
			}
		}
	}
</style>
