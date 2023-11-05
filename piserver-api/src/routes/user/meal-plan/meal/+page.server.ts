import type { Actions } from './$types';

import type { Recipe, FoodItem } from '$lib/foodBasedTypes';


/**
 * Recipe form post endpoint 
 * Form data shape:
 *  recipeName
 *  recipeDescription 
 *  recipeInstruction_<(<0..n>)1..n>
 *  recipeIngredient_<0..n>
 */
interface RecipeFormData {
    recipeName: string,
    recipeDescription: string,

}


function extractRecipeFormElements(nestedFormElementDict: Object, formData: FormData)  {
    // const extractedElements = {}

    // groupedElementNames.forEach(elementName => {
    //     const recipeInstructions: string[] = []
    //     let i = 0;
    //     while(formData.get("recipeInstruction".concat(i.toString()))) {
    //         const recipeInstruction: string | undefined = formData.get("recipeInstruction".concat(i.toString()))?.toString()
    //         if (recipeInstruction !== undefined) recipeInstructions.push(recipeInstruction)
    //         i++;
    //     }
    // });

    const formEntries = Array.from(formData.entries())
    console.log(formEntries);
    

    // return extractListedElementsRecurr(nestedFormElementDict, formEntries)
}

/**
 * Because form data comes in the shape of a flattened list of Objects containing kv pairs, we must find a way to unflatten it to make it fit our type specifications.
 * To do this we will be recurrsively steping through a template object created by us designating how to read in and construct the type with the data availible
 * This recurrsion becomes necessary in the context of the following example. Here we can have instruction, sub-instructions for those instructions, 
 *  sub-sub-instructions for those sub-instructions, etc...
 * 
 *      e.g. recipeInstruction_01
 * 
 * The suffix will denote as follows:
 *  _   => unique character to define listed element and need for recurrsion
 *  int => each following int from left to right will denote ordering within the current depth
 *          
 *          e.g. _01 will mean that from the second main instruction(1) this example recipeInstruction is the first sub-instruction
 * 
 * @param nestedFormElementDict 
 * @param formEntries 
 * @returns 
 */
function extractListedElementsRecurr(nestedFormElementDict: Object, formEntries: string[][]): Object | null {
    const currentIterableElements = Object.entries(nestedFormElementDict)

    // base case -> child element in nested dictionary doesn't have any keys
    if (currentIterableElements.length === 0) {
        return null
    } 

    const formEntryChildren: string[][] = []

    formEntries.forEach(entry  => {
        if (entry.length !== 2) {
            return null
        }

        const key = entry[0]
        const [prefix, suffix] = key.split("_")

        // if suffix exists
        if (suffix !== undefined) {
            // append updated key to the nested
            const iteratedSuffix = suffix.length === 1 ? "" : "_".concat(suffix.slice(0, suffix.length - 1))
            const newKey = prefix.concat(iteratedSuffix)
            formEntryChildren.push([newKey, entry[1]])
        } else {
            
        }
    });
    
    if (formEntryChildren.length > 0) {

    } 

    return {}
}


export const actions = {

	get: async (event) => {
		
	},
    post: async ({ request }) => {
        const formData = await request.formData();

        // const recipeNestedFormElementDict = {
        //     "recipeName" : "name",
        //     "recipeDescription": "description",
        //     "recipeInstruction": [],
        //     "recipeIngredients"
        //     "recipeIngredientName"
        // }

        // const recipeName: string | undefined = formData.get("recipeName")?.toString();
        // const recipeDescription: string | undefined = formData.get("recipeDescription")?.toString();

        // const recipeInstructions: string[] = []
        // let i = 0;
        // while(formData.get("recipeInstruction".concat(i.toString()))) {
        //     const recipeInstruction: string | undefined = formData.get("recipeInstruction".concat(i.toString()))?.toString()
        //     if (recipeInstruction !== undefined) recipeInstructions.push(recipeInstruction)
        //     i++;
        // }
        
        extractRecipeFormElements({}, formData)

        // this object is should have the keys be the same as the form but the values be in the
        // const sampleRecipeFormReturn: RecipeFormData = {}
        

        const ingredientFormFields = {
            "recipeIngredientName": {},
            "recipeIngredientPortionMetric": {}, 
            "recipeIngredientPortionAmount": {}
        }
        
        // const recipeIngredients: FoodItem[] | undefined = []
        // let  = 0;
        // while(formData.get("recipeInstruction".concat(i.toString()))) {
        //     const recipeInstruction: string | undefined = formData.get("recipeInstruction".concat(i.toString()))?.toString()
        //     if (recipeInstruction !== undefined) recipeInstructions.push(recipeInstruction)
        //     i++;
        // }
        
        
        // const recipeInstructions: string[] | undefined = filteredInstructions.map((kvpair) => {
        //     kvpair.
        //     return [""]
        // })

        
        
        // const recipe: Recipe = {

        //     name: recipeName,
        //     description: recipeDescription,
        //     orderedInstructions: string[],

        //     ingredients: FoodItem[]
        // }
        
    }
} satisfies Actions;