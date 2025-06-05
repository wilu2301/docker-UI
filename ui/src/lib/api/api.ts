import { Fetcher } from 'openapi-typescript-fetch';
import { API_URL_NEW } from '$lib';
import type { paths } from './schema';

const fetcher = Fetcher.for<paths>();

// Configure base URL on the fetcher
fetcher.configure({
	baseUrl: API_URL_NEW
});

// <section> Container API
export const getApps = fetcher.path('/api/apps/').method('get').create();

export const getApp = fetcher.path('/api/apps/{app_name}').method('get').create();

export const getAppVolumes = fetcher.path('/api/apps/{app_name}/volumes').method('get').create();

export const getServices = fetcher.path('/api/apps/{app_name}/services').method('get').create();

export const getServiceContainers = fetcher
	.path('/api/apps/{app_name}/{service_name}/containers')
	.method('get')
	.create();

// </section>
