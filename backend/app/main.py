from fastapi import FastAPI
from app.api.meal_plan import router

app = FastAPI(title="NutriWise AI Diet Engine")

app.include_router(router)
