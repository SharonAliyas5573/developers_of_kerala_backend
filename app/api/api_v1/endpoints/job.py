from fastapi import APIRouter, Query
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from app.schemas.company import (
    CompanyProfile,
    UpdateCompanyProfileModel,
    Opening,
    OpeningUpdate,
    OpeningOut,
)
from app.db.engine import db
from bson import ObjectId
from pymongo import ReturnDocument
from typing import List

router = APIRouter()


@router.get(
    "/list",
    response_description="Get a list of all job postings",
    response_model=List[OpeningOut],
    response_model_by_alias=False,
    responses={
        401: {"description": "Unauthorized"},
        200: {"description": "Successful Response"},
    },
)
async def get_job_list():
    try:
        # Assuming db is your MongoDB connection object
        # and Opening is your MongoDB collection
        job_list = list(db.Opening.find())

        # Convert ObjectId to string for each job in the result
        job_list = [{**job, "_id": str(job["_id"])} for job in job_list]

        return job_list
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve job list: {str(e)}"
        )


@router.post(
    "/post",
    response_description="Create a new job posting",
    # response_model=Opening,
    response_model_by_alias=False,
    responses={
        401: {"description": "Unauthorized"},
        201: {"description": "Job posting created successfully"},
    },
)
async def post_job(job: Opening):
    print("opening:", job.dict())
    try:
        # Assuming db is your MongoDB connection object
        # and Opening is your MongoDB collection
        new_job = db.Opening.insert_one(job.model_dump(by_alias=True))

        # You can get the inserted document from the database
        # using the inserted_id and return it in the response
        inserted_job = db.Opening.find_one({"_id": new_job.inserted_id})
        # Convert ObjectId to string for serialization
        inserted_job["_id"] = str(inserted_job["_id"])
        return {"message": "Job posting created successfully", "job": inserted_job}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")


@router.get(
    "/search",
    response_description="Search for developers based on criteria",
    response_model=list[OpeningOut],
    response_model_by_alias=False,
    responses={
        404: {"description": "No openings found"},
        401: {"description": "Unauthorized"},
        200: {"description": "Successful Response"},
    },
)
async def search_jobs(
    field: str = Query(..., description="The field to search by"),
    value: str = Query(..., description="The value to search for"),
):
    """
    Search for companies based on a specific field and value.

    Parameters:
    - field (str): The field to search by (e.g., "company_name", "industry", etc.).
    - value (str): The value to search for in the specified field.

    Returns:
    - List[CompanyProfile]: A list of companies matching the search criteria.

    Raises:
    - HTTPException: If there is an error during the search or no companies are found.
    """
    try:
        # Create a dynamic query to find companies based on the provided field and value
        search_query = {field: {"$regex": value, "$options": "i"}}
        print("search_query:", search_query)
        openings = db.Opening.find(search_query)
        # Convert ObjectId to string for each company in the result
        opening_list = [{**opening, "_id": str(opening["_id"])} for opening in openings]

        print("opening_list", opening_list)
        if not opening_list:
            raise HTTPException(status_code=404, detail=f"No developers found")

        return opening_list
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": str(e),
            },
        )


@router.put(
    "/update",
    response_description="Update a job posting",
    response_model=OpeningUpdate,
    response_model_by_alias=False,
    responses={
        401: {"description": "Unauthorized"},
        200: {"description": "Job posting updated successfully"},
        404: {"description": "Job not found"},
        500: {"description": "Internal Server Error"},
    },
)
async def update_job(job_id: str, updated_job: Opening):
    try:
        # Convert job_id to ObjectId
        job_object_id = ObjectId(job_id)
        print(job_object_id)
        # Check if the job exists
        existing_job = db.Opening.find_one({"_id": job_object_id})
        print("existing_job:", existing_job, updated_job.model_dump())
        if not existing_job:
            raise HTTPException(status_code=404, detail="Job not found")

        updated_job = db.Opening.find_one_and_update(
            {"_id": job_object_id},
            {"$set": updated_job.model_dump()},
            return_document=ReturnDocument.AFTER,
        )

        print("updated_job---------------------", updated_job)
        # Return the updated job
        # updated_job_dict = {**existing_job, **updated_job.model_dump()}
        if updated_job:
            updated_job["_id"] = str(updated_job["_id"])  # Convert ObjectId to string
            return updated_job

    except HTTPException:
        # Re-raise HTTPException to keep the status code and detail intact
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update job: {str(e)}")


@router.delete(
    "/delete",
    response_description="Delete a job posting",
    # response_model=Opening,
    response_model_by_alias=False,
    responses={
        401: {"description": "Unauthorized"},
        200: {"description": "Job posting deleted successfully"},
    },
)
async def delete_job(job_id: str):
    try:
        # Assuming db is your MongoDB connection object
        # and Opening is your MongoDB collection
        try:
            job_object_id = ObjectId(job_id)
        except Exception:
            raise HTTPException(status_code=404, detail=f"Invalid ObjectId: {id}")
        deleted_job = db.Opening.find_one_and_delete({"_id": job_object_id})
        if deleted_job:
            deleted_job["_id"] = str(deleted_job["_id"])
            return {"message": "Job posting deleted successfully", "job": deleted_job}
        else:
            raise HTTPException(status_code=404, detail="Job not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete job: {str(e)}")
