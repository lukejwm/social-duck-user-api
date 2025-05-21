import pytest
from fastapi.testclient import TestClient

def test_register_user(client):
    """Test registering a new user"""
    response = client.post(
        "/users",
        json={
            "username": "testuser",
            "email": "test@example.com"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_register_duplicate_username(client):
    """Test registering a user with a duplicate username"""
    client.post(
        "/users",
        json={
            "username": "duplicate",
            "email": "first@example.com"
        }
    )
    
    response = client.post(
        "/users",
        json={
            "username": "duplicate",
            "email": "second@example.com"
        }
    )
    assert response.status_code == 400
    assert "Username or email already exists" in response.json()["detail"]

def test_register_duplicate_email(client):
    """Test registering a user with a duplicate email"""
    client.post(
        "/users",
        json={
            "username": "first",
            "email": "duplicate@example.com"
        }
    )
    
    response = client.post(
        "/users",
        json={
            "username": "second",
            "email": "duplicate@example.com"
        }
    )
    assert response.status_code == 400
    assert "Username or email already exists" in response.json()["detail"]
