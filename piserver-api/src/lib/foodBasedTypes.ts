

interface Recipe {
    name?: string, // recipe name
    description?: string,
    orderedInstructions: string[],

    ingredients: FoodItem[],
}

interface FoodItem {
    name: string,
    portionMetric: string,
    portionAmount:  number
}

interface MealPlan {
    breakfast?: Recipe,
    postBreakfastSnack?: Recipe,
    lunch?: Recipe,
    postLunchSnack?: Recipe,
    preWorkoutSnack?: Recipe,
    dinner?: Recipe,
    preBedSnack?: Recipe
}

export type {
    Recipe,
    FoodItem,
    MealPlan
}