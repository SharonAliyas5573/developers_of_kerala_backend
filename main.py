from re import S
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pymongo.errors import DuplicateKeyError ,ServerSelectionTimeoutError
from passlib.context import CryptContext

from datetime import datetime, timedelta
from bson import ObjectId
from typing import List , Optional
from dotenv import load_dotenv
import os
import json

from database import db
from models import Developer , User # Import your ODMantic models
from authentication import create_access_token, verify_token
# Load environment variables from .env file
load_dotenv()
# FastAPI intialization
app = FastAPI()
# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>Hello Kerala Developers!</h1>"


# example endpoint for mongo db interaction
@app.post("/insert_tree/")
async def insert_tree(tree_data: str):
    try:
        # Insert tree data into the collection
        tree_dict = {"tree_data": tree_data}
        result = db.test_tree.insert_one(tree_dict)
        if result.inserted_id:
            return {
                "message": "Tree inserted successfully",
                "tree_id": str(result.inserted_id),
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to insert tree")
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Tree with same ID already exists")


@app.post("/submit_email/")
async def submit_email(email: str = Form(...)):
    print(f"Received email: {email}")
    try:
        result = db.waitlist.insert_one({"email": email})
        if result.inserted_id:
            return {
                "message": "Email inserted successfully",
                "email_id": str(result.inserted_id),
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to insert")
    except Exception as e:
        return {"exception": str(e)}




@app.post("/create_developer/")
async def create_developer(
    name: str, place: str, skills: str, email: str, resume: Optional[str] = None
):
    try:
        # Create a dictionary for developer data
        developer_data = {
            "name": name,
            "place": place,
            "skills": skills,
            "email": email,
            "resume": resume,
        }

        # Insert the developer data into the collection
        result = db.developers_talent.insert_one(developer_data)

        if result.inserted_id:
            return {
                "message": "Developer created successfully",
                "developer_id": str(result.inserted_id),
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create developer")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create developer: {str(e)}"
        )


@app.get("/list_developers/")
async def list_developers():
    # try:
    # Fetch all developers from the collection
    developers = db.developers_talent.find()

    # Convert MongoDB cursor to list of dictionaries with ObjectId converted to string
    developers_list = [
        {**developer, "_id": str(developer["_id"])} for developer in developers
    ]

    # Return the list of developers
    return developers_list


# except Exception as e:
#     raise HTTPException(status_code=500, detail=f"Failed to fetch developers")


@app.get("/check_db")
async def check_db_connection():
    try:
        # The ismaster command is cheap and does not require auth.
        db.command("ismaster")
        
        return {"status": "Database is connected"}
    except ServerSelectionTimeoutError as e:
        return {"status": "Database connection failed", "exception": str(e)}

# Endppoint for user registration
@app.post("/register")
async def register_user(
    username: str = Form(...), 
    email: str = Form(...), 
    hashed_password: str = Form(...)
):
    user_dict = {"username": username, "email": email, "hashed_password": hashed_password}
    user_dict["hashed_password"] = pwd_context.hash(user_dict["hashed_password"])
    result = db.users.insert_one(user_dict)
    if result.acknowledged:
        return {"message": "User registered successfully", "user_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to register user")
    
# Endpoint for user login
@app.post("/login")
async def generate_token(username: str = Form(...), password: str = Form(...)):
    user =  db.users.find_one({"username": username})
    if user and pwd_context.verify(password, user["hashed_password"]):
        token_data = {"sub": str(user["_id"]), "username": user["username"]}
        token = create_access_token(token_data)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")