def test_not_found_returns_json(client):
    response = client.get("/this-route-does-not-exist")

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 404

    data = response.get_json()

    assert data["message"] == (
        "The requested URL was not found on the server. "
        "If you entered the URL manually please check your spelling "
        "and try again."
    )


def test_method_not_allowed_returns_json(client):
    response = client.post("/health")

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.get_json())

    assert response.status_code == 405

    data = response.get_json()

    assert data["message"] == (
        "The method is not allowed for the requested URL."
    )