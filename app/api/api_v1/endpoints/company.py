from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.company import CompanyProfile, UpdateCompanyProfileModel
from app.db.engine import db

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
        dict: A dictionary containing the list of companies.
            Each company is represented as a dictionary with the "_id" field converted to a string.
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
