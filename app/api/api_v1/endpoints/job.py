from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from app.schemas.company import (
    CompanyProfile,
    UpdateCompanyProfileModel,
    Opening,
    OpeningUpdate,
)
from app.db.engine import db
from bson import ObjectId
from pymongo import ReturnDocument

router = APIRouter()


@router.post(
    "/post",
    response_description="Create a new job posting",
    response_model=Opening,
    response_model_by_alias=False,
    responses={
        401: {"description": "Unauthorized"},
        201: {"description": "Job posting created successfully"},
    },
)
async def post_job(job: Opening):
    try:
        # Assuming db is your MongoDB connection object
        # and Opening is your MongoDB collection
        new_job = db.Opening.insert_one(job.model_dump(by_alias=True))

        # You can get the inserted document from the database
        # using the inserted_id and return it in the response
        inserted_job = db.Opening.find_one({"_id": new_job.inserted_id})

        return {"message": "Job posting created successfully", "job": inserted_job}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")


@router.get(
    "/search",
    response_description="Search for jobs",
    response_model=Opening,
    response_model_by_alias=False,
    responses={
        401: {"description": "Unauthorized"},
        200: {"description": "Successful Response"},
    },
)
async def search_jobs(query: str):
    # Your logic to search for jobs based on the query
    return {"message": "Jobs found", "query": query}


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
async def update_job(job_id: str, updated_job: OpeningUpdate):
    try:
        # Convert job_id to ObjectId
        job_object_id = ObjectId(job_id)

        # Check if the job exists
        existing_job = db.Opening.find_one({"_id": job_object_id})
        if not existing_job:
            raise HTTPException(status_code=404, detail="Job not found")

        # Update the job
        db.Opening.update_one(
            {"_id": job_object_id}, {"$set": updated_job.model_dump()}
        )

        # Return the updated job
        updated_job_dict = {**existing_job.dict(), **updated_job.model_dump()}
        return {"message": "Job posting updated successfully", "job": updated_job_dict}
    except HTTPException:
        # Re-raise HTTPException to keep the status code and detail intact
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update job: {str(e)}")


@router.delete(
    "/delete",
    response_description="Delete a job posting",
    response_model=Opening,
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
            return {"message": "Job posting deleted successfully", "job": deleted_job}
        else:
            raise HTTPException(status_code=404, detail="Job not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete job: {str(e)}")
