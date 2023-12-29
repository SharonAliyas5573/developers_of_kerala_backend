from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",response_class=HTMLResponse)
async def read_root():
    return "<h1>Hello Kerala Developers!</h1>"

@app.post("/submit_email/")
async def submit_email(email: str = Form(...)):
    print(f"Received email: {email}")
    return {"email": email}
