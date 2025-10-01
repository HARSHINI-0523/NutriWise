# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Import the engine from your other file
from diet_engine import NutriWiseEngine 

# --- Define the structure of the data your Node.js server will send ---
class Anthropometry(BaseModel):
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    activity_level: str

class UserRequest(BaseModel):
    user_id: str
    goal: str
    diet_preference: str
    pre_medical_conditions: List[str] = []
    allergies: List[str] = []
    sensitivities: List[str] = []
    anthropometry: Anthropometry

# --- Initialize the FastAPI app ---
app = FastAPI(title="NutriWise Diet Engine API")

# Define the file path for your dataset on the server
DATA_FILE_PATH = "./data/indb_with_recipe.xlsx" 
diet_engine = None

# --- Startup Event: Load the model ONCE when the server starts ---
@app.on_event("startup")
def load_engine():
    """This function runs only once, when the server starts up."""
    global diet_engine
    try:
        # Create an instance of our engine, which will load the large Excel file.
        diet_engine = NutriWiseEngine(DATA_FILE_PATH)
        print("NutriWise Diet Engine has been successfully loaded and is ready.")
    except Exception as e:
        print(f"FATAL: Could not start the Diet Engine: {e}")
        # In a real app, you might want the server to fail to start if this happens.

# --- The API Endpoint your Node.js backend will call ---
@app.post("/api/generate-plan")
def generate_diet_plan(user_request: UserRequest):
    """
    Receives user data, generates a diet plan, and returns it.
    """
    if not diet_engine:
        raise HTTPException(status_code=503, detail="Diet Engine is not available or failed to load.")
    
    # The user_request is a Pydantic model. Convert it to a dictionary.
    user_json = user_request.dict()
    
    # Call the engine's main function to get the plan
    result = diet_engine.generate_clean_plan(user_json)
    
    if result["status"] == "error":
        # If the plan couldn't be generated, send a 400 Bad Request error
        raise HTTPException(status_code=400, detail=result["message"])
        
    return result

# --- How to Run This Server ---
# In your VS Code terminal, run the following command:
# python -m uvicorn main:app --reload
#
# This will start a local server, usually at http://127.0.0.1:8000
# You can then send POST requests from your Node.js app to this address.