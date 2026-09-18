import uuid


def test_get_medicines_without_authentication(client):
    response = client.get("/api/v1/medicines")

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code in [401, 403]


def test_get_medicines_with_authentication(client, auth_headers):
    response = client.get(
        "/api/v1/medicines",
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 200
    


# add the Medicine CRUD tests, starting with creating a medicine  ..........
def test_create_medicine_with_authentication(client, auth_headers):
    unique_name = f"Test Medicine {uuid.uuid4().hex[:8]}"

    payload = {
        "name": unique_name,
        "generic_name": "Test Generic",
        "brand_name": "Test Brand",
        "strength": "500 mg",
        "dosage_form": "Tablet",
        "manufacturer": "Test Manufacturer",
        "stock_quantity": 100,
        "reorder_level": 10,
        "active": True
    }

    response = client.post(
        "/api/v1/medicines",
        json=payload,
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == unique_name
    assert data["stock_quantity"] == 100
    assert data["reorder_level"] == 10
    assert data["active"] is True
    
    

# add the GET medicine by ID test .........................
def test_get_medicine_by_id_with_authentication(client, auth_headers):
    unique_name = f"Get Medicine {uuid.uuid4().hex[:8]}"

    payload = {
        "name": unique_name,
        "generic_name": "Test Generic",
        "brand_name": "Test Brand",
        "strength": "500 mg",
        "dosage_form": "Tablet",
        "manufacturer": "Test Manufacturer",
        "stock_quantity": 100,
        "reorder_level": 10,
        "active": True
    }

    create_response = client.post(
        "/api/v1/medicines",
        json=payload,
        headers=auth_headers
    )

    assert create_response.status_code == 201

    medicine_id = create_response.get_json()["id"]

    response = client.get(
        f"/api/v1/medicines/{medicine_id}",
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == medicine_id
    assert data["name"] == unique_name 
    

# Update Medicine test .............................................................
def test_update_medicine_with_authentication(client, auth_headers):
    unique_name = f"Update Medicine {uuid.uuid4().hex[:8]}"

    payload = {
        "name": unique_name,
        "generic_name": "Test Generic",
        "brand_name": "Test Brand",
        "strength": "500 mg",
        "dosage_form": "Tablet",
        "manufacturer": "Test Manufacturer",
        "stock_quantity": 100,
        "reorder_level": 10,
        "active": True
    }

    create_response = client.post(
        "/api/v1/medicines",
        json=payload,
        headers=auth_headers
    )

    assert create_response.status_code == 201

    medicine_id = create_response.get_json()["id"]

    update_payload = {
        "stock_quantity": 150,
        "reorder_level": 20
    }

    response = client.put(
        f"/api/v1/medicines/{medicine_id}",
        json=update_payload,
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 200

    data = response.get_json()["medicine"]

    assert data["id"] == medicine_id
    assert data["stock_quantity"] == 150
    assert data["reorder_level"] == 20
    
    
# Delete Medicine ...................................................../
def test_delete_medicine_with_authentication(client, auth_headers):
    unique_name = f"Delete Medicine {uuid.uuid4().hex[:8]}"

    payload = {
        "name": unique_name,
        "generic_name": "Test Generic",
        "brand_name": "Test Brand",
        "strength": "500 mg",
        "dosage_form": "Tablet",
        "manufacturer": "Test Manufacturer",
        "stock_quantity": 100,
        "reorder_level": 10,
        "active": True
    }

    create_response = client.post(
        "/api/v1/medicines",
        json=payload,
        headers=auth_headers
    )

    assert create_response.status_code == 201

    medicine_id = create_response.get_json()["id"]

    response = client.delete(
        f"/api/v1/medicines/{medicine_id}",
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 200
    assert response.get_json()["message"] == \
        "Medicine deleted successfully"

    get_response = client.get(
        f"/api/v1/medicines/{medicine_id}",
        headers=auth_headers
    )

    assert get_response.status_code == 404

# Add Medicine validation tests ..........................
def test_create_medicine_with_invalid_data(client, auth_headers):
    payload = {
        "generic_name": "Missing Name",
        "stock_quantity": 100,
        "reorder_level": 10,
        "active": True
    }

    response = client.post(
        "/api/v1/medicines",
        json=payload,
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 400

    data = response.get_json()

    assert data["message"] == "Validation failed"
    assert "name" in data["errors"]
    

# Test medicine not found .....
def test_get_medicine_not_found(client, auth_headers):
    response = client.get(
        "/api/v1/medicines/999999",
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 404
    assert response.get_json()["message"] == "Medicine not found"
    
# Test invalid update data ............
def test_update_medicine_with_invalid_data(client, auth_headers):
    unique_name = f"Invalid Update Medicine {uuid.uuid4().hex[:8]}"

    payload = {
        "name": unique_name,
        "stock_quantity": 100,
        "reorder_level": 10,
        "active": True
    }

    create_response = client.post(
        "/api/v1/medicines",
        json=payload,
        headers=auth_headers
    )

    assert create_response.status_code == 201

    medicine_id = create_response.get_json()["id"]

    update_payload = {
        "stock_quantity": "invalid-stock"
    }

    response = client.put(
        f"/api/v1/medicines/{medicine_id}",
        json=update_payload,
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 400

    data = response.get_json()

    assert data["message"] == "Validation failed"
    assert "stock_quantity" in data["errors"] 
    


# Test empty request bodies .............
def test_create_medicine_without_request_body(client, auth_headers):
    response = client.post(
        "/api/v1/medicines",
        json={},
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 400
    assert response.get_json()["message"] == \
        "Request body must contain JSON data"
        
        
# Test pagination ......................
def test_get_medicines_with_pagination(client, auth_headers):
    response = client.get(
        "/api/v1/medicines?page=1&per_page=2",
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 200

    data = response.get_json()

    assert "pagination" in data
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["per_page"] == 2
    assert len(data["data"]) <= 2
    
    
    
# Test medicine search .......
def test_get_medicines_with_search(client, auth_headers):
    unique_name = f"Searchable Medicine {uuid.uuid4().hex[:8]}"

    payload = {
        "name": unique_name,
        "generic_name": "Search Generic",
        "brand_name": "Search Brand",
        "strength": "500 mg",
        "dosage_form": "Tablet",
        "manufacturer": "Test Manufacturer",
        "stock_quantity": 100,
        "reorder_level": 10,
        "active": True
    }

    create_response = client.post(
        "/api/v1/medicines",
        json=payload,
        headers=auth_headers
    )

    assert create_response.status_code == 201

    response = client.get(
        f"/api/v1/medicines?search={unique_name}",
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 200

    data = response.get_json()

    assert any(
        medicine["name"] == unique_name
        for medicine in data["data"]
    )
    

# Test active-status filtering .............
def test_get_medicines_with_active_filter(client, auth_headers):
    unique_name = f"Inactive Medicine {uuid.uuid4().hex[:8]}"

    payload = {
        "name": unique_name,
        "generic_name": "Inactive Generic",
        "brand_name": "Inactive Brand",
        "strength": "500 mg",
        "dosage_form": "Tablet",
        "manufacturer": "Test Manufacturer",
        "stock_quantity": 100,
        "reorder_level": 10,
        "active": False
    }

    create_response = client.post(
        "/api/v1/medicines",
        json=payload,
        headers=auth_headers
    )

    assert create_response.status_code == 201

    response = client.get(
        "/api/v1/medicines?active=false",
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 200

    data = response.get_json()

    assert any(
        medicine["name"] == unique_name
        and medicine["active"] is False
        for medicine in data["data"]
    )



# Test low-stock filtering .................
def test_get_medicines_with_low_stock_filter(client, auth_headers):
    unique_name = f"Low Stock Medicine {uuid.uuid4().hex[:8]}"

    payload = {
        "name": unique_name,
        "generic_name": "Low Stock Generic",
        "brand_name": "Low Stock Brand",
        "strength": "500 mg",
        "dosage_form": "Tablet",
        "manufacturer": "Test Manufacturer",
        "stock_quantity": 5,
        "reorder_level": 10,
        "active": True
    }

    create_response = client.post(
        "/api/v1/medicines",
        json=payload,
        headers=auth_headers
    )

    assert create_response.status_code == 201

    response = client.get(
        "/api/v1/medicines?low_stock=true",
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 200

    data = response.get_json()

    assert any(
        medicine["name"] == unique_name
        and medicine["stock_quantity"] < medicine["reorder_level"]
        for medicine in data["data"]
    )
    


# Test sorting .........................
def test_get_medicines_with_sorting(client, auth_headers):
    response = client.get(
        "/api/v1/medicines?sort_by=stock_quantity&order=desc",
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 200

    data = response.get_json()["data"]

    stock_values = [
        medicine["stock_quantity"]
        for medicine in data
        if medicine["stock_quantity"] is not None
    ]

    assert stock_values == sorted(
        stock_values,
        reverse=True
    )
    
    
# Test invalid pagination parameters .................
def test_get_medicines_with_invalid_pagination(client, auth_headers):
    response = client.get(
        "/api/v1/medicines?page=0&per_page=-5",
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 400