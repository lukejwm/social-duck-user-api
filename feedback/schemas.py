from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    city: str

class BusinessInfo(BaseModel):
    business_name: str
    address: str
    town_city: str
    type: str

    class Config:
        orm_mode = True