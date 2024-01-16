"""
developer.py

This module contains the data models for handling operations related to developers.
"""
from typing import Optional, List, Annotated
from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from bson import ObjectId


PyObjectId = Annotated[str, Field(alias="_id", default=None)]


class DeveloperRole(str, Enum):
    frontend = "frontend"
    backend = "backend"
    fullstack = "fullstack"
    mobile = "mobile"
    devops = "devops"
    data_engineer = "data_engineer"


class DeveloperProfile(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    profile_pic: Optional[str] = Field(default=None)  # s3 address for profile pic
    contact: Optional[str] = Field(default=None)
    developer_role: Optional[DeveloperRole] = Field(default=None)
    skills: List[str] = Field(default=[])
    experience: str = Field(default="nil")
    education: Optional[str] = Field(default=None)
    location: str = Field(default=None)  # link from google maps
    socials: Optional[dict] = Field(default=None)  # e.g., {"LinkedIn": "<link>", etc}
    website: Optional[str] = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "name": "Developer Name",
                "email": "developer@company.com",
                "profile_pic": "s3://bucket/profile_pic.jpg",
                "contact": "+91xxxxxxxxx",
                "developer_role": "backend",
                "skills": ["Python", "FastAPI"],
                "experience": "5 years",
                "education": "Bachelor's in Computer Science",
                "location": "Location from Google Maps API",
                "socials": {"LinkedIn": "<link>"},
                "website": "https://developer.com",
            }
        }


class UpdateDeveloperModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_pic: Optional[str] = None
    contact: Optional[str] = None
    developer_role: Optional[DeveloperRole] = None
    skills: Optional[List[str]] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    location: Optional[str] = None
    socials: Optional[dict] = None
    website: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Developer Name",
                "email": "developer@company.com",
                "profile_pic": "s3://bucket/profile_pic.jpg",
                "contact": "+91xxxxxxxxx",
                "developer_role": "backend",
                "skills": ["Python", "FastAPI"],
                "experience": "5 years",
                "education": "Bachelor's in Computer Science",
                "location": "Location from Google Maps API",
                "socials": {"LinkedIn": "<link>"},
                "website": "https://developer.com",
            }
        }
