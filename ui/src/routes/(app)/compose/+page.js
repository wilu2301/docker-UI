import { canAccess } from "$lib/utils/auth_helper.js";
import "$lib/utils/auth_helper.js";

export const ssr = false;

const REQUIRED_PERMISSION = 32;

export const load = async (event) => {
  await canAccess(event, REQUIRED_PERMISSION);
};
