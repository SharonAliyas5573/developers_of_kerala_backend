from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import List
from dotenv import load_dotenv
import os
import json
from database import db
from models import Developer  # Import your ODMantic models
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

mongodb_uri = os.environ.get('MONGODB_URI')
print("mongo db uri:",mongodb_uri)

@app.get("/",response_class=HTMLResponse)
async def read_root():
    return "<h1>Hello Kerala Developers!</h1>"

# example endpoint for mongo db interaction
@app.post("/insert_tree/")
async def insert_tree(tree_data: str):
    try:
        # Insert tree data into the collection
        tree_dict = {'tree_data':tree_data}
        result = db.test_tree.insert_one(tree_dict)
        if result.inserted_id:
            return {"message": "Tree inserted successfully", "tree_id": str(result.inserted_id)}
        else:
            raise HTTPException(status_code=500, detail="Failed to insert tree")
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Tree with same ID already exists")



@app.post("/submit_email/")
async def submit_email(email: str = Form(...)):
    print(f"Received email: {email}")
    try:
        result = db.waitlist.insert_one({'email': email})
        if result.inserted_id:
            return {"message": "Email inserted successfully", "email_id": str(result.inserted_id)}
        else:
            raise HTTPException(status_code=500, detail="Failed to insert")
    except Exception as e:
        return {"exception": str(e)}


from fastapi import HTTPException

@app.post("/create_developer/")
async def create_developer(name: str, place: str, skills: str, email: str, resume: str = None):
    try:
        # Create a dictionary for developer data
        developer_data = {
            "name": name,
            "place": place,
            "skills": skills,
            "email": email,
            "resume": resume
        }

        # Insert the developer data into the collection
        result = db.developers_talent.insert_one(developer_data)
        
        if result.inserted_id:
            return {"message": "Developer created successfully", "developer_id": str(result.inserted_id)}
        else:
            raise HTTPException(status_code=500, detail="Failed to create developer")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create developer: {str(e)}")



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


