import pytest
from fastapi.testclient import TestClient

def test_start_chat(client, test_db):
    """Test starting a chat between a business and a user"""
    from app.user_account.models import User
    user = User(id=1, username="chatuser", email="chat@user.com")
    test_db.add(user)
    
    from app.feedback.models import BusinessUser
    business = BusinessUser(
        id=1,
        email="chat@business.com",
        business_name="Chat Business",
        address="123 Chat St",
        town_city="Chat City",
        type="Restaurant"
    )
    test_db.add(business)
    test_db.commit()
    
    response = client.post(
        "/chat/start",
        json={
            "business_email": "chat@business.com",
            "user_email": "chat@user.com",
            "message": "Hello, I'd like to discuss my recent experience."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["message"] == "Chat started"
    
    return data["session_id"]

def test_send_message(client, test_db):
    """Test sending a message in an existing chat"""
    session_id = test_start_chat(client, test_db)
    
    response = client.post(
        "/chat/send",
        json={
            "session_id": session_id,
            "message": "Thank you for reaching out. How can I help?",
            "sender": "chat@business.com",
            "receiver": "chat@user.com"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Message sent"}

def test_get_chat_history(client, test_db):
    """Test retrieving chat history"""
    session_id = test_start_chat(client, test_db)
    
    client.post(
        "/chat/send",
        json={
            "session_id": session_id,
            "message": "Thank you for reaching out. How can I help?",
            "sender": "chat@business.com",
            "receiver": "chat@user.com"
        }
    )
    
    response = client.get(f"/chat/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # At least 2 messages (initial + response)
    assert data[0]["message"] == "Hello, I'd like to discuss my recent experience."
    assert data[1]["message"] == "Thank you for reaching out. How can I help?"
