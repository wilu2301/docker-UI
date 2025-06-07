class SettingsState {
  public host: string;

  constructor() {
    this.host = "http://localhost";
  }
}

export const settingsState = new SettingsState();
