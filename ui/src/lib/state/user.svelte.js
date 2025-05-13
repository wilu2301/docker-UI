import axios from 'axios';
import { API_URL } from '$lib';

class UserState {
	username = $state('');
	token = $state('');

	constructor(username = '', token = '') {
		this.username = username;
		this.token = token;
	}

	save() {
		localStorage.setItem('username', this.username);
		localStorage.setItem('token', this.token);
	}

	load() {
		this.username = localStorage.getItem('username') || '';
		this.token = localStorage.getItem('token') || '';
	}

	clear() {
		this.username = '';
		this.token = '';
		localStorage.removeItem('username');
		localStorage.removeItem('token');
	}

	async login(username, password) {
		this.clear();

		try {
			const res = await axios.post(
				API_URL + `auth/login?username=${username}&password=${password}`
			);

			if (res.status === 200) {
				this.token = res.data.token;
				this.username = username;

				this.save();
				return true;
			}
		} catch {
			return false;
		}
	}

	async hasPermission(scope) {
		try {
			const res = await axios.get(
				API_URL + `auth/has_permission?scope=${scope}&token=${this.token}`
			);

			if (res.status === 200) {
				return res.data.permission;
			}
		} catch {
			return false;
		}
		return false;
	}

	async hasToken() {
		if (this.token === '') {
			this.load();
		}
		return this.token !== '';
	}
}

export const userState = new UserState();
