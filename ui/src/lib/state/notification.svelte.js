export const NotificationType = {
	INFO: 'info',
	WARNING: 'warning',
	ERROR: 'error',
	SUCCESS: 'success'
};

class NotificationState {
	constructor() {
		this.notifications = [];
	}

	messages = $state([]);

	addMessage(message, type = NotificationType.INFO) {
		this.messages.push({
			id: this.messages.length + 1,
			createdAt: new Date(),
			message: message,
			type: type
		});
	}

	deleteMessage(id) {
		this.messages = this.messages.filter((message) => message.id !== id);
	}

	clearAll() {
		this.messages = [];
	}
}

export const notificationState = new NotificationState();
