import { Fetcher } from 'openapi-typescript-fetch';
import type { paths } from './schema';

const fetcher = Fetcher.for<paths>();

// Configure base URL on the fetcher
fetcher.configure({
	baseUrl: 'http://localhost:8000'
});

export const ping = fetcher.path('/ping').method('get').create();

// <section> Container API
export const getApps = fetcher.path('/apps/').method('get').create();

export const getApp = fetcher.path('/apps/{app_name}').method('get').create();
// </section>
