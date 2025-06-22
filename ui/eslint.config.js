import prettier from 'eslint-config-prettier';
import js from '@eslint/js';
import { includeIgnoreFile } from '@eslint/compat';
import svelte from 'eslint-plugin-svelte';
import globals from 'globals';
import { fileURLToPath } from 'node:url';
import svelteConfig from './svelte.config.js';
import tseslint from 'typescript-eslint';

const gitignorePath = fileURLToPath(new URL('./.gitignore', import.meta.url));

export default [
	includeIgnoreFile(gitignorePath),
	js.configs.recommended,
	...tseslint.configs.recommended,
	...svelte.configs.recommended,
	prettier,
	...svelte.configs.prettier,
	{
		languageOptions: {
			globals: { ...globals.browser, ...globals.node }
		}
	},
	{
		files: ['**/*.svelte', '**/*.svelte.js'],
		languageOptions: { parserOptions: { svelteConfig } }
	},
	{
		files: ['**/*.ts', '**/*.tsx'],
		...tseslint.configs.recommendedTypeChecked,
		languageOptions: {
			parserOptions: {
				project: './tsconfig.json',
				tsconfigRootDir: '.'
			}
		}
	},
	{
		files: ['**/*.svelte'],
		...tseslint.configs.recommendedTypeChecked,
		languageOptions: {
			parserOptions: {
				project: './tsconfig.json',
				tsconfigRootDir: '.',
				extraFileExtensions: ['.svelte']
			}
		}
	}
];
