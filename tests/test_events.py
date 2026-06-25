
def test_list_events_returns_all_events(client):
    response = client.get("/api/events")
    assert response.status_code == 200
    assert len(response.json()["events"]) == 10

def test_list_events_returns_correct_shape(client):
    response = client.get("/api/events")
    event = response.json()["events"][0]
    assert event.keys() == {
        "id", "title", "starts_at", "ends_at", "location"
    }

def test_list_events_location_format_is_correct(client):
    expected_location = "The Skiff, 30 Cheapside, Brighton, BN1 4GD"
    response = client.get("/api/events")
    event = next(filter(lambda l: l["title"] == "Brighton Python Meetup", response.json()["events"]))
    assert event["location"] == expected_location

def test_list_events_ordered_by_start_date(client):
    response = client.get("/api/events")
    dates = [event["starts_at"] for event in response.json()["events"]]
    assert dates == sorted(dates)

def test_events_by_id_returns_200_for_valid_id(client):
    response = client.get("/api/events/1")
    assert response.status_code == 200

def test_events_by_id_returns_correct_shape(client):
    response = client.get("/api/events/1")
    event = response.json()["events"][0]
    assert event.keys() == {
        "id",
        "title",
        "description",
        "starts_at",
        "ends_at"
        "location",
        "address",
        "capacity",
        "created_at"
    }

def test_events_by_id_returns_404_for_invalid_eventt(client):
    response = client.get("/api/events/9999")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"