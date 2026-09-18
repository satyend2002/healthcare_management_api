import uuid
def test_get_patients_requires_authentication(client):
    response = client.get("/api/v1/patients")

    assert response.status_code == 401


def test_get_patients_with_authentication(client, auth_headers):
    response = client.get(
        "/api/v1/patients",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.get_json()

    assert response_data["success"] is True
    assert "data" in response_data


def test_create_patient(client, auth_headers):
    unique_id = uuid.uuid4().hex[:8]

    response = client.post(
        "/api/v1/patients",
        headers=auth_headers,
        json={
            "first_name": "Test",
            "last_name": "Patient",
            "phone": f"9{unique_id}",
            "email": f"testpatient_{unique_id}@example.com",
            "gender": "Male",
            "date_of_birth": "1995-01-01"
        }
    )

    assert response.status_code in [200, 201]

    response_data = response.get_json()

    assert response_data["success"] is True
    assert "data" in response_data 
    
    
def test_get_patient_by_id(client, auth_headers):
    unique_id = uuid.uuid4().hex[:8]

    create_response = client.post(
        "/api/v1/patients",
        headers=auth_headers,
        json={
            "first_name": "Detail",
            "last_name": "Patient",
            "phone": f"8{unique_id}",
            "email": f"detail_{unique_id}@example.com",
            "gender": "Male",
            "date_of_birth": "1995-01-01"
        }
    )

    assert create_response.status_code in [200, 201]

    created_data = create_response.get_json()["data"]
    patient_id = created_data["id"]

    response = client.get(
        f"/api/v1/patients/{patient_id}",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.get_json()

    assert response_data["success"] is True
    assert "data" in response_data
    assert response_data["data"]["id"] == patient_id
    
    
    
def test_update_patient(client, auth_headers):
    unique_id = uuid.uuid4().hex[:8]

    create_response = client.post(
        "/api/v1/patients",
        headers=auth_headers,
        json={
            "first_name": "Update",
            "last_name": "Patient",
            "phone": f"7{unique_id}",
            "email": f"update_{unique_id}@example.com",
            "gender": "Male",
            "date_of_birth": "1995-01-01"
        }
    )

    assert create_response.status_code in [200, 201]

    patient_id = create_response.get_json()["data"]["id"]

    update_response = client.put(
        f"/api/v1/patients/{patient_id}",
        headers=auth_headers,
        json={
            "first_name": "Updated"
        }
    )

    assert update_response.status_code == 200

    response_data = update_response.get_json()

    assert response_data["success"] is True
    assert response_data["data"]["first_name"] == "Updated" 


def test_delete_patient(client, auth_headers):
    unique_id = uuid.uuid4().hex[:8]

    create_response = client.post(
        "/api/v1/patients",
        headers=auth_headers,
        json={
            "first_name": "Delete",
            "last_name": "Patient",
            "phone": f"6{unique_id}",
            "email": f"delete_{unique_id}@example.com",
            "gender": "Male",
            "date_of_birth": "1995-01-01"
        }
    )

    assert create_response.status_code in [200, 201]

    patient_id = create_response.get_json()["data"]["id"]

    delete_response = client.delete(
        f"/api/v1/patients/{patient_id}",
        headers=auth_headers
    )

    assert delete_response.status_code in [200, 204]

    get_response = client.get(
        f"/api/v1/patients/{patient_id}",
        headers=auth_headers
    )

    assert get_response.status_code == 404 
    

## Adding negative test if trying to fetch patients that are not exists  ..... 
def test_get_nonexistent_patient(client, auth_headers):
    response = client.get(
        "/api/v1/patients/999999",
        headers=auth_headers
    )

    assert response.status_code == 404

    response_data = response.get_json()

    assert response_data["success"] is False
    assert response_data["message"] == "Patient not found" 
    

# update non-existent patient test: ......
def test_update_nonexistent_patient(client, auth_headers):
    response = client.put(
        "/api/v1/patients/999999",
        headers=auth_headers,
        json={
            "first_name": "Updated"
        }
    )

    assert response.status_code == 404

    response_data = response.get_json()

    assert response_data["success"] is False
    assert response_data["message"] == "Patient not found" 
    

# Deleting non-existing patients .......................
def test_delete_nonexistent_patient(client, auth_headers):
    response = client.delete(
        "/api/v1/patients/999999",
        headers=auth_headers
    )

    assert response.status_code == 404

    response_data = response.get_json()

    assert response_data["success"] is False
    assert response_data["message"] == "Patient not found"