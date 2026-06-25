
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