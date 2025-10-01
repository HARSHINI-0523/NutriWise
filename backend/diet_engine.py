# diet_engine.py
import pandas as pd
import numpy as np
import random
import warnings
warnings.filterwarnings('ignore')



# --- CONFIGURATION ---
FILE_PATH = './data/indb_with_recipe.xlsx'
# Standard RDAs (Recommended Dietary Allowances)
RDAS = {
    'calcium_mg': 1000, 'iron_mg': 18, 'potassium_mg': 3500,
    'vitc_mg': 90, 'folate_ug': 400, 'vitb12_ug': 2.4
}

# --- 1. DATA PROCESSOR CLASS (ENHANCED WITH TAGGING) ---
class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self._load_and_process_data()

    def _load_and_process_data(self):
        print("1. Loading and Processing Nutritional Data...")
        try:
            df = pd.read_excel(self.file_path)
        except FileNotFoundError:
            print(f"ERROR: File not found at '{self.file_path}'. Please update the FILE_PATH variable.")
            return pd.DataFrame()

        nutrient_cols = [
            'energy_kcal', 'carb_g', 'protein_g', 'fat_g', 'freesugar_g', 'fibre_g', 'sfa_mg',
            'mufa_mg', 'pufa_mg', 'cholesterol_mg', 'calcium_mg', 'potassium_mg', 'iron_mg',
            'vitc_mg', 'folate_ug', 'vitb12_ug'
        ]
        df = df.rename(columns={'food_name': 'DishName', 'type (Course)': 'MealCourse', 'Diet type': 'DietType'})
        df['DietType'] = df['DietType'].fillna('Veg').astype(str).str.lower().replace({'veg': 'vegetarian', 'non-veg': 'non-vegetarian', 'nan': 'vegetarian'})
        df['Ingredients'] = df['Ingredient'].fillna('').astype(str).str.lower()
        df['DishNameLower'] = df['DishName'].str.lower()
        for col in nutrient_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            else:
                df[col] = 0
        df['sfa_g'] = df['sfa_mg'] / 1000

        self._add_heuristic_tags(df)
        print("   ...Data loading and processing complete.")
        return df

    def _add_heuristic_tags(self, df):
        """NEW: Add heuristic tags for meal slots and sensitivities."""
        def assign_meal_slot(name):
            if any(k in name for k in ['idli', 'dosa', 'poha', 'upma', 'paratha', 'oats', 'porridge', 'omelette', 'thepla']): return 'Breakfast'
            if any(k in name for k in ['soup', 'juice', 'cooler', 'sharbat', 'lassi', 'milkshake']): return 'Brunch/Supper'
            if any(k in name for k in ['biscuit', 'pakora', 'samosa', 'vada', 'chaat', 'kebab', 'cutlet']): return 'Snack'
            return 'Lunch/Dinner'

        def assign_dairy_tag(row):
            dairy_keywords = ['milk', 'yogurt', 'curd', 'paneer', 'rabri', 'cheese', 'lassi', 'buttermilk']
            text_to_check = row['DishNameLower'] + " " + row['Ingredients']
            return any(keyword in text_to_check for keyword in dairy_keywords)

        df['MealSlotHeuristic'] = df['DishNameLower'].apply(assign_meal_slot)
        df['is_dairy'] = df.apply(assign_dairy_tag, axis=1)

# --- 2. USER PROFILE & CONSTRAINT GENERATOR CLASS (ENHANCED) ---
class UserProfile:
    def __init__(self, user_data_json):
        self.profile = user_data_json
        self.constraints = self._calculate_all_constraints()

    def _calculate_bmr_tdee(self):
        p = self.profile['anthropometry']
        if p['gender'].lower() == 'male':
            bmr = 88.362 + (13.397 * p['weight_kg']) + (4.799 * p['height_cm']) - (5.677 * p['age'])
        else:
            bmr = 447.593 + (9.247 * p['weight_kg']) + (3.098 * p['height_cm']) - (4.330 * p['age'])
        activity_multipliers = {'sedentary': 1.2, 'light': 1.375, 'moderate': 1.55, 'active': 1.725, 'very active': 1.9}
        tdee = bmr * activity_multipliers.get(p['activity_level'].lower(), 1.375)
        goal = self.profile.get('goal', 'maintenance').lower()
        if goal == 'weight loss': tdee -= 500
        elif goal == 'weight gain': tdee += 500
        return round(tdee)

    def _calculate_all_constraints(self):
        print("2. Calculating User-Specific Nutritional Constraints...")
        target_kcal = self._calculate_bmr_tdee()
        constraints = {
            'Target_Kcal': target_kcal,
            'Min_Protein_g': round((target_kcal * 0.25) / 4), # Increased protein goal
            'Max_Carb_g': round((target_kcal * 0.45) / 4),
            'Max_Fat_g': round((target_kcal * 0.30) / 9),
            'Max_Sodium_mg': 2300, 'Max_Sugar_g': 25, 'Max_SFA_g': round((target_kcal * 0.1) / 9),
            'Max_Cholesterol_mg': 300, 'Min_Fibre_g': 28,
            'Diet_Type': self.profile.get('diet_preference', 'vegetarian').lower(),
            'Allergies': [a.lower().strip() for a in self.profile.get('allergies', [])],
            'Sensitivities': [s.lower().strip() for s in self.profile.get('sensitivities', [])], # NEW
            'Micronutrients': RDAS
        }
        conditions = [c.lower() for c in self.profile.get('pre_medical_conditions', [])]
        if 'diabetes' in conditions:
            constraints.update({'Max_Carb_g': round((target_kcal * 0.40) / 4), 'Min_Fibre_g': 30, 'Max_Sugar_g': 15})
        if 'hypertension' in conditions: constraints['Max_Sodium_mg'] = 1500
        if 'high cholesterol' in conditions:
            constraints.update({'Max_Fat_g': round((target_kcal * 0.25) / 9), 'Max_SFA_g': round((target_kcal * 0.07) / 9), 'Max_Cholesterol_mg': 200})
        print("   ...Constraints calculation complete.")
        return constraints

# --- 3. RE-ENGINEERED DIET PLANNER CLASS ---
class DietPlanner:
    def __init__(self, data_processor, user_profile):
        self.df = data_processor.df
        self.constraints = user_profile.constraints
        self.meal_kcal_targets = self._get_meal_targets()
        self.meal_slots_ordered = ['Breakfast', 'Brunch', 'Lunch', 'Snack', 'Dinner', 'Supper']
        # MODIFIED: Expanded blacklist for better health alignment
        self.unhealthy_keywords = [
            'pastry', 'fried', 'namkeen', 'cake', 'cookie', 'ladoo', 'halwa', 'burfi', 'jamun', 'chikki',
            'jelly', 'custard', 'rabri', 'rasmalai', 'pickle', 'achaar', 'malpua', 'ice cream'
        ]

    def _get_meal_targets(self):
        cal = self.constraints['Target_Kcal']
        return {'Breakfast': cal * 0.20, 'Brunch': cal * 0.10, 'Lunch': cal * 0.30, 'Snack': cal * 0.10, 'Dinner': cal * 0.25, 'Supper': cal * 0.05}

    def _apply_base_filters(self):
        df = self.df[self.df['DietType'] == self.constraints['Diet_Type']].copy()
        for allergy in self.constraints['Allergies']:
            if allergy: df = df[~df['Ingredients'].str.contains(allergy)]
        df = df[(df['energy_kcal'] > 20) & (df['protein_g'] > 1)]
        return df

    def _get_dishes_for_slot(self, df, meal_slot):
        """MODIFIED: Applies much stricter health-based filtering for each slot."""
        candidates = df.copy()
        is_main_meal = meal_slot in ['Breakfast', 'Lunch', 'Dinner']

        # General health filter: low sugar, decent fiber
        candidates = candidates[candidates['freesugar_g'] < 10]

        if is_main_meal:
            for keyword in self.unhealthy_keywords:
                candidates = candidates[~candidates['DishNameLower'].str.contains(keyword)]
            # Ensure main meals are substantial
            candidates = candidates[(candidates['protein_g'] > 5) & (candidates['fibre_g'] > 1)]

        if meal_slot == 'Breakfast': return candidates[candidates['MealSlotHeuristic'] == 'Breakfast']
        if meal_slot in ['Brunch', 'Supper']: return candidates[candidates['MealSlotHeuristic'] == 'Brunch/Supper']
        if meal_slot == 'Snack': return candidates[candidates['MealSlotHeuristic'] == 'Snack']
        if meal_slot in ['Lunch', 'Dinner']: return candidates[candidates['MealSlotHeuristic'] == 'Lunch/Dinner']

        return df

    def _select_best_dish(self, dishes_df, calorie_target):
        """MODIFIED: Re-weighted scoring and random selection for variety."""
        if dishes_df.empty: return None

        # Re-weighted scoring to prioritize protein and fiber for satiety
        dishes_df['cal_score'] = 1 - (abs(dishes_df['energy_kcal'] - calorie_target) / calorie_target)
        dishes_df['protein_score'] = dishes_df['protein_g'] / 20  # Normalize by a high protein value
        dishes_df['fibre_score'] = dishes_df['fibre_g'] / 10 # Normalize by a high fiber value
        dishes_df['final_score'] = (dishes_df['cal_score'] * 0.2) + (dishes_df['protein_score'] * 0.5) + (dishes_df['fibre_score'] * 0.3)

        # NEW: Select randomly from the top 10 best options to ensure variety
        top_dishes = dishes_df.sort_values('final_score', ascending=False).head(10)
        return top_dishes.sample(1).iloc[0] if not top_dishes.empty else None

    def _create_meal_from_dish(self, dish, meal_slot, calorie_target):
        dish_kcal_per_100g = dish['energy_kcal'] if dish['energy_kcal'] > 0 else 1
        portion_g = max(50, min(400, (calorie_target / dish_kcal_per_100g) * 100))
        meal = {'MealSlot': meal_slot, 'DishName': dish['DishName']} # Simplified for final output
        # Store full data for validation later
        meal['_full_data'] = dish.to_dict()
        meal['_portion_g'] = int(portion_g)
        return meal

    def generate_7_day_plan(self):
        print("3. Generating Improved 7-Day Diet Plan...")
        weekly_plan = {}
        filtered_dishes = self._apply_base_filters()

        used_weekly_dishes = set()
        for d in range(1, 8):
            daily_plan = []
            used_dishes_today = set()
            dairy_count_today = 0
            max_dairy = 2 if 'dairy' in self.constraints['Sensitivities'] else 6

            for slot in self.meal_slots_ordered:
                calorie_target = self.meal_kcal_targets[slot]

                # Filter out dishes already used this week for better variety
                available_dishes = filtered_dishes[~filtered_dishes['DishName'].isin(used_weekly_dishes)]
                if len(available_dishes) < 20: # Fallback if we run out of unique dishes
                    available_dishes = filtered_dishes[~filtered_dishes['DishName'].isin(used_dishes_today)]

                slot_candidates = self._get_dishes_for_slot(available_dishes, slot)

                # NEW: Handle dairy sensitivity
                if dairy_count_today >= max_dairy:
                    slot_candidates = slot_candidates[slot_candidates['is_dairy'] == False]

                if slot_candidates.empty: continue

                best_dish = self._select_best_dish(slot_candidates, calorie_target)
                if best_dish is not None:
                    meal = self._create_meal_from_dish(best_dish, slot, calorie_target)
                    daily_plan.append(meal)
                    used_dishes_today.add(best_dish['DishName'])
                    if best_dish['is_dairy']:
                        dairy_count_today += 1

            if daily_plan:
                weekly_plan[f"Day {d}"] = daily_plan
                used_weekly_dishes.update(used_dishes_today)

        print("   ...Improved 7-Day plan generated.")
        return weekly_plan

class NutriWiseEngine:
    """
    Singleton-style wrapper to hold the loaded data in memory
    and process user requests.
    """
    def __init__(self, file_path):
        print(f"Initializing NutriWise Diet Engine...")
        # Load data ONCE during initialization
        self.data_processor = DataProcessor(file_path)
        if self.data_processor.df.empty:
            raise Exception("CRITICAL: Could not load food database file.")
        print("Engine Ready.")

    def generate_clean_plan(self, user_json_data):
        """
        The main entry point for the backend.
        Takes user JSON, returns the clean meal plan JSON.
        """
        try:
            # 1. Create Profile
            user_profile = UserProfile(user_json_data)
            
            # 2. Generate Plan
            planner = DietPlanner(self.data_processor, user_profile)
            raw_weekly_plan = planner.generate_7_day_plan()

            # 3. Clean and Format Output (The format you requested)
            clean_output = {}
            if raw_weekly_plan:
                for day, meals in raw_weekly_plan.items():
                    # Sort meals correctly
                    sorted_meals = sorted(meals, key=lambda x: planner.meal_slots_ordered.index(x['MealSlot']))
                    
                    # Create simple list of {slot: dish}
                    day_schedule = []
                    for meal in sorted_meals:
                        day_schedule.append({
                            "slot": meal['MealSlot'],
                            "dish": meal['DishName']
                            # Add 'id' here if your DB has dish IDs for connecting to recipes
                        })
                    clean_output[day] = day_schedule
                
                return {
                    "status": "success",
                    "plan": clean_output,
                    # Optional: Include calculated targets for frontend display
                    "targets": user_profile.constraints 
                }
            else:
                return {
                    "status": "error",
                    "message": "Could not generate a plan matching these constraints."
                }

        except Exception as e:
            print(f"Error generating plan: {e}")
            return {"status": "error", "message": str(e)}