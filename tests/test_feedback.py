import pytest
from fastapi.testclient import TestClient
import os
from io import BytesIO

def test_submit_feedback_form(client):
    """Test submitting the feedback form"""
    response = client.post(
        "/feedback/submit",
        data={
            "username": "testuser",
            "business_name": "Test Business",
            "title": "Great Experience",
            "body": "I had a wonderful time at this business.",
            "star_rating": "5"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Feedback submitted successfully"}

def test_create_feedback(client, test_db):
    """Test creating feedback with all details"""
    from app.user_account.models import User
    user = User(id=1, username="feedbackuser", email="feedback@example.com")
    test_db.add(user)
    
    from app.feedback.models import BusinessUser
    business = BusinessUser(
        id=1,
        email="business@example.com",
        business_name="Feedback Business",
        address="123 Feedback St",
        town_city="Feedback City",
        type="Restaurant"
    )
    test_db.add(business)
    test_db.commit()
    
    photo_content = b"test photo content"
    photo = BytesIO(photo_content)
    photo.name = "test_photo.jpg"
    
    response = client.post(
        "/feedback/create",
        data={
            "username": "feedbackuser",
            "business_name": "Feedback Business",
            "title": "Detailed Review",
            "body": "This is a detailed review of my experience.",
            "star_rating": "2"
        },
        files={"photo": ("test_photo.jpg", photo, "image/jpeg")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Negative feedback submitted. Business will be alerted."
    assert "feedback_id" in data

def test_positive_feedback(client, test_db):
    """Test creating positive feedback"""
    from app.user_account.models import User
    user = User(id=2, username="positivefeedback", email="positive@example.com")
    test_db.add(user)
    
    from app.feedback.models import BusinessUser
    business = BusinessUser(
        id=2,
        email="positive@business.com",
        business_name="Positive Business",
        address="456 Positive St",
        town_city="Positive City",
        type="Retail"
    )
    test_db.add(business)
    test_db.commit()
    
    response = client.post(
        "/feedback/create",
        data={
            "username": "positivefeedback",
            "business_name": "Positive Business",
            "title": "Excellent Service",
            "body": "The service was excellent!",
            "star_rating": "5"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Feedback submitted successfully"}
