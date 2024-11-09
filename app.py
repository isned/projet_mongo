from flask import Flask, redirect, render_template, request, jsonify
from flask_pymongo import PyMongo
from config import Config
from models import abonne
from models import document
from models import emprunt
from datetime import datetime

from datetime import datetime
from bson import ObjectId
from flask import request, redirect, render_template, jsonify

app = Flask(__name__)  # Corrigé name en _name_
app.config.from_object(Config)

mongo = PyMongo(app)




# Route principale
@app.route('/')
def home():
    return render_template('index.html')





# Route pour lister les abonnés
@app.route('/abonnes', methods=['GET'])
def abonnes_lister():
    abonnes = abonne.get_abonnes(mongo)  # Récupère tous les documents
    return render_template('abonnes/lister.html', abonnes=abonnes)

# Route pour récupérer un abonné par ID
@app.route('/abonnes/<id>/', methods=['GET'])
def show_abonne_details(id):
    ab = abonne.get_abonne_by_id(id, mongo)
    if ab:
        return render_template('abonnes/details.html', abonne=ab)
    else:
        return "Abonné non trouvé", 404

# Route pour afficher la page de modification
@app.route('/abonnes/<id>/update', methods=['GET'])
def show_update_abonne_form(id):
    abonne_to_update = abonne.get_abonne_by_id(id, mongo)
    if abonne_to_update:
        return render_template('abonnes/modifier.html', abonne=abonne_to_update)
    else:
        return "Abonné non trouvé", 404

# Route pour mettre à jour un abonné
@app.route('/abonnes/<id>/update', methods=['POST'])
def update_abonne(id):
    data = request.form
    if not data:
        return "Aucune donnée fournie", 400
    result = abonne.update_abonne(id, data, mongo)
    return redirect('/abonnes')

# Route pour supprimer un abonné
@app.route('/abonnes/<id>/delete', methods=['GET'])
def delete_abonne_route(id):
    result = abonne.delete_abonne(id, mongo)
    if 'message' in result:
        return redirect('/abonnes')
    else:
        return "Erreur lors de la suppression", 404

# Route pour ajouter un abonné
@app.route('/add_abonne', methods=['GET'])
def show_add_abonne_form():
    return render_template('abonnes/ajouter.html')

@app.route('/add_abonne', methods=['POST'])
def add_abonne_route():
    nom = request.form['nom']
    prenom = request.form['prenom']
    adresse = request.form['adresse']
    date_inscription = request.form['date_inscription']
    
    data = {
        'nom': nom,
        'prenom': prenom,
        'adresse': adresse,
        'date_inscription': date_inscription,
    }
    
    result = abonne.add_abonne(data, mongo)
    return redirect('/abonnes')




















# Afficher le formulaire d'ajout de document
@app.route('/add_document', methods=['GET'])
def show_add_document_form():
    return render_template('documents/ajouter.html')

# Ajouter un document via POST
@app.route('/add_document', methods=['POST'])
def add_document_route():
    # Récupérer les données du formulaire via request.form
    titre = request.form['titre']
    auteur = request.form['auteur']
    genre = request.form['genre']
    date_publication = request.form['date_publication']
    disponibilite = request.form['disponibilite']
    
    # Préparer les données du document
    data = {
        'titre': titre,
        'auteur': auteur,
        'genre': genre,
        'date_publication': date_publication,
        'disponibilite': disponibilite
    }
    
    # Ajouter le document à la base de données
    result = document.add_document(data, mongo)
    
    # Rediriger vers la page de liste des documents après ajout
    return redirect('/documents')

@app.route('/documents', methods=['GET'])
def documents_lister():
    documents = document.get_documents(mongo)  # Récupère tous les documents
    return render_template('documents/lister.html', documents=documents)




# Route pour récupérer un document par ID
@app.route('/documents/<id>/', methods=['GET'])
def show_document_details(id):
    # Appeler la fonction du module 'document' pour récupérer un document
    doc = document.get_document_by_id(id, mongo)  # Renommer la variable pour éviter le conflit
    if doc:
        return render_template('documents/details.html', document=doc)  # Afficher la page de détails
    else:
        return "Document non trouvé", 404  # Si le document n'est pas trouvé

# Route pour afficher la page de modification
@app.route('/documents/<id>/update', methods=['GET'])
def show_update_form(id):
    # Récupérer le document à partir de la base de données
    document_to_update = document.get_document_by_id(id,mongo)
    if document_to_update:
        return render_template('documents/modifier.html', document=document_to_update)
    else:
        return "Document non trouvé", 404

# Route pour mettre à jour le document
@app.route('/documents/<id>/update', methods=['POST'])
def update_document(id):
    data = request.form  # Récupérer les données envoyées via le formulaire

    # Vérification si les données sont présentes
    if not data:
        return "Aucune donnée fournie", 400

    # Mettre à jour le document avec les nouvelles données
    result = document.update_document(id, data, mongo)

    return redirect('/documents')  # Rediriger vers la liste des documents après modification


@app.route('/documents/<id>/', methods=['PUT'])
def update_document_route(id):
    data = document.get_document_by_id(id, mongo)
    if data:
        return render_template('documents/update.html', document=data)
    return jsonify({"message": "Document non trouvé"}), 404


@app.route('/documents/<id>/delete', methods=['GET'])
def delete_document_route(id):
    try:
        # Appel à la fonction delete_document dans document.py
        result = document.delete_document(id, mongo)

        # Vérifie si la suppression a réussi
        if 'message' in result:
            return redirect('/documents')  # Redirige vers la liste des documents après la suppression
        else:
            return "Erreur lors de la suppression du document", 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/emprunts', methods=['GET'])
def emprunts_lister():
    emprunts = emprunt.get_emprunts(mongo)  # Récupère tous les documents
    return render_template('emprunts/lister.html', emprunts=emprunts)

# Route pour récupérer un abonné par ID
@app.route('/empruntss/<id>/', methods=['GET'])
def show_emprunt_details(id):
    em = emprunt.get_emprunt_by_id(id, mongo)
    if em:
        return render_template('emprunts/details.html', emprunt=em)
    else:
        return "Emprunt non trouvé", 404

# Route pour afficher la page de modification
@app.route('/emprunts/<id>/update', methods=['GET'])
def show_update_emprunt_form(id):
    emprunt_to_update = emprunt.get_emprunt_by_id(id, mongo)
    if emprunt_to_update:
        return render_template('emprunts/modifier.html', emprunt=emprunt_to_update)
    else:
        return "Emprunt non trouvé", 404

# Route pour mettre à jour un abonné
@app.route('/emprunts/<id>/update', methods=['POST'])
def update_emprunt(id):
    data = request.form
    if not data:
        return "Aucune donnée fournie", 400
    result = emprunt.update_emprunt(id, data, mongo)
    return redirect('/emprunts')

# Route pour supprimer un abonné
@app.route('/emprunts/<id>/delete', methods=['GET'])
def delete_emprunt_route(id):
    result = emprunt.delete_emprunt(id, mongo)
    if 'message' in result:
        return redirect('/emprunts')
    else:
        return "Erreur lors de la suppression", 404



# Afficher le formulaire d'ajout de document
@app.route('/add_emprunt', methods=['GET'])
def show_add_emprunt_form():
    return render_template('emprunts/ajouter.html')


@app.route('/add_emprunt', methods=['POST'])
def add_emprunt_route():
    # Récupérer les données du formulaire via request.form
        abonne_id = request.form['abonne_id']
        document_id = request.form['document_id']
        date_retour_prevu = request.form['date_retour_prevu']
        date_emprunt = datetime.now()
        # Convertir la date de retour prévue en objet datetime
        date_retour_prevu = datetime.strptime(date_retour_prevu, '%Y-%m-%d')

        # Vérifier si la date de retour est antérieure à la date d'emprunt
        if date_retour_prevu < date_emprunt:
            return "La date de retour ne peut pas être antérieure à la date d'emprunt", 400
        data = {
            'abonne_id': abonne_id,
            'document_id': document_id,
            'date_emprunt': date_emprunt,
            'date_retour_prevu': date_retour_prevu,
            'statut': 'emprunté'
        }
    
    # Ajouter le document à la base de données
        result = emprunt.add_emprunt(data, mongo)
    
    # Rediriger vers la page de liste des documents après ajout
        return redirect('/emprunts')












if __name__ == '__main__':  # Corrigé name en _name_
    print("Démarrage de l'application Flask sur le port 5000")
    app.run(debug=True, port=5000)