import { canAccess } from '$lib/utils/auth_helper.js';
import '$lib/utils/auth_helper.js';
import type { PageLoad } from './$types';

export const ssr = false;

const REQUIRED_PERMISSION = 2;

export const load: PageLoad = async (event) => {
	await canAccess(event, REQUIRED_PERMISSION);
	return {
		name: event.params.app
	};
};
