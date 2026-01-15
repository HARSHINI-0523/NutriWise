def update_usage(used_counts, meals):
    for meal in meals.values():
        used_counts[meal["food_name"]] += 1
