import { userState } from '$lib/state/user.svelte.js';
import { goto } from '$app/navigation';
export const ssr = false


const REQUIRED_PERMISSION = 2


export const load = async (event) => {

	if (!await userState.hasToken()) {
		const redirectTo = event.url.searchParams
		await goto(`/login?redirectTo=${redirectTo}&reason="Not logged in"}`);
	}

	if (!await userState.hasPermission(REQUIRED_PERMISSION)) {
		await goto(`/login?reason="Insufficient permission. Required: ${REQUIRED_PERMISSION}"`,)
	}
}