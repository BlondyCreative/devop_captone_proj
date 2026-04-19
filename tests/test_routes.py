import unittest
from service.routes import app
from service.common import status

class TestAccountService(unittest.TestCase):
    """Pruebas para el Microservicio de Cuentas"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        self.client = app.test_client()

    def test_index(self):
        """Debe retornar la página de inicio correctamente"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_account_list(self):
        """Debe retornar una lista de cuentas"""
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
