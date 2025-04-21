from fastapi import FastAPI
from database import Base, engine
from user_account.routes import router as user_router
from feedback.routes import router as feedback_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount user routes
app.include_router(user_router)
app.include_router(feedback_router)