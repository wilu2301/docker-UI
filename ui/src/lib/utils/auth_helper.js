import { userState } from '$lib/state/user.svelte.js';
import { goto } from '$app/navigation';

export async function canAccess(event,permission) {
	setTimeout(async () => {
		if (!(await userState.hasToken())) {
			const redirectTo = event.url.searchParams;
			await goto(`/login?redirectTo=${redirectTo}&reason="Not logged in"}`);
		}

		if (!(await userState.hasPermission(permission))) {
			await goto(`/login?reason="Insufficient permission. Required: ${permission}"`);
		}
	}, 0);
}