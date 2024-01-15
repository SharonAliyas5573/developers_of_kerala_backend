"""
developer.py

This module contains the data models for handling operations related to developers.
"""
from typing import Optional, List, Annotated
from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from bson import ObjectId


class DeveloperRole(str, Enum):
    frontend = "frontend"
    backend = "backend"
    fullstack = "fullstack"
    mobile = "mobile"
    devops = "devops"
    data_engineer = "data_engineer"


class DeveloperProfile(BaseModel):
    name: str = Field(default=None)
    email: EmailStr = Field(default=None)
    profile_pic: Optional[str] = Field(default=None)  # s3 address for profile pic
    contact: str = Field(default=None)
    role: DeveloperRole = Field(default=None)
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
                "role": "backend",
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

    name: str = Field(default=None)
    email: EmailStr = Field(default=None)
    profile_pic: str = Field(default=None)
    contact: str = Field(default=None)
    role: DeveloperRole = Field(default=None)
    skills: List[str] = Field(default=[])
    experience: str = Field(default="nil")
    education: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
    socials: Optional[dict] = Field(default=None)
    website: Optional[str] = Field(default=None)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Developer Name",
                "email": "developer@company.com",
                "profile_pic": "s3://bucket/profile_pic.jpg",
                "contact": "+91xxxxxxxxx",
                "role": "backend",
                "skills": ["Python", "FastAPI"],
                "experience": "5 years",
                "education": "Bachelor's in Computer Science",
                "location": "Location from Google Maps API",
                "socials": {"LinkedIn": "<link>"},
                "website": "https://developer.com",
            }
        }
