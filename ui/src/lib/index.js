// place files you want to import through the `$lib` alias in this folder.

// Check if building
export let API_URL;
export let API_URL_NEW;
if (import.meta.env.PROD) {
	API_URL = '/api/';
	API_URL_NEW = '';
} else {
	API_URL = 'http://localhost:8000/api/';
	API_URL_NEW = 'http://localhost:8000';
}
