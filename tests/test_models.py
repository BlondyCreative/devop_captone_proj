from service import app
from service.models import Account


def test_create_account():
    with app.app_context():
        account = Account(name="Test", email="test@example.com")
        account.create()
        assert account.id is not None


def test_read_account():
    with app.app_context():
        account = Account(name="Test", email="test@example.com")
        account.create()
        found = Account.find(account.id)
        assert found.id == account.id


def test_update_account():
    with app.app_context():
        account = Account(name="Test", email="test@example.com")
        account.create()
        account.name = "Updated"
        account.update()
        updated = Account.find(account.id)
        assert updated.name == "Updated"


def test_delete_account():
    with app.app_context():
        account = Account(name="Test", email="test@example.com")
        account.create()
        account.delete()
        assert Account.find(account.id) is None
