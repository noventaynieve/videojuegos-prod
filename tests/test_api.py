import unittest
import json
from app import app, db
from models import Juego


class TestGameVaultAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_api_get_juegos(self):
        """Verifica que el endpoint GET /api/juegos devuelva una lista JSON válida."""
        response = self.client.get('/api/juegos')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_api_post_juegos(self):
        """Verifica la inserción de registros a través de POST /api/juegos."""
        payload = {
            "nombre": "Hades II",
            "descripcion": "Roguelike de acción",
            "precio": 29.99
        }
        response = self.client.post(
            '/api/juegos',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 201])

        item = Juego.query.filter_by(nombre="Hades II").first()
        self.assertIsNotNone(item)
        self.assertEqual(item.descripcion, "Roguelike de acción")
        self.assertAlmostEqual(item.precio, 29.99)


if __name__ == '__main__':
    unittest.main()
