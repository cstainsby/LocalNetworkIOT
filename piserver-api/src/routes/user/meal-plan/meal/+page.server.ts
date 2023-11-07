import type { Actions } from './$types';

import type { Recipe, FoodItem } from '$lib/foodBasedTypes';


/**
 * Recipe form data type 
 * Form data shape:
 *  recipeName
 *  recipeDescription 
 *  recipeInstruction_<(<0..n>)1..n>
 *  recipeIngredient_<0..n>
 */
interface RecipeFormData_Ingredient {
    name?: string,
    portion_metric?: string,
    portion_amount?: string
}
interface RecipeFormData_Recipe {
    recipe_name?: string,
    recipe_description?: string,
    recipe_instructions?: string[]
    recipe_ingredients?: RecipeFormData_Ingredient[]
}

interface GenericFormData {
    [key: string]: string | string[] | GenericFormData | GenericFormData[] | undefined
}


function extractRecipeFormDataElements(formData: FormData): RecipeFormData_Recipe {
    const rawFormData = extractFormDataElements(formData)

    const recipeName = (rawFormData.recipename) ? rawFormData.recipename as string : ""
    const recipeDescription = (rawFormData.recipedescription) ? rawFormData.recipedescription as string : ""
    const recipeInstructions = (rawFormData.recipeinstructions) ? (rawFormData.recipeinstructions as string[]): []

    const recipeIngredientObject = (rawFormData.recipeingredients) 
        ? (rawFormData.recipeingredients as GenericFormData): {}
    const ingredientNames = (recipeIngredientObject && recipeIngredientObject.name) 
        ? (recipeIngredientObject.name as string[]): []
    const ingredientPortionMetrics = (recipeIngredientObject && recipeIngredientObject.portionmetric) 
        ? (recipeIngredientObject.portionmetric as string[]): []
    const ingredientPortionAmounts = (recipeIngredientObject && recipeIngredientObject.portionamount) 
        ? (recipeIngredientObject.portionamount as string[]): []

    const recipeIngredients: RecipeFormData_Ingredient[] = []
    for (let index = 0; index < ingredientNames.length; index++) {
        // iterate using ingredient names - they are required
        const name = ingredientNames[index];
        const portionMetric = ingredientPortionMetrics[index];
        const portionAmount = ingredientPortionAmounts[index];

        recipeIngredients.push({
            name: name,
            portion_amount: portionAmount,
            portion_metric: portionMetric
        })
    }
    
    return {
        recipe_name: recipeName,
        recipe_description: recipeDescription,
        recipe_instructions: recipeInstructions,
        recipe_ingredients: recipeIngredients
    }
}

function extractFormDataElements(formData: FormData): GenericFormData {
    const formEntries = Array.from(formData.entries())
    // console.log(formEntries);
    
    let buildObject: GenericFormData = {};

    for (const [key, formEntryValue] of formEntries) {
        let currentObject = buildObject;
        const keys = key.split('_');
        const value = formEntryValue.toString()

        for (let i = 0; i < keys.length; i++) {
            const currentKey = keys[i];

            if (i === keys.length - 1) {
                // Last key, assign the value
                currentObject[currentKey] = value;
            } else {
                // Create nested object if it doesn't exist
                if (!currentObject[currentKey]) {
                    currentObject[currentKey] = !isNaN(Number(keys[i + 1])) 
                        ? [] as GenericFormData[]
                        : {} as GenericFormData;
                }

                // Move to the next level of the object
                currentObject = currentObject[currentKey] as GenericFormData;
            }
        }
    }

    return buildObject;
}


// function recipeFormDataToRecipe(recipeFormData: RecipeFormData_Recipe): Recipe | Error {

//     return {
//         name: recipeFormData.recipeName
//         description?: string,
//         orderedInstructions: string[],

//         ingredients: FoodItem[],
//     }
// }


export const actions = {

	get: async (event) => {
		
	},
    post: async ({ request }) => {
        const formData = await request.formData();

        
        
        const recipeFormData = extractRecipeFormDataElements(formData)
        // const createdRecipe = recipeFormDataToRecipe(recipeFormData)
        
        return { success: true }
    }
} satisfies Actions;