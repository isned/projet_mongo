from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from config import Config
from models import abonne
from models import document
from models import emprunt



app = Flask(__name__)  # Corrigé name en _name_
app.config.from_object(Config)

mongo = PyMongo(app)




# Route principale
@app.route('/')
def home():
    return "Bienvenue dans la médiathèque !"




@app.route('/add_abonne', methods=['POST'])
def ajouter_abonne():
    data = request.get_json()  # Récupérer les données envoyées par le client
    result = abonne.add_abonne(data,mongo)
    return jsonify(result)


# READ - Récupérer tous les abonnés
@app.route('/abonnes', methods=['GET'])
def get_all_abonnes():
    abonnes = abonne.get_abonnes(mongo)
    return jsonify(abonnes)

# READ - Récupérer un abonné par son ID
@app.route('/abonnes/<string:id>', methods=['GET'])
def get_abonne(id):
    abonne = abonne.get_abonne_by_id(id,mongo)
    if abonne:
        return jsonify(abonne)
    return jsonify({"message": "Abonné non trouvé"}), 404

# UPDATE - Mettre à jour un abonné
@app.route('/abonnes/<string:id>', methods=['PUT'])
def update_abonne_route(id):
    data = request.get_json()  # Données pour mettre à jour
    result = abonne.update_abonne(id, data,mongo)
    return jsonify(result)

# DELETE - Supprimer un abonné
@app.route('/abonnes/<string:id>', methods=['DELETE'])
def delete_abonne_route(id):
    result = abonne.delete_abonne(id,mongo)
    return jsonify(result)


# Route pour ajouter un document
@app.route('/add_document', methods=['POST'])
def add_document_route():
    data = request.get_json()
    result = document.add_document(data, mongo)
    return jsonify(result)

# Route pour récupérer tous les documents
@app.route('/documents', methods=['GET'])
def get_documents_route():
    documents = document.get_documents(mongo)
    return jsonify(documents)

# Route pour récupérer un document par ID
@app.route('/documents/<id>', methods=['GET'])
def get_document_by_id_route(id):
    document = document.get_document_by_id(id, mongo)
    if document:
        return jsonify(document)
    return jsonify({"message": "Document non trouvé"}), 404

# Route pour mettre à jour un document
@app.route('/documents/<id>', methods=['PUT'])
def update_document_route(id):
    data = request.get_json()
    result = document.update_document(id, data, mongo)
    return jsonify(result)

# Route pour supprimer un document
@app.route('/documents/<id>', methods=['DELETE'])
def delete_document_route(id):
    result = document.delete_document(id, mongo)
    return jsonify(result)



# Exemple d'utilisation dans une route
@app.route('/add_emprunt', methods=['POST'])
def add_emprunt_route():
    data = request.get_json()  # Récupérer les données envoyées en JSON
    return emprunt.add_emprunt(data, mongo)

@app.route('/emprunts', methods=['GET'])
def get_all_emprunts():
    return jsonify(emprunt.get_emprunts(mongo))

@app.route('/emprunts/<id>', methods=['GET'])
def get_emprunt(id):
    emprunt = emprunt.get_emprunt_by_id(id, mongo)
    if emprunt:
        return jsonify(emprunt)
    return jsonify({"message": "Emprunt non trouvé"}), 404

@app.route('/emprunts/<id>', methods=['PUT'])
def update_emprunt_route(id):
    data = request.get_json()
    return emprunt.update_emprunt(id, data, mongo)

@app.route('/emprunts/<id>', methods=['DELETE'])
def delete_emprunt_route(id):
    return emprunt.delete_emprunt(id, mongo)
if __name__ == '__main__':  # Corrigé name en _name_
    print("Démarrage de l'application Flask sur le port 5000")
    app.run(debug=True, port=5000)