def is_excluded(food, user):
    if food.calories > 800 or food.sodium_mg > 600:
        return True

    if "diabetes" in user["conditions"]:
        if food.free_sugar_g > 10:
            return True
        if food.carbs_g > 60 and food.fiber_g < 5:
            return True

    if "hypertension" in user["conditions"]:
        if food.sodium_mg >= 300:
            return True

    if "anemia" in user["conditions"]:
        if food.iron_mg < 1 and food.fiber_g < 2:
            return True

    if "pcos" in user["conditions"]:
        if food.free_sugar_g > 10:
            return True

    return False
