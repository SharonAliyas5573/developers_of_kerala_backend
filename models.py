from pydantic import BaseModel, EmailStr
from typing import List
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
    role: UserRole = UserRole.developer # default role is developer

class UserProfileUpdate(BaseModel):
    full_name: str
    profile_pic: str  # s3 address for profile picture
    contact: str
    #add more fields here


# Developer-specific fields
class DeveloperProfileUpdate(UserProfileUpdate):
    intro: str
    skills: List[str]
    experience: int
    location: str
    resume: str  # s3 address for resume
    qualifications: str
    certifications: List[str]
    achievements: str
    projects: List[str]
    socials: dict  # e.g., {"LinkedIn": "<link>", "GitHub": "<link>", "Twitter": "<link>"}
    
    
# Company-specific fields
class CompanyProfileUpdate(UserProfileUpdate):
    industry: str
    detail_intro: str
    location: str
    open_positions: dict  # e.g., {"Software Engineer": 3, "Data Scientist": 2}
    skills_needed: List[str]
    qualification_required: str
    job_role: str
    job_description: str
    
class UserReference(BaseModel):
    user_info: UserRegistration
    profile_info: UserProfileUpdate
    developer_info: DeveloperProfileUpdate = None
    company_info: CompanyProfileUpdate = None
