"""
developers.py

This module contains the routes for handling operations related to developers.
"""
from fastapi import APIRouter, HTTPException, Body, Depends
from fastapi.responses import JSONResponse
from app.schemas.developer import DeveloperProfile, UpdateDeveloperModel
from app.db.engine import db
from bson import ObjectId
from pymongo import ReturnDocument

router = APIRouter()


@router.get(
    "/",
    response_description="List all developers",
    response_model=UpdateDeveloperModel,
    response_model_by_alias=False,
    responses={
        404: {"description": "No developers found"},
        401: {"description": "Unauthorized"},
        200: {"description": "Successful Response"},
    },
)
async def retrieve_developer_list():
    """
    Retrieve the list of developers from the collection.

    Returns:
    - dict: A dictionary containing the list of developers.

    Raises:
    - HTTPException: If there is an error while retrieving the developer list.
    """
    try:
        # Fetch all developers from the collection
        developers = db.Developers.find()
        developer_list = [
            {**developer, "_id": str(developer["_id"])} for developer in developers
        ]
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "data": developer_list,
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
    response_description="Get a single Developer Profile",
    response_model=DeveloperProfile,
    response_model_by_alias=False,
    responses={
        404: {"description": "Developer not found"},
        401: {"description": "Unauthorized"},
        200: {"description": "Successful Response"},
    },
)
async def get_developer(id: str):
    """
    Get the record for a specific developer, looked up by `id`.

    Parameters:
    - id (str): The ID of the developer to retrieve.

    Returns:
    - dict: The developer profile.

    Raises:
    - HTTPException: If the developer with the specified ID is not found.
    """
    try:
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Invalid ObjectId: {id}")

    if (developer := db.Developers.find_one({"_id": object_id})) is not None:
        developer["_id"] = str(developer["_id"])  # Convert ObjectId to string
        return developer

    raise HTTPException(status_code=404, detail=f"Developer {id} not found")


@router.put(
    "/{id}",
    response_description="Update Developer Profile",
    response_model=DeveloperProfile,
    response_model_by_alias=False,
)
async def update_developer(id: str, developer: UpdateDeveloperModel = Body(...)):
    """
    Update individual fields of an existing developer profile.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.

    Parameters:
    - id (str): The ID of the developer profile to be updated.
    - developer (UpdateDeveloperModel): The updated developer profile data.

    Returns:
    - DeveloperProfile: The updated developer profile.

    Raises:
    - HTTPException: If the developer profile with the given ID is not found.
    """
    developer_dict = developer.dict(by_alias=True)
    developer_updates = {k: v for k, v in developer_dict.items() if v is not None}
    if developer_updates:
        updated_developer = db.Developers.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": developer_updates},
            return_document=ReturnDocument.AFTER,
            upsert=True,
        )

        if updated_developer:
            updated_developer["_id"] = str(
                updated_developer["_id"]
            )  # Convert ObjectId to string
            return updated_developer

    # The update is empty, but we should still return the matching document:
    if (developer := db.Developers.find_one({"_id": ObjectId(id)})) is not None:
        developer["_id"] = str(developer["_id"])  # Convert ObjectId to string
        return developer

    raise HTTPException(status_code=404, detail=f"Developer {id} not found")
