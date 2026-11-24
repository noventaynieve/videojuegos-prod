import unittest
from app import app, db


class TestGameVaultRoutes(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_gamevault_home(self):
        """Verifica que la página principal de GameVault responda o redirija correctamente."""
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 302])

    def test_gamevault_home_follow_redirects(self):
        """Verifica que al seguir redirecciones desde '/' se obtenga una respuesta válida."""
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
