from src.app import activities


ACTIVITY = "Chess Club"
NEW_EMAIL = "newstudent@mergington.edu"


def test_root_redirects_to_static_page(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_catalog(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert ACTIVITY in response.json()
    assert isinstance(response.json()[ACTIVITY]["participants"], list)


def test_signup_adds_participant(client):
    response = client.post(
        f"/activities/{ACTIVITY}/signup",
        params={"email": NEW_EMAIL},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {NEW_EMAIL} for {ACTIVITY}"
    }
    assert NEW_EMAIL in activities[ACTIVITY]["participants"]


def test_signup_rejects_duplicate_participant(client):
    existing_email = activities[ACTIVITY]["participants"][0]

    response = client.post(
        f"/activities/{ACTIVITY}/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student is already signed up for this activity"
    }


def test_signup_rejects_unknown_activity(client):
    response = client.post(
        "/activities/Unknown Activity/signup",
        params={"email": NEW_EMAIL},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_removes_participant(client):
    existing_email = activities[ACTIVITY]["participants"][0]

    response = client.delete(
        f"/activities/{ACTIVITY}/participants/{existing_email}"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {existing_email} from {ACTIVITY}"
    }
    assert existing_email not in activities[ACTIVITY]["participants"]


def test_unregister_rejects_missing_participant(client):
    response = client.delete(
        f"/activities/{ACTIVITY}/participants/{NEW_EMAIL}"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }


def test_unregister_rejects_unknown_activity(client):
    response = client.delete(
        f"/activities/Unknown Activity/participants/{NEW_EMAIL}"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
