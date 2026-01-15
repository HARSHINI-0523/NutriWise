def scale_portion(food, target_calories):
    factor = target_calories / food.calories

    return {
        "food_name": food.food_name,
        "portion_g": round(food.serving_size_g * factor),
        "household_measure": food.household_measure,
        "calories": round(food.calories * factor),
        "protein_g": round(food.protein_g * factor, 1),
        "carbs_g": round(food.carbs_g * factor, 1),
        "fat_g": round(food.fat_g * factor, 1)
    }
