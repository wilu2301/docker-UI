import { Fetcher } from 'openapi-typescript-fetch';

import type { paths } from './schema';

const fetcher = Fetcher.for<paths>();

// global configuration
fetcher.configure({
	baseUrl: 'http://localhost:8000',
});

export const ping = fetcher.path('/ping').method('get').create();
