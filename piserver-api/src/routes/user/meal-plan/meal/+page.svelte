

<script lang="ts">
    import type { Recipe } from "$lib/foodBasedTypes";

    let newRecipe: Recipe = {
        name: '',
        description: '',
        orderedInstructions: [],
        ingredients: []
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
      // Handle submitting the recipe (you can implement this part)
      console.log('New Recipe:', newRecipe);
    };
</script>
  
<h1>Create a New Recipe</h1>

<form method="post" action="/user/meal-plan/meal/post">
    <label>
        Name:
        <input type="text" bind:value="{newRecipe.name}" />
    </label>
    <br />

    <label>
        Description:
        <textarea bind:value="{newRecipe.description}" rows="4"></textarea>
    </label>
    <br />

    <label>
        Instructions (comma-separated):
        <input type="text" bind:value="{newRecipe.orderedInstructions}" />
    </label>
    <br />

    <!-- Ingredients -->
    <h2>Ingredients</h2>
    <ul>
    {#each newRecipe.ingredients as ingredient, index}
        <li class="ingredient">
            <label>
                Ingredient Name:
                <input type="text" bind:value="{ingredient.name}" />
            </label>
            <br />

            <label>
                Portion Metric:
                <input type="text" bind:value="{ingredient.portionMetric}" />
            </label>
            <br />

            <label>
                Portion Amount:
                <input type="number" step="0.01" bind:value="{ingredient.portionAmount}" />
            </label>
            <br />

            <button type="button" on:click="{() => removeIngredient(index)}">Remove Ingredient</button>
        </li>
    {/each}
    </ul>

    <button type="button" on:click="{addIngredient}">Add Ingredient</button>

    <button type="submit">Submit Recipe</button>
</form>
  

<!-- <div>

    <form method="POST" action="?/post">

    </form>
</div> -->