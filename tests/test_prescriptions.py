## create test patient ......
import uuid


def create_test_patient(client, auth_headers):
    unique_id = uuid.uuid4().hex[:8]
    unique_phone = str(
        9000000000 + int(unique_id, 16) % 1000000000
    )

    response = client.post(
        "/api/v1/patients",
        headers=auth_headers,
        json={
            "first_name": f"Prescription{unique_id}",
            "last_name": "Patient",
            "phone": unique_phone,
            "email": f"prescription_{unique_id}@example.com",
            "gender": "Male",
            "date_of_birth": "1995-01-01"
        }
    )

    assert response.status_code in [200, 201]

    return response.get_json()["data"]["id"]


def create_test_appointment(client, auth_headers, patient_id):
    response = client.post(
        "/api/v1/appointments",
        headers=auth_headers,
        json={
            "patient_id": patient_id,
            "doctor_id": 1,
            "appointment_date": "2026-09-25",
            "appointment_time": "10:30:00",
            "reason": "Prescription consultation"
        }
    )

    assert response.status_code in [200, 201]

    appointment_data = response.get_json()

    return (
        appointment_data.get("id")
        or appointment_data.get("data", {}).get("id")
    )


def test_get_prescriptions_without_authentication(client):
    response = client.get("/api/v1/prescriptions")

    assert response.status_code in [401, 403]


def test_get_prescriptions_with_authentication(client, auth_headers):
    response = client.get(
        "/api/v1/prescriptions",
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 200 
    

# Add the prescription creation test ....................
def test_create_prescription(client, auth_headers):
    patient_id = create_test_patient(client, auth_headers)

    appointment_id = create_test_appointment(
        client,
        auth_headers,
        patient_id
    )

    response = client.post(
        "/api/v1/prescriptions",
        headers=auth_headers,
        json={
            "patient_id": patient_id,
            "doctor_id": 1,
            "appointment_id": appointment_id,
            "medicine_name": "Paracetamol",
            "dosage": "650 mg",
            "frequency": "Three times daily",
            "duration": "7 days",
            "instructions": "Take after meals"
        }
    )

    print("CREATE STATUS:", response.status_code)
    print("CREATE RESPONSE:", response.get_json())

    assert response.status_code == 201, response.get_json()

    response_data = response.get_json()

    assert response_data["patient_id"] == patient_id
    assert response_data["doctor_id"] == 1
    assert response_data["appointment_id"] == appointment_id
    assert response_data["medicine_name"] == "Paracetamol"
    

# test getting a prescription by ID .......
def test_get_prescription_by_id(client, auth_headers):
    patient_id = create_test_patient(client, auth_headers)

    appointment_id = create_test_appointment(
        client,
        auth_headers,
        patient_id
    )

    create_response = client.post(
        "/api/v1/prescriptions",
        headers=auth_headers,
        json={
            "patient_id": patient_id,
            "doctor_id": 1,
            "appointment_id": appointment_id,
            "medicine_name": "Paracetamol",
            "dosage": "650 mg",
            "frequency": "Three times daily",
            "duration": "7 days",
            "instructions": "Take after meals"
        }
    )

    assert create_response.status_code == 201

    prescription_data = create_response.get_json()
    prescription_id = prescription_data["id"]

    response = client.get(
        f"/api/v1/prescriptions/{prescription_id}",
        headers=auth_headers
    )

    print("GET STATUS:", response.status_code)
    print("GET RESPONSE:", response.get_json())

    assert response.status_code == 200

    response_data = response.get_json()
    assert response_data["id"] == prescription_id
    assert response_data["medicine_name"] == "Paracetamol" 
    

# test a nonexistent prescription.............
def test_get_nonexistent_prescription(client, auth_headers):
    response = client.get(
        "/api/v1/prescriptions/999999",
        headers=auth_headers
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 404 
    
# test updating a prescription ........................
def test_update_prescription(client, auth_headers):
    patient_id = create_test_patient(client, auth_headers)

    appointment_id = create_test_appointment(
        client,
        auth_headers,
        patient_id
    )

    create_response = client.post(
        "/api/v1/prescriptions",
        headers=auth_headers,
        json={
            "patient_id": patient_id,
            "doctor_id": 1,
            "appointment_id": appointment_id,
            "medicine_name": "Paracetamol",
            "dosage": "650 mg",
            "frequency": "Three times daily",
            "duration": "7 days",
            "instructions": "Take after meals"
        }
    )

    assert create_response.status_code == 201

    prescription_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/api/v1/prescriptions/{prescription_id}",
        headers=auth_headers,
        json={
            "dosage": "500 mg",
            "duration": "5 days",
            "instructions": "Take before meals"
        }
    )

    print("UPDATE STATUS:", update_response.status_code)
    print("UPDATE RESPONSE:", update_response.get_json())

    assert update_response.status_code == 200

    response_data = update_response.get_json()

    assert response_data["message"] == "Prescription updated successfully"
    assert response_data["prescription"]["dosage"] == "500 mg"
    assert response_data["prescription"]["duration"] == "5 days"
    assert response_data["prescription"]["instructions"] == "Take before meals"
    
    
    # test delete prescription .....
def test_delete_prescription(client, auth_headers):
    patient_id = create_test_patient(client, auth_headers)

    appointment_id = create_test_appointment(
        client,
        auth_headers,
        patient_id
    )

    create_response = client.post(
        "/api/v1/prescriptions",
        headers=auth_headers,
        json={
            "patient_id": patient_id,
            "doctor_id": 1,
            "appointment_id": appointment_id,
            "medicine_name": "Paracetamol",
            "dosage": "650 mg",
            "frequency": "Three times daily",
            "duration": "7 days",
            "instructions": "Take after meals"
        }
    )

    assert create_response.status_code == 201

    prescription_id = create_response.get_json()["id"]

    delete_response = client.delete(
        f"/api/v1/prescriptions/{prescription_id}",
        headers=auth_headers
    )

    print("DELETE STATUS:", delete_response.status_code)
    print("DELETE RESPONSE:", delete_response.get_json())

    assert delete_response.status_code == 200

    response_data = delete_response.get_json()
    assert response_data["message"] == "Prescription deleted successfully"