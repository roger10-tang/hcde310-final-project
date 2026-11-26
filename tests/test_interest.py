import json

from app import create_app


def form_token(client):
    client.get("/")
    with client.session_transaction() as browser:
        return browser["formToken"]


def add_post(client):
    response = client.post("/posts", data={"course": "Test course", "date": "2099-01-01",
                                          "time": "10:00", "formToken": form_token(client)})
    assert response.status_code == 303
    return next(iter(client.get("/counts").get_json()))


def test_interest_survives_a_new_app_and_keeps_session(tmp_path):
    app = create_app(tmp_path)
    client = app.test_client()
    post_id = add_post(client)
    response = client.post(f"/posts/{post_id}/interest", data={"formToken": form_token(client)}, follow_redirects=True)
    assert b"Interest saved." in response.data
    assert b"Remove interest" in response.data
    records = json.loads((tmp_path / "interests.json").read_text())
    assert set(records[0]) == {"interestId", "postId", "studentId"}
    restarted = create_app(tmp_path).test_client()
    restarted.set_cookie("session", client.get_cookie("session").value)
    assert restarted.get("/counts").get_json()[post_id] == {"count": 1, "interested": True}


def test_two_browsers_share_count_but_keep_separate_interests(tmp_path):
    app = create_app(tmp_path, "test-key")
    first, second = app.test_client(), app.test_client()
    post_id = add_post(first)
    first.post(f"/posts/{post_id}/interest", data={"formToken": form_token(first)})
    assert second.get("/counts").get_json()[post_id] == {"count": 1, "interested": False}
    second.post(f"/posts/{post_id}/interest", data={"formToken": form_token(second)})
    assert first.get("/counts").get_json()[post_id]["count"] == 2
    first.post(f"/posts/{post_id}/interest", data={"formToken": form_token(first)})
    assert second.get("/counts").get_json()[post_id] == {"count": 1, "interested": True}


def test_missing_file_and_unknown_post(tmp_path):
    client = create_app(tmp_path, "test-key").test_client()
    assert b"No tee times posted yet" in client.get("/").data
    assert client.get("/counts").get_json() == {}
    response = client.post("/posts/missing/interest", data={"formToken": form_token(client)})
    assert response.status_code == 404
    assert not (tmp_path / "interests.json").exists()


def test_corrupt_json_is_not_overwritten(tmp_path):
    client = create_app(tmp_path, "test-key").test_client()
    post_id = add_post(client)
    token = form_token(client)
    (tmp_path / "interests.json").write_text("broken data")
    response = client.post(f"/posts/{post_id}/interest", data={"formToken": token})
    assert response.status_code == 503
    assert (tmp_path / "interests.json").read_text() == "broken data"


def test_bad_post_input_and_duplicate(tmp_path):
    client = create_app(tmp_path, "test-key").test_client()
    token = form_token(client)
    assert client.post("/posts", data={"formToken": token}).status_code == 400
    assert client.post("/posts", data={"course": "Test", "date": "2000-01-01", "time": "10:00", "formToken": token}).status_code == 400
    add_post(client)
    assert client.post("/posts", data={"course": "Test course", "date": "2099-01-01", "time": "10:00", "formToken": token}).status_code == 409


def test_missing_form_token_cannot_change_data(tmp_path):
    client = create_app(tmp_path, "test-key").test_client()
    post_id = add_post(client)
    assert client.post(f"/posts/{post_id}/interest").status_code == 400
    assert client.get("/counts").get_json()[post_id]["count"] == 0
