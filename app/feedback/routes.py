from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas, models
from app.user_account import models as user_models
from typing import List
import shutil
import os

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("/business_search", response_model=List[schemas.BusinessInfo])
def submit_feedback(request: schemas.FeedbackRequest, db: Session = Depends(get_db)):
    city = request.city.strip()
    businesses = db.query(models.BusinessUser).filter(models.BusinessUser.town_city.ilike(city)).all()
    return businesses

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/feedback/create")
def create_feedback(
    username: str = Form(...),
    business_name: str = Form(...),
    title: str = Form(...),
    body: str = Form(...),
    star_rating: int = Form(...),
    photo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    if not (1 <= star_rating <= 5):
        raise HTTPException(status_code=400, detail="Star rating must be between 1 and 5")
    if len(title) < 10 or len(title) > 75:
        raise HTTPException(status_code=400, detail="Title must be between 10 and 75 characters")
    if len(body) < 20 or len(body) > 500:
        raise HTTPException(status_code=400, detail="Body must be between 20 and 500 characters")

    # Fetch user
    user = db.query(user_models.User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch business
    business = db.query(models.BusinessUser).filter_by(business_name=business_name).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    review_type = "Positive" if star_rating >= 4 else "Negative"

    photo_filename = None
    if photo:
        photo_filename = f"{username}_{photo.filename}"
        photo_path = os.path.join(UPLOAD_DIR, photo_filename)
        with open(photo_path, "wb") as f:
            shutil.copyfileobj(photo.file, f)

    feedback = models.Feedback(
        user_id=user.id,
        username=user.username,
        business_id=business.id,
        business_name=business.business_name,
        location=business.town_city,
        title=title,
        body=body,
        photo_filename=photo_filename,
        star_rating=star_rating,
        review_type=review_type
    )
    db.add(feedback)
    db.commit()
    
    if review_type == "Negative":
        return {"message": "Negative feedback submitted. Business will be alerted.", "feedback_id": feedback.id}
    
    return {"message": "Feedback submitted successfully"}
