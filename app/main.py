from fastapi import FastAPI
from app.database import Base, engine
from app.user_account.routes import router as user_router
from app.feedback.routes import router as feedback_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount user routes
app.include_router(user_router)
app.include_router(feedback_router)