import uuid
# testing authentication test ......
def test_get_departments_requires_authentication(client):
    response = client.get("/api/v1/departments")

    assert response.status_code == 401
    
    
# Step 2: Test authenticated department listing ....
def test_get_departments_with_authentication(client, auth_headers):
    response = client.get(
        "/api/v1/departments",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.get_json()

    assert isinstance(response_data, list) 
    

# test getting a department by ID....
def test_get_department_by_id(client, auth_headers):
    response = client.get(
        "/api/v1/departments/1",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.get_json()

    assert isinstance(response_data, dict)
    assert response_data["id"] == 1
    

# test a non-existent department......
def test_get_nonexistent_department(client, auth_headers):
    response = client.get(
        "/api/v1/departments/999999",
        headers=auth_headers
    )

    assert response.status_code == 404 
    

# create department test ................
def test_create_department(client, auth_headers):
    unique_id = uuid.uuid4().hex[:8]

    response = client.post(
        "/api/v1/departments",
        headers=auth_headers,
        json={
            "name": f"Test Department {unique_id}",
            "description": "Department created during testing"
        }
    )

    assert response.status_code in [200, 201]

    response_data = response.get_json()

    assert response_data["id"] is not None
    assert response_data["name"] == f"Test Department {unique_id}"
    
    
# test updating a department......
def test_update_department(client, auth_headers):
    unique_id = uuid.uuid4().hex[:8]

    create_response = client.post(
        "/api/v1/departments",
        headers=auth_headers,
        json={
            "name": f"Update Department {unique_id}",
            "description": "Original description"
        }
    )

    assert create_response.status_code in [200, 201]

    created_data = create_response.get_json()
    department_id = created_data["id"]

    update_response = client.put(
        f"/api/v1/departments/{department_id}",
        headers=auth_headers,
        json={
            "name": f"Updated Department {unique_id}",
            "description": "Updated description"
        }
    )

    assert update_response.status_code == 200

    get_response = client.get(
        f"/api/v1/departments/{department_id}",
        headers=auth_headers
    )

    assert get_response.status_code == 200

    updated_data = get_response.get_json()

    assert updated_data["id"] == department_id
    assert updated_data["name"] == f"Updated Department {unique_id}"
    assert updated_data["description"] == "Updated description"
    
    
# Add department delete test......
def test_delete_department(client, auth_headers):
    unique_id = uuid.uuid4().hex[:8]

    create_response = client.post(
        "/api/v1/departments",
        headers=auth_headers,
        json={
            "name": f"Delete Department {unique_id}",
            "description": "Department to be deleted"
        }
    )

    assert create_response.status_code in [200, 201]

    created_data = create_response.get_json()
    department_id = created_data["id"]

    delete_response = client.delete(
        f"/api/v1/departments/{department_id}",
        headers=auth_headers
    )

    assert delete_response.status_code in [200, 204]

    get_response = client.get(
        f"/api/v1/departments/{department_id}",
        headers=auth_headers
    )

    assert get_response.status_code == 404


# add a test for updating a non-existent department.....
def test_update_nonexistent_department(client, auth_headers):
    response = client.put(
        "/api/v1/departments/999999",
        headers=auth_headers,
        json={
            "name": "Updated Missing Department",
            "description": "This department does not exist"
        }
    )

    assert response.status_code == 404
    
    
# Test deleting a non-existent department .............4
def test_delete_nonexistent_department(client, auth_headers):
    response = client.delete(
        "/api/v1/departments/999999",
        headers=auth_headers
    )

    assert response.status_code == 404