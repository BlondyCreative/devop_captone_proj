from service import app
from service.models import Account


def test_index_route():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_list_accounts():
    with app.app_context():
        Account(name="Test", email="test@example.com").create()
        client = app.test_client()
        response = client.get("/account")
        assert response.status_code == 200


def test_get_account():
    with app.app_context():
        account = Account(name="Test", email="test@example.com")
        account.create()
        client = app.test_client()
        response = client.get(f"/account/{account.id}")
        assert response.status_code == 200


def test_get_account_not_found():
    client = app.test_client()
    response = client.get("/account/9999")
    assert response.status_code == 404
