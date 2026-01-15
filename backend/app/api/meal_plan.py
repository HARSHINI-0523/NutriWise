from fastapi import APIRouter
from app.services.meal_plan_service import generate_meal_plan

router = APIRouter()

@router.post("/generate-meal-plan")
def generate(user: dict):
    return generate_meal_plan(user)
