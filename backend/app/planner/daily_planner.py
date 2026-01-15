from app.rules.exclusions import is_excluded
from app.scoring.scoring import score_food
from app.planner.portion_scaling import scale_portion
from app.models.predictor import predict_base_scores

def build_day(df, user, used_foods):
    meals = {}
    daily_cal = user["calorie_target"] / 4

    for meal_type in ["breakfast", "lunch", "snack", "dinner"]:
        candidates = df[
            (df.meal_type == meal_type) &
            (~df.food_name.isin(used_foods))
        ]

        candidates = candidates[
            ~candidates.apply(lambda r: is_excluded(r, user), axis=1)
        ]

        if candidates.empty:
            continue

        base_scores = predict_base_scores(candidates)
        candidates = candidates.copy()
        candidates["score"] = [
            score_food(row, user, s)
            for row, s in zip(candidates.itertuples(), base_scores)
        ]

        best = candidates.sort_values("score", ascending=False).iloc[0]
        meals[meal_type] = scale_portion(best, daily_cal)

        used_foods.add(best.food_name)

    return meals
