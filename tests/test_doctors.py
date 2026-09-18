import uuid
def test_get_doctors_without_authentication(client):
    response = client.get("/api/v1/doctors")

    assert response.status_code == 401 
    

# Test authenticated GET doctors ...... 
def test_get_doctors_with_authentication(client, auth_headers):
    response = client.get(
        "/api/v1/doctors",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.get_json()

    assert response_data is not None 
    
# Test creating a doctor ....
def test_create_doctor(client, auth_headers):
    unique_id = uuid.uuid4().hex[:8]
    unique_phone = f"9{unique_id[:9]}"

    response = client.post(
        "/api/v1/doctors",
        headers=auth_headers,
        json={
            "first_name": f"Test{unique_id}",
            "last_name": "Doctor",
            "email": f"doctor_{unique_id}@example.com",
            "phone": unique_phone,
            "specialization": "Cardiologist",
            "department_id": 1
        }
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code in [200, 201]

    response_data = response.get_json()

    assert response_data is not None
    assert response_data["id"] is not None 
    
# Test getting a doctor by ID ..................
def test_get_doctor_by_id(client, auth_headers):
    response = client.get(
        "/api/v1/doctors/1",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.get_json()

    assert response_data is not None
    assert response_data["id"] == 1 
    

# Test getting a non-existent doctor .......
def test_get_nonexistent_doctor(client, auth_headers):
    response = client.get(
        "/api/v1/doctors/999999",
        headers=auth_headers
    )

    assert response.status_code == 404 
    
    
# Test updating a doctor .....................
def test_update_doctor(client, auth_headers):
    unique_id = uuid.uuid4().hex[:8]
    unique_phone = str(9000000000 + int(unique_id, 16) % 1000000000)

    create_response = client.post(
        "/api/v1/doctors",
        headers=auth_headers,
        json={
            "first_name": f"Update{unique_id}",
            "last_name": "Doctor",
            "email": f"update_doctor_{unique_id}@example.com",
            "phone": unique_phone,
            "specialization": "Cardiologist",
            "department_id": 1
        }
    )

    assert create_response.status_code in [200, 201]

    created_data = create_response.get_json()
    doctor_id = created_data["id"]

    update_response = client.put(
        f"/api/v1/doctors/{doctor_id}",
        headers=auth_headers,
        json={
            "first_name": f"Updated{unique_id}",
            "last_name": "Specialist",
            "email": f"updated_doctor_{unique_id}@example.com",
            "phone": str(int(unique_phone) + 1),
            "specialization": "Neurologist",
            "department_id": 1
        }
    )

    assert update_response.status_code == 200

    get_response = client.get(
        f"/api/v1/doctors/{doctor_id}",
        headers=auth_headers
    )

    assert get_response.status_code == 200

    updated_data = get_response.get_json()

    assert updated_data["id"] == doctor_id
    assert updated_data["first_name"] == f"Updated{unique_id}"
    assert updated_data["last_name"] == "Specialist"
    assert updated_data["specialization"] == "Neurologist" 
    
    
    
# Test deleting a doctor ......................
def test_delete_doctor(client, auth_headers):
    unique_id = uuid.uuid4().hex[:8]
    unique_phone = str(9000000000 + int(unique_id, 16) % 1000000000)

    create_response = client.post(
        "/api/v1/doctors",
        headers=auth_headers,
        json={
            "first_name": f"Delete{unique_id}",
            "last_name": "Doctor",
            "email": f"delete_doctor_{unique_id}@example.com",
            "phone": unique_phone,
            "specialization": "Cardiologist",
            "department_id": 1
        }
    )

    assert create_response.status_code in [200, 201]

    created_data = create_response.get_json()
    doctor_id = created_data["id"]

    delete_response = client.delete(
        f"/api/v1/doctors/{doctor_id}",
        headers=auth_headers
    )

    assert delete_response.status_code in [200, 204]

    get_response = client.get(
        f"/api/v1/doctors/{doctor_id}",
        headers=auth_headers
    )

    assert get_response.status_code == 404
    
    
    
# Test updating a non-existent doctor.............
def test_update_nonexistent_doctor(client, auth_headers):
    response = client.put(
        "/api/v1/doctors/999999",
        headers=auth_headers,
        json={
            "first_name": "Missing",
            "last_name": "Doctor",
            "email": "missing_doctor@example.com",
            "phone": "9123456789",
            "specialization": "Cardiologist",
            "department_id": 1
        }
    )

    assert response.status_code == 404
    


# Test deleting a non-existent doctor .................
def test_delete_nonexistent_doctor(client, auth_headers):
    response = client.delete(
        "/api/v1/doctors/999999",
        headers=auth_headers
    )

    assert response.status_code == 404