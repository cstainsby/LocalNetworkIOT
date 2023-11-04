import type { Actions } from './$types';

export const actions = {

	get: async (event) => {
		
	},
    post: async (event) => {
        console.log(event.params);
        
    }
} satisfies Actions;