from fastapi import APIRouter, Form, HTTPException
from app.db.engine import db

router = APIRouter()


@router.post("/submit")
async def submit_waitlist_email(email: str = Form(...)):
    print(f"Received waitlist email: {email}")
    try:
        result = db.waitlist.insert_one({"email": email})
        if result.inserted_id:
            return {
                "message": "Waitlist email submitted successfully",
                "email_id": str(result.inserted_id),
            }
        else:
            raise HTTPException(
                status_code=500, detail="Waitlist email submission failed"
            )
    except Exception as e:
        return {"error": str(e)}
