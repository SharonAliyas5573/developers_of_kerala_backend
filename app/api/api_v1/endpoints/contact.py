from fastapi import APIRouter, Form, HTTPException
from app.db.engine import db

router = APIRouter()


@router.post("/submit")
async def submit_contact_form(email: str = Form(...), message: str = Form(...)):
    print(f"Received contact form from: {email}, message: {message}")
    try:
        result = db.contact.insert_one({"email": email, "message": message})
        if result.inserted_id:
            return {
                "message": "Contact form submitted successfully",
                "email_id": str(result.inserted_id),
            }
        else:
            raise HTTPException(
                status_code=500, detail="Contact form submission failed"
            )
    except Exception as e:
        return {"error": str(e)}
