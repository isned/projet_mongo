from flask import Flask, redirect, render_template, request, jsonify, url_for
from flask_pymongo import PyMongo
from config import Config
from models import abonne, genre
from models import document
from models import emprunt
from datetime import datetime

from datetime import datetime
from bson import ObjectId
from flask import request, redirect, render_template, jsonify

app = Flask(__name__)  
app.config.from_object(Config)

mongo = PyMongo(app)




@app.route('/')
def home():
    # Récupérer tous les emprunts
    emprunts = emprunt.get_emprunts(mongo) 
    
    # Récupérer tous les abonnés et documents pour les lier aux emprunts
    abonnes = {str(abonne['_id']): abonne for abonne in mongo.db.abonnes.find()}
    documents = {str(document['_id']): document for document in mongo.db.documents.find()}
    genres = {str(genre['_id']): genre for genre in mongo.db.genres.find()}
    
    # Passer les emprunts et les informations supplémentaires au template
    return render_template('index.html', emprunts=emprunts, abonnes=abonnes, documents=documents,genres=genres)




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




















@app.route('/add_document', methods=['GET'])
def show_add_document_form():
    genres = list(mongo.db.genres.find())  # Récupère tous les genres
    print("Genres récupérés :", genres)   # Debug : Affiche les genres récupérés
    return render_template('documents/ajouter.html', genres=genres)


@app.route('/add_document', methods=['POST'])
def add_document_route():
    # Récupérer les données du formulaire via request.form
    titre = request.form['titre']
    auteur = request.form['auteur']
    genre_id = request.form['genre_id']  # Récupérer l'ID du genre
    date_publication = request.form['date_publication']
    disponibilite = request.form['disponibilite']
    
    # Préparer les données du document
    data = {
        'titre': titre,
        'auteur': auteur,
        'genre': genre_id,  # Assurez-vous d'utiliser l'ID du genre
        'date_publication': date_publication,
        'disponibilite': disponibilite
    }
    
    # Ajouter le document à la base de données
    result = document.add_document(data, mongo)
    
    # Rediriger vers la page de liste des documents après ajout
    return redirect('/documents')


@app.route('/documents', methods=['GET'])
def documents_lister():
    documents = document.get_documents(mongo) 
    genres = list(mongo.db.genres.find())  # Récupère tous les genres
   
    return render_template('documents/lister.html', documents=documents,genres=genres)




# Route pour récupérer un document par ID
@app.route('/documents/<id>/', methods=['GET'])
def show_document_details(id):
    # Appeler la fonction du module 'document' pour récupérer un document
    doc = document.get_document_by_id(id, mongo)  # Renommer la variable pour éviter le conflit
    if doc:
        return render_template('documents/details.html', document=doc)  # Afficher la page de détails
    else:
        return "Document non trouvé", 404  # Si le document n'est pas trouvé

@app.route('/documents/<id>/update', methods=['GET'])
def show_update_form(id):
    # Get the document by ID
    document_to_update = document.get_document_by_id(id, mongo)
    
    if document_to_update:
        # Get all genres
        genres = mongo.db.genres.find()
        return render_template('documents/modifier.html', document=document_to_update, genres=genres)
    else:
        return "Document non trouvé", 404



@app.route('/documents/<id>/update', methods=['POST'])
def update_document(id):
    data = request.form
    genre_id = ObjectId(data['genre'])  # Ensure the genre is passed as ObjectId
    
    # Check if the genre exists
    genre = mongo.db.genres.find_one({"_id": genre_id})
    if not genre:
        return "Genre non trouvé", 400

    updated_document = {
        "titre": data['titre'],
        "auteur": data['auteur'],
        "genre": genre_id,  # Correctly store the ObjectId
        "date_publication": data['date_publication'],
        "disponibilite": data['disponibilite']
    }

    # Update the document in the database
    mongo.db.documents.update_one({"_id": ObjectId(id)}, {"$set": updated_document})

    return redirect('/documents')  # Redirect to the documents list




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
@app.route('/emprunts/<id>/', methods=['GET'])
def show_emprunt_details(id):
    em = emprunt.get_emprunt_by_id(id, mongo)
    if em:
        return render_template('emprunts/details.html', emprunt=em)
    else:
        return "Emprunt non trouvé", 404



@app.route('/emprunts/<id>/update', methods=['GET'])
def show_update_emprunt_form(id):
    emprunt_to_update = emprunt.get_emprunt_by_id(id, mongo)
    if emprunt_to_update:
        abonnes = mongo.db.abonnes.find()
        documents = mongo.db.documents.find()
        date_retour_prevu = emprunt_to_update['date_retour_prevu'].strftime('%Y-%m-%d') if 'date_retour_prevu' in emprunt_to_update else ''
        
        return render_template('emprunts/modifier.html', 
                               emprunt=emprunt_to_update,
                               abonnes=abonnes,
                               documents=documents,
                               date_retour_prevu=date_retour_prevu)
    else:
        return "Emprunt non trouvé", 404




@app.route('/add_emprunt', methods=['GET'])
def show_add_emprunt_form():
    # Fetch all abonnes (members) and documents with "Disponible" status
    abonnes = list(mongo.db.abonnes.find())
    documents_disponibles = list(mongo.db.documents.find({"disponibilite": "Disponible"}))
    
    # Debugging: Print the fetched documents to check if they exist
    print("Documents disponibles:", documents_disponibles)
    
    # Get the current date in the format needed for the input field
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Render the form with available abonnes and documents
    return render_template('emprunts/ajouter.html', abonnes=abonnes, documents=documents_disponibles, current_date=current_date)




@app.route('/add_emprunt', methods=['POST'])
def add_emprunt_route():
    # Retrieve form data from the request
    abonne_id = request.form['abonne_id']
    document_id = request.form['document_id']
    date_emprunt = datetime.now()
    date_retour_prevu = request.form['date_retour_prevu']
    
    # Convert the planned return date to a datetime object
    date_retour_prevu = datetime.strptime(date_retour_prevu, '%Y-%m-%d')

    # Check if the planned return date is before the borrowing date
    if date_retour_prevu < date_emprunt:
        return "La date de retour ne peut pas être antérieure à la date d'emprunt", 400
    
    # Prepare the data for the new loan (emprunt)
    data = {
        'abonne_id': abonne_id,
        'document_id': document_id,
        'date_emprunt': date_emprunt,
        'date_retour_prevu': date_retour_prevu,
        'statut': 'emprunté'
    }
    
    # Add the loan to the database using the helper function
    result = emprunt.add_emprunt(data, mongo)
    
    # Redirect to the list of emprunts after adding the new loan
    return redirect('/emprunts')





# Route pour supprimer un abonné
@app.route('/emprunts/<id>/delete', methods=['GET'])
def delete_emprunt_route(id):
    result = emprunt.delete_emprunt(id, mongo)
    if 'message' in result:
        return redirect('/emprunts')
    else:
        return "Erreur lors de la suppression", 404






















@app.route('/genres', methods=['GET'])
def genres_lister():
    genres = genre.get_genres(mongo)  # Récupère tous les documents
    return render_template('genres/lister.html', genres=genres)

# Route pour récupérer un genre par ID
@app.route('/genres/<id>/', methods=['GET'])
def show_genre_details(id):
    g = genre.get_genre_by_id(id, mongo)
    if g:
        return render_template('genres/details.html', genre=g)
    else:
        return "Genre non trouvé", 404

# Route pour afficher la page de modification
@app.route('/genres/<id>/update', methods=['GET'])
def show_update_genre_form(id):
    genre_to_update = genre.get_genre_by_id(id, mongo)
    if genre_to_update:
        return render_template('genres/modifier.html', genre=genre_to_update)
    else:
        return "Genre non trouvé", 404

# Route pour mettre à jour un genre
@app.route('/genres/<id>/update', methods=['POST'])  # Correction du chemin '/gernes' en '/genres'
def update_genre(id):
    data = request.form
    if not data:
        return "Aucune donnée fournie", 400
    result = genre.update_genre(id, data, mongo)
    return redirect('/genres')

# Route pour supprimer un genre
@app.route('/genres/<id>/delete', methods=['GET'])
def delete_genre_route(id):
    result = genre.delete_genre(id, mongo)
    if 'message' in result:
        return redirect('/genres')  # Correction de la redirection '/genre' en '/genres'
    else:
        return "Erreur lors de la suppression", 404

# Route pour ajouter un genre
@app.route('/add_genre', methods=['GET'])
def show_add_genre_form():
    
    return render_template('genres/ajouter.html')

@app.route('/add_genre', methods=['POST'])
def add_genre_route():
    genre_name = request.form['genre_name']  # Changement de 'genre' en 'genre_name'
    
    data = {
        'genre_name': genre_name,  # Utilisation de 'genre_name' au lieu de 'genre'
    }
    
    result = genre.add_genre(data, mongo)
    return redirect('/genres')





if __name__ == '__main__':  # Corrigé name en _name_
    print("Démarrage de l'application Flask sur le port 5000")
    app.run(debug=True, port=5000)