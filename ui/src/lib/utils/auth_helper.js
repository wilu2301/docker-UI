import { userState } from "$lib/state/user.svelte.js";
import { goto } from "$app/navigation";
import {
  notificationState,
  NotificationType,
} from "$lib/state/notification.svelte.js";

export async function canAccess(event, permission) {
  setTimeout(async () => {
    if (!(await userState.hasToken())) {
      const redirectTo = event.url.pathname;
      await goto(`/login?redirectTo=${redirectTo}&reason="Not logged in"`);
      return;
    }
    if (!userState.isTokenValid()) {
      const redirectTo = event.url.pathname;
      await goto(`/login?redirectTo=${redirectTo}&reason="Session expired"`);
      return;
    }

    if (!(await userState.hasPermission(permission))) {
      if (event.url.pathname === "/") {
        await goto(`/login?reason=Every Permission denied`);
        return;
      }
      await notificationState.addMessage(
        "Permission denied",
        NotificationType.WARNING,
      );
      await goto(`/`);
    }
  }, 0);
}
