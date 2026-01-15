import pandas as pd
from app.planner.weekly_planner import build_week
from app.rules.exclusions import is_excluded

def generate_meal_plan(user):
    df = pd.read_csv("app/data/nutriwise_food_core.csv")

    avoid = df[df.apply(lambda r: is_excluded(r, user), axis=1)]
    week_plan = build_week(df, user)

    return {
        "avoid_list": avoid.food_name.tolist(),
        "meal_plan": week_plan
    }
