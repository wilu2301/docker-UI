export const load = async (event) => {
	const redirectTo = event.url.searchParams.get('redirectTo');
	const reason = event.url.searchParams.get('reason');

	return {
		redirectTo: redirectTo,
		reason: reason
	};
};
