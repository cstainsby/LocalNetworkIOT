

<script lang="ts">
    import type { Recipe } from "$lib/foodBasedTypes";
    import { onDestroy, onMount } from "svelte";

    const LOCALSTORE_RECIPE_FORM_KEY = "newRecipeFormData"

    let newRecipe: Recipe = {
        name: '',
        description: '',
        orderedInstructions: [],
        ingredients: []
    };

    let isSaving = false;
    let changesMade = false

    const addInstruction = () => {
        newRecipe.orderedInstructions.push("");
        newRecipe.orderedInstructions = [...newRecipe.orderedInstructions]
    };
    const removeInstruction = (index: number) => {
        newRecipe.orderedInstructions.splice(index, 1);
        newRecipe.orderedInstructions = [...newRecipe.orderedInstructions]
    };
  
    const addIngredient = () => {
        newRecipe.ingredients.push({ name: '', portionMetric: '', portionAmount: 0 });
        newRecipe.ingredients = [...newRecipe.ingredients]
    };
    const removeIngredient = (index: number) => {
        newRecipe.ingredients.splice(index, 1);
        newRecipe.ingredients = [...newRecipe.ingredients]
    };
  
    const submitRecipe = () => {
        const savedRecipeFormData = localStorage.getItem(LOCALSTORE_RECIPE_FORM_KEY)
        if (savedRecipeFormData !== undefined && savedRecipeFormData !== null) {
            localStorage.removeItem(LOCALSTORE_RECIPE_FORM_KEY)
        }
    };


    const handleFormChange = (event) => {
        if (changesMade === false) {
            changesMade = true
        }

        // if (event.target !== null && event.target.value != null) {
        //     // the currently held object already has the updated changes
        //     localStorage.setItem(LOCALSTORE_RECIPE_FORM_KEY, JSON.stringify(newRecipe))
        // }
    }

    // onMount(async () => {
    //     const savedRecipeFormData = localStorage.getItem(LOCALSTORE_RECIPE_FORM_KEY)
    //     if (savedRecipeFormData !== undefined && savedRecipeFormData !== null) {
    //         newRecipe = JSON.parse(savedRecipeFormData)
    //     }
    // })

    // onDestroy(() => {
    //     if (typeof window !== 'undefined' && typeof localStorage !== 'undefined') {
    //         const savedRecipeFormData = localStorage.getItem(LOCALSTORE_RECIPE_FORM_KEY)
    //         if (savedRecipeFormData !== undefined && savedRecipeFormData !== null) {
    //             localStorage.removeItem(LOCALSTORE_RECIPE_FORM_KEY)
    //         }
    //     }
    // })

</script>

<style lang="scss">
    form {
        display: flex;
        flex-direction: column;

        label {
            display: flex;
            flex-direction: column;

            & > * {
                margin: 4px;
            }
        }

        input[type="text"],
        textarea {
            width: auto;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }

        .submit-button {
            margin-top: 12px;
            width: 96px;
            height: 48px;
        }

        .multiple-item-input-header {
            display: flex;
            flex-direction: row;
            align-items: center;

            & > * {
                padding-right: 8px;
            }

            & > button {
                width: 72px;
                height: 24px;
            }
        }

        ul {
            list-style-type: none;
            margin: 0px;

            // li {
            //     margin: 12px;
            //     padding: 12px;
            //     background-color: lightblue;
            //     border-radius: 4px;

            //     label {
            //         display: flex;
            //         flex-direction: column;
            //         margin: 12px;
            //     }
            // }
        }
    }
</style>
  
<h1>Create a New Recipe</h1>
<!-- {#if changesMade}
    {#if isSaving} 
    <p>Saving...</p>
    {:else}
    <p>Saved</p>
    {/if}
{/if} -->


<form method="post" action="?/post" on:change={handleFormChange}>
    <label>
        <h3>Title:</h3>
        <input name="recipeName" type="text" bind:value="{newRecipe.name}" />
    </label>

    <label>
        <h3>Description:</h3>
        <textarea name="recipeDescription" bind:value="{newRecipe.description}" rows="4"></textarea>
    </label>

    <div class="multiple-item-input-header">
        <h3>Instructions</h3>
        <button type="button" on:click="{addInstruction}">Add</button>
    </div>
    <ul>
        {#each newRecipe.orderedInstructions as instruction, index} 
            <li>
                <div class="listed-item-header">
                    <b>Instruction {index}:</b>
                    <button type="button" on:click="{() => removeInstruction(index)}">Remove Ingredient</button>
                </div>
                <label>
                    <textarea name="recipeInstruction_{index}" bind:value="{instruction}" />
                </label>
            </li>
        {/each}
    </ul>

    <!-- Ingredients -->
    <div class="multiple-item-input-header">
        <h3>Ingredients</h3>
        <button type="button" on:click="{addIngredient}">Add</button>
    </div>
    <ul>
    {#each newRecipe.ingredients as ingredient, index}
        <li class="ingredient">
            <div class="recipe-header">
                <b>Ingredient {index}:</b>
                <button type="button" on:click="{() => removeIngredient(index)}">Remove Ingredient</button>
            </div>
            <label>
                Ingredient Name:
                <input name="recipeIngredientName_{index}" type="text" bind:value="{ingredient.name}" />
            </label>

            <label>
                Portion Metric:
                <input name="recipeIngredientPortionMetric_{index}" type="text" bind:value="{ingredient.portionMetric}" />
            </label>

            <label>
                Portion Amount:
                <input name="recipeIngredientPortionAmount_{index}" type="number" step="1" bind:value="{ingredient.portionAmount}" />
            </label>
        </li>
    {/each}
    </ul>

    <button class="submit-button" type="submit">Save</button>
</form>
  

<!-- <div>

    <form method="POST" action="?/post">

    </form>
</div> -->