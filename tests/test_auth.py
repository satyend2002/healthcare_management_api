def test_login_success(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "admin",
            "password": "Admin@123"
        }
    )

    assert response.status_code == 200

    response_data = response.get_json()

    assert response_data["message"] == "Login successful"
    assert "access_token" in response_data
    assert "refresh_token" in response_data 
    
    
    
def test_login_invalid_password(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "admin",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401

    response_data = response.get_json()

    assert response_data["message"] == "Invalid username or password"