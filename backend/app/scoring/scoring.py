def score_food(food, user, base_score):
    score = base_score

    if "diabetes" in user["conditions"]:
        if food.low_gi_candidate:
            score += 2
        if food.carbs_g > 50:
            score -= 1

    if "anemia" in user["conditions"] and food.iron_rich:
        score += 3

    if "hypertension" in user["conditions"] and food.low_sodium:
        score += 2

    return score
