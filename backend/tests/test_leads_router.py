"""Lead router tests."""

CSV_HEADER = (
    "business_name,category,city,state,phone,website,rating,review_count,"
    "address,source_url\n"
)


def test_lead_import_route_accepts_csv_upload(client) -> None:
    csv_content = (
        CSV_HEADER
        + "Healthy Smile Clinic,Dentist,Ranchi,Jharkhand,+91 98765 43210,"
        "https://example.com,4.6,150,Main Road,source\n"
    )

    response = client.post(
        "/leads/import",
        files={"file": ("leads.csv", csv_content, "text/csv")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["summary"]["total_rows"] == 1
    assert payload["summary"]["valid_rows"] == 1
    assert payload["summary"]["invalid_rows"] == 0
    assert payload["valid_rows"][0]["business_name"] == "Healthy Smile Clinic"
    assert payload["imported_ids"]


def test_lead_import_route_returns_partial_import_result(client) -> None:
    csv_content = (
        CSV_HEADER
        + "Healthy Smile Clinic,Dentist,Ranchi,Jharkhand,+91 98765 43210,"
        "https://example.com,4.6,150,Main Road,source\n"
        "Broken Clinic,Dentist,Ranchi,Jharkhand,+91,example.com,4.6,150,"
        "Main Road,source\n"
    )

    response = client.post(
        "/leads/import",
        files={"file": ("leads.csv", csv_content, "text/csv")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["summary"]["total_rows"] == 2
    assert payload["summary"]["valid_rows"] == 1
    assert payload["summary"]["invalid_rows"] == 1
    assert payload["invalid_rows"][0]["row_number"] == 3
    assert (
        "website must start with http:// or https://"
        in payload["invalid_rows"][0]["reasons"]
    )


def test_lead_import_route_rejects_non_csv_upload(client) -> None:
    response = client.post(
        "/leads/import",
        files={"file": ("leads.txt", "not csv", "text/plain")},
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Uploaded lead import file must use a .csv filename."
    )


def test_lead_import_route_rejects_invalid_json_payload(client) -> None:
    response = client.post("/leads/import", json={"csv_content": ""})
    assert response.status_code == 422


def test_lead_import_route_does_not_break_health_route(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "leados-api"}
