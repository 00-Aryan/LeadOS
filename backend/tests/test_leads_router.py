"""Lead router tests."""


def test_lead_import_route_persists_valid_lead(client) -> None:
    csv_content = (
        "business_name,category,city,state,phone,website,rating,review_count,address,source_url\n"
        "Healthy Smile Clinic,Dentist,Ranchi,Jharkhand,+91 98765 43210,https://example.com,4.6,150,Main Road,source\n"
    )

    response = client.post("/leads/import", json={"csv_content": csv_content, "source_name": "test.csv"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["valid_records"] == 1
    assert payload["imported_ids"]

    list_response = client.get("/leads")
    assert list_response.status_code == 200
    assert list_response.json()[0]["business_name"] == "Healthy Smile Clinic"


def test_lead_import_route_rejects_invalid_payload(client) -> None:
    response = client.post("/leads/import", json={"csv_content": ""})
    assert response.status_code == 422
