// place files you want to import through the `$lib` alias in this folder.

// Check if building
export let API_URL;
if (import.meta.env.PROD) {
	API_URL = '/api';
} else {
	API_URL = 'http://localhost:8000/api/';
}
