from service import app
from service.models import Account

def test_create_account():
    """Prueba crear una cuenta"""
    with app.app_context():
        account = Account(name="Test Create", email="create@example.com")
        account.create()
        assert account.id is not None


def test_read_account():
    """Prueba leer una cuenta"""
    with app.app_context():
        account = Account(name="Test Read", email="read@example.com")
        account.create()

        found = Account.find(account.id)
        assert found is not None
        assert found.name == "Test Read"


def test_update_account():
    """Prueba actualizar una cuenta"""
    with app.app_context():
        account = Account(name="Old Name", email="old@example.com")
        account.create()

        account.name = "New Name"
        account.update()

        updated = Account.find(account.id)
        assert updated.name == "New Name"


def test_delete_account():
    """Prueba eliminar una cuenta"""
    with app.app_context():
        account = Account(name="Delete Me", email="delete@example.com")
        account.create()

        account.delete()
        deleted = Account.find(account.id)
        assert deleted is None