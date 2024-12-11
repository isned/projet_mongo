import unittest
from unittest.mock import patch
from app import app  
from models import abonne

class TestAbonneRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('models.abonne.get_abonnes')
    def test_abonnes_lister(self, mock_get_abonnes):
        mock_get_abonnes.return_value = [
            {'nom': 'Dupont', 'prenom': 'Jean', 'adresse': '123 Rue A', 'date_inscription': '2024-01-01'}
        ]
        response = self.app.get('/abonnes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dupont', response.data)
        self.assertIn(b'Jean', response.data)

    @patch('models.abonne.get_abonne_by_id')
    def test_show_abonne_details_found(self, mock_get_abonne_by_id):
        mock_get_abonne_by_id.return_value = {'nom': 'Dupont', 'prenom': 'Jean'}
        response = self.app.get('/abonnes/1/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dupont', response.data)

    @patch('models.abonne.get_abonne_by_id')
    def test_show_abonne_details_not_found(self, mock_get_abonne_by_id):
        mock_get_abonne_by_id.return_value = None
        response = self.app.get('/abonnes/99/')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Abonné non trouvé'.encode('utf-8'), response.data)

    @patch('models.abonne.get_abonne_by_id')
    def test_show_update_abonne_form_found(self, mock_get_abonne_by_id):
        mock_get_abonne_by_id.return_value = {'nom': 'Dupont', 'prenom': 'Jean'}
        response = self.app.get('/abonnes/1/update')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dupont', response.data)

    @patch('models.abonne.get_abonne_by_id')
    def test_show_update_abonne_form_not_found(self, mock_get_abonne_by_id):
        mock_get_abonne_by_id.return_value = None
        response = self.app.get('/abonnes/99/update')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Abonné non trouvé'.encode('utf-8'), response.data)

    @patch('models.abonne.update_abonne')
    def test_update_abonne(self, mock_update_abonne):
        mock_update_abonne.return_value = {'message': 'Abonné mis à jour'}
        data = {'nom': 'Dupont', 'prenom': 'Jean', 'adresse': '123 Rue A'}
        response = self.app.post('/abonnes/1/update', data=data)
        self.assertEqual(response.status_code, 302)  

    @patch('models.abonne.delete_abonne')
    def test_delete_abonne(self, mock_delete_abonne):
        mock_delete_abonne.return_value = {'message': 'Abonné supprimé'}
        response = self.app.get('/abonnes/1/delete')
        self.assertEqual(response.status_code, 302)  

    @patch('models.abonne.add_abonne')
    def test_add_abonne(self, mock_add_abonne):
        mock_add_abonne.return_value = {'message': 'Abonné ajouté'}
        data = {
            'nom': 'Dupont',
            'prenom': 'Jean',
            'adresse': '123 Rue A',
            'date_inscription': '2024-01-01'
        }
        response = self.app.post('/add_abonne', data=data)
        self.assertEqual(response.status_code, 302)  

    


if __name__ == '__main__':
    unittest.main()
