import { userState } from '$lib/state/user.svelte.js';
import { goto } from '$app/navigation';

export async function canAccess(event,permission) {
	setTimeout(async () => {
		if (!(await userState.hasToken())) {
			const redirectTo = event.url.pathname;
			console.log(event);
			await goto(`/login?redirectTo=${redirectTo}&reason="Not logged in"`);
			return;
		}

		if (!(await userState.hasPermission(permission))) {

			if (event.url.pathname === '/') {
				await goto(`/login?reason=Every Permission denied`);
				return;
			}
			await goto(`/?permission_error=true`);
		}
	}, 0);
}