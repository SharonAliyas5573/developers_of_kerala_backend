from fastapi import APIRouter, Form, HTTPException, Depends
from app.db.engine import db
from app.api.deps import get_current_user


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

@router.get("/list")
async def list_contact_messages(current_user: dict = Depends(get_current_user)):
    try:
        waitlist_messages = list(db.contact.find({}, {"_id": 0, "email": 1, "message": 1}))
        return {"waitlist_messages": waitlist_messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing contact messages: {str(e)}")