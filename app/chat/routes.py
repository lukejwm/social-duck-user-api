from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from . import models, schemas
from app.user_account import models as user_models
from app.feedback import models as feedback_models
from uuid import uuid4

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/start")
def start_chat(chat_data: schemas.StartChatRequest, db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter_by(email=chat_data.user_email).first()
    business = db.query(feedback_models.BusinessUser).filter_by(email=chat_data.business_email).first()
    
    if not user or not business:
        raise HTTPException(status_code=404, detail="User or business not found")
    
    session_id = str(uuid4())
    new_entry = models.ChatHistory(
        session_id=session_id,
        business_id=business.id,
        business_email=business.email,
        user_id=user.id,
        user_email=user.email,
        message=chat_data.message,
        sender=user.email,
        receiver=business.email,
    )
    db.add(new_entry)
    db.commit()
    
    return {"session_id": session_id, "message": "Chat started"}

@router.post("/send")
def send_message(msg_data: schemas.SendMessageRequest, db: Session = Depends(get_db)):
    chat_session = db.query(models.ChatHistory).filter_by(session_id=msg_data.session_id).first()
    
    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    new_msg = models.ChatHistory(
        session_id=msg_data.session_id,
        business_id=chat_session.business_id,
        business_email=chat_session.business_email,
        user_id=chat_session.user_id,
        user_email=chat_session.user_email,
        message=msg_data.message,
        sender=msg_data.sender,
        receiver=msg_data.receiver,
    )
    db.add(new_msg)
    db.commit()
    
    return {"message": "Message sent"}

@router.get("/{session_id}", response_model=list[schemas.ChatHistory])
def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    history = db.query(models.ChatHistory).filter_by(session_id=session_id).order_by(models.ChatHistory.timestamp).all()
    
    if not history:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    return history
