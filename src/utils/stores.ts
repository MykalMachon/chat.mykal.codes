import { writable } from 'svelte/store';

export const thread = writable([]);
export const newMessageStream = writable('');
export const threadLoading = writable(false);

