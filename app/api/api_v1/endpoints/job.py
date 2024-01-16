from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from app.schemas.company import CompanyProfile, UpdateCompanyProfileModel
from app.db.engine import db
from bson import ObjectId
from pymongo import ReturnDocument

router = APIRouter()
