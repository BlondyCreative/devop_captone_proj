from service import app
from service.models import Account
from service.common import status

def test_index_route():
    """Prueba la ruta raíz /"""
    with app.app_context():
        client = app.test_client()
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert b"Account RESTful Service" in response.data


def test_list_accounts():
    """Prueba GET /accounts"""
    with app.app_context():
        client = app.test_client()
        response = client.get("/accounts")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json, list)


def test_get_account():
    """Prueba GET /accounts/<id>"""
    with app.app_context():
        # Crear cuenta temporal
        account = Account(name="Test User", email="test@example.com")
        account.create()

        client = app.test_client()
        response = client.get(f"/accounts/{account.id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json["name"] == "Test User"


def test_get_account_not_found():
    """Prueba GET /accounts/<id> con ID inexistente"""
    with app.app_context():
        client = app.test_client()
        response = client.get("/accounts/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND