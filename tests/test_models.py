import unittest
from app import app, db
from models import Juego, User


class TestGameVaultModels(unittest.TestCase):

    def setUp(self):
        """Configura una base de datos en memoria para pruebas aisladas."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Limpia la base de datos y el contexto al terminar cada prueba."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_juego_record(self):
        """Verifica que se pueda instanciar y guardar un registro en Juego."""
        item = Juego(nombre="Elden Ring", descripcion="RPG de acción", precio=59.99)
        db.session.add(item)
        db.session.commit()

        saved_item = Juego.query.filter_by(nombre="Elden Ring").first()
        self.assertIsNotNone(saved_item)
        self.assertEqual(saved_item.descripcion, "RPG de acción")
        self.assertAlmostEqual(saved_item.precio, 59.99)

    def test_create_user_and_password(self):
        """Verifica la creación de usuario y el hash de contraseña."""
        user = User(username="marcos", email="marcos@example.com", password="secret")
        db.session.add(user)
        db.session.commit()

        saved_user = User.query.filter_by(username="marcos").first()
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.email, "marcos@example.com")
        self.assertTrue(saved_user.verify_password("secret"))
        self.assertFalse(saved_user.verify_password("incorrecta"))


if __name__ == '__main__':
    unittest.main()
