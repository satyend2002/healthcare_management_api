import uuid
import pytest
# he unauthorized GET test:...................
def test_get_appointments_without_authentication(client):
    response = client.get("/api/v1/appointments")

    assert response.status_code == 401
    
    

# Test authenticated GET appointments ...............
def test_get_appointments_with_authentication(client, auth_headers):
    response = client.get(
        "/api/v1/appointments",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.get_json()

    assert response_data is not None
    

# Test getting an appointment by ID .....
def test_get_appointment_by_id(client, auth_headers):
    response = client.get(
        "/api/v1/appointments/1",
        headers=auth_headers
    )

    assert response.status_code == 200

    response_data = response.get_json()

    assert response_data is not None
    assert response_data["id"] == 1
    


# Test getting a non-existent appointment ..........................
def test_get_nonexistent_appointment(client, auth_headers):
    response = client.get(
        "/api/v1/appointments/999999",
        headers=auth_headers
    )

    assert response.status_code == 404
    
    
    
# Test creating an appointment .....
def test_create_appointment(client, auth_headers):
    unique_id = uuid.uuid4().hex[:8]
    unique_phone = str(9000000000 + int(unique_id, 16) % 1000000000)

    patient_response = client.post(
        "/api/v1/patients",
        headers=auth_headers,
        json={
            "first_name": f"Appointment{unique_id}",
            "last_name": "Patient",
            "phone": unique_phone,
            "email": f"appointment_patient_{unique_id}@example.com",
            "gender": "Male",
            "date_of_birth": "1995-01-01"
        }
    )

    print("PATIENT STATUS:", patient_response.status_code)
    print("PATIENT RESPONSE:", patient_response.get_json())

    assert patient_response.status_code in [200, 201]


    patient_data = patient_response.get_json()
    patient_id = patient_data["data"]["id"]

    response = client.post(
        "/api/v1/appointments",
        headers=auth_headers,
        json={
            "patient_id": patient_id,
            "doctor_id": 1,
            "appointment_date": "2026-09-20",
            "appointment_time": "10:00:00",
            "reason": "Regular consultation"
        }
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code in [200, 201]

    response_data = response.get_json()

    assert response_data is not None 
    
    
# Test updating an appointment ................
def test_update_appointment(client, auth_headers):
    unique_id = uuid.uuid4().hex[:8]
    unique_phone = str(9000000000 + int(unique_id, 16) % 1000000000)

    patient_response = client.post(
        "/api/v1/patients",
        headers=auth_headers,
        json={
            "first_name": f"Update{unique_id}",
            "last_name": "Patient",
            "phone": unique_phone,
            "email": f"update_patient_{unique_id}@example.com",
            "gender": "Male",
            "date_of_birth": "1995-01-01"
        }
    )

    assert patient_response.status_code in [200, 201]

    patient_id = patient_response.get_json()["data"]["id"]

    appointment_response = client.post(
        "/api/v1/appointments",
        headers=auth_headers,
        json={
            "patient_id": patient_id,
            "doctor_id": 1,
            "appointment_date": "2026-09-20",
            "appointment_time": "10:00:00",
            "reason": "Initial consultation"
        }
    )

    assert appointment_response.status_code in [200, 201]

    appointment_data = appointment_response.get_json()
    appointment_id = (
        appointment_data.get("id")
        or appointment_data.get("data", {}).get("id")
    )

    update_response = client.put(
        f"/api/v1/appointments/{appointment_id}",
        headers=auth_headers,
        json={
            "appointment_date": "2026-09-21",
            "appointment_time": "11:00:00",
            "reason": "Follow-up consultation"
        }
    )

    print("UPDATE STATUS:", update_response.status_code)
    print("UPDATE RESPONSE:", update_response.get_json())

    assert update_response.status_code == 200 
    
    
    
# add the delete appointment test....................
def test_delete_appointment(client, auth_headers):
    unique_id = uuid.uuid4().hex[:8]
    unique_phone = str(9000000000 + int(unique_id, 16) % 1000000000)

    patient_response = client.post(
        "/api/v1/patients",
        headers=auth_headers,
        json={
            "first_name": f"Delete{unique_id}",
            "last_name": "Patient",
            "phone": unique_phone,
            "email": f"delete_patient_{unique_id}@example.com",
            "gender": "Male",
            "date_of_birth": "1995-01-01"
        }
    )

    assert patient_response.status_code in [200, 201]

    patient_id = patient_response.get_json()["data"]["id"]

    appointment_response = client.post(
        "/api/v1/appointments",
        headers=auth_headers,
        json={
            "patient_id": patient_id,
            "doctor_id": 1,
            "appointment_date": "2026-09-20",
            "appointment_time": "10:00:00",
            "reason": "Appointment to be deleted"
        }
    )

    assert appointment_response.status_code in [200, 201]

    appointment_data = appointment_response.get_json()
    appointment_id = (
        appointment_data.get("id")
        or appointment_data.get("data", {}).get("id")
    )

    delete_response = client.delete(
        f"/api/v1/appointments/{appointment_id}",
        headers=auth_headers
    )

    print("DELETE STATUS:", delete_response.status_code)
    print("DELETE RESPONSE:", delete_response.get_json())

    assert delete_response.status_code in [200, 204]