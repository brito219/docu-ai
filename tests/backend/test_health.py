from conftest import create_test_client


def test_health_check_returns_ok(tmp_path) -> None:
    with create_test_client(tmp_path) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["environment"] == "test"
