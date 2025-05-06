class UserState {
	username = $state('');
	token = $state('');

	constructor(username = '', token = '') {
		this.username = username;
		this.token = token;
	}

	setUsername(username) {
		this.username = username;
	}
}

export const userState = new UserState();
