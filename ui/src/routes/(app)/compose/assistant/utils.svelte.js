import axios from 'axios';
import { notificationState, NotificationType } from '$lib/state/notification.svelte.js';

export async function apiCall(url, responseField, currentResult, method = 'POST') {
	let result = currentResult;
	try {
		let response;
		if (method === 'POST') {
			response = await axios.post(url);
		} else {
			response = await axios.get(url);
		}

		if (response.status === 200) {
			if (responseField == null) {
				result = response.data;
			} else {
				result = response.data[responseField];
			}
		}
	} catch (error) {
		if (error.status === 403) {
			notificationState.addMessage('Permission denied', NotificationType.WARNING);
		} else {
			notificationState.addMessage('Connection issues with the server', NotificationType.ERROR);
			throw Error;
		}
	}
	return result;
}
