import unittest
from flask import Flask
from app import db  # Importez seulement les parties nécessaires de votre application

# Créez une application Flask pour les tests
app = Flask(__name__)
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Utilisez une base de données en mémoire pour les tests
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Importez les routes que vous souhaitez tester après avoir initialisé l'application Flask
from app import routes

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_offers_route(self):
        response = self.app.get('/offers')
        self.assertEqual(response.status_code, 200)

    def test_update_cart_route(self):
        response = self.app.post('/update_cart', json={'action': 'add', 'offer_type': 'solo'})
        self.assertEqual(response.status_code, 200)

    def test_register_route(self):
        response = self.app.post('/register', data={'nom': 'Zola', 'prenom': 'randy', 'email': 'zola.ridy@example.com', 'password': 'password', 'selected_offer': 'solo'})
        self.assertEqual(response.status_code, 302)  # Redirection après l'inscription

    def test_login_route(self):
        response = self.app.post('/login', data={'username': 'ridy', 'password': 'Zola2024@'})
        self.assertEqual(response.status_code, 302)  # Redirection après la connexion réussie

    def test_payment_route(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 'ridy'  # Simuler la connexion de l'utilisateur
        response = self.app.get('/payment')
        self.assertEqual(response.status_code, 200)

    # Ajoutez des méthodes de test pour d'autres routes de votre application

if __name__ == '__main__':
    unittest.main()
