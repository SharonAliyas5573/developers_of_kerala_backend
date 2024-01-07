from pydantic import BaseModel, EmailStr 
from typing import List , Optional
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    developer = "developer"
    company = "company"


# Common fields for both developers and companies
class UserRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.developer
    

# Developer-specific fields
class DeveloperProfileUpdate(BaseModel):
    intro: str
    skills: List[str]
    experience: int
    location: str
    resume: str  # s3 address for resume
    qualifications: str
    certifications: List[str]
    achievements: str
    projects: List[str]
    socials: dict  # e.g., {"LinkedIn": "<link>", etc}


class OpeningStatus(str, Enum):
    active = "active"
    closed = "closed"
    paused = "paused"


class Opening(BaseModel):
    skills_needed: List[str]
    qualification_required: str
    job_role: str
    job_description: str
    no_of_openings: int = 1
    status: OpeningStatus = OpeningStatus.active


# Company-specific fields
class CompanyProfileUpdate(BaseModel):
    name: Optional[str] = None
    full_name: Optional[str] = None
    profile_pic: Optional[str] = None  # s3 address for profile pic
    contact: Optional[str] = None
    industry: Optional[str] = None
    detail_intro: Optional[str] = None
    location: Optional[str] =None  # get from google maps api
    openings: Optional[List[Opening]] = None
    socials: Optional[dict] = None # e.g., {"LinkedIn": "<link>", etc}
    website: Optional[str] = None
    