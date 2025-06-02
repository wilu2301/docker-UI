class SettingsState {

	public host: $state<string>

	constructor() {
		this.host = "http://localhost"
	}

}

export const settingsState = new SettingsState();