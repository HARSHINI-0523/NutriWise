from collections import defaultdict
from app.planner.daily_planner import build_day
from app.planner.variety_optimizer import update_usage

def build_week(df, user):
    week = {}
    usage = defaultdict(int)

    for day in range(1, 8):
        blocked = {f for f, c in usage.items() if c >= 2}
        meals = build_day(df, user, blocked)
        update_usage(usage, meals)
        week[f"Day {day}"] = meals

    return week
