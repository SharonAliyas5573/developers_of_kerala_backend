"""
company.py

This module contains the routes for handling operations related to companies.


"""
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from app.schemas.company import CompanyProfile, UpdateCompanyProfileModel
from app.db.engine import db
from bson import ObjectId
from pymongo import ReturnDocument

router = APIRouter()


@router.get(
    "/",
    response_description="List all companies",
    response_model=UpdateCompanyProfileModel,
    response_model_by_alias=False,
    responses={
        404: {"description": "No companies found"},
        401: {"description": "Unauthorized"},
        200: {"description": "Successful Response"},
    },
)
async def retrieve_company_list():
    """
    Retrieve the list of companies from the collection.

    Returns:
    - dict: A dictionary containing the list of companies.

    Raises:
    - HTTPException: If there is an error while retrieving the company list.
    """
    try:
        # Fetch all companies from the collection
        companies = db.UserRegistration.find({"role": "company"}, {"password": 0})
        company_list = [
            {**company, "_id": str(company["_id"])} for company in companies
        ]
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": company_list,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": str(e),
            },
        )


@router.get(
    "/{id}",
    response_description="Get a single Company Profile",
    response_model=CompanyProfile,
    response_model_by_alias=False,
    responses={
        404: {"description": "Company not found"},
        401: {"description": "Unauthorized"},
        200: {"description": "Successful Response"},
    },
)
async def get_company(id: str):
    """
    Get the record for a specific company, looked up by `id`.

    Parameters:
    - id (str): The ID of the company to retrieve.

    Returns:
    - dict: The company profile.

    Raises:
    - HTTPException: If the company with the specified ID is not found.
    """
    if (company := db.UserRegistration.find_one({"_id": ObjectId(id)})) is not None:
        company["_id"] = str(company["_id"])  # Convert ObjectId to string
        return company

    raise HTTPException(status_code=404, detail=f"company {id} not found")


@router.put(
    "/{id}",
    response_description="Update Company Profile",
    response_model=CompanyProfile,
    response_model_by_alias=False,
)
async def update_company(id: str, company: UpdateCompanyProfileModel = Body(...)):
    """
    Update individual fields of an existing company profile.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.

    Parameters:
    - id (str): The ID of the company profile to be updated.
    - company (UpdateCompanyProfileModel): The updated company profile data.

    Returns:
    - CompanyProfile: The updated company profile.

    Raises:
    - HTTPException: If the company profile with the given ID is not found.
    """
    company_dict = company.dict(by_alias=True)
    company_updates = {k: v for k, v in company_dict.items() if v is not None}
    if company_updates:
        updated_company = db.UserRegistration.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": company_updates},
            return_document=ReturnDocument.AFTER,
            upsert=True,
        )

        if updated_company:
            updated_company["_id"] = str(
                updated_company["_id"]
            )  # Convert ObjectId to string
            return updated_company

    # The update is empty, but we should still return the matching document:
    if (company := db.UserRegistration.find_one({"_id": ObjectId(id)})) is not None:
        company["_id"] = str(company["_id"])  # Convert ObjectId to string
        return company

    raise HTTPException(status_code=404, detail=f"company {id} not found")
