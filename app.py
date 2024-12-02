from flask import Flask, flash, redirect, render_template, request, jsonify, session, url_for
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_pymongo import PyMongo
from config import Config
from models import abonne, genre,user
from models import document
from models import emprunt
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import login_required

from datetime import datetime
from bson import ObjectId
from flask import request, redirect, render_template, jsonify

from models.user import User

app = Flask(__name__)  
app.config.from_object(Config)
# Ensure cookies are set correctly for third-party contexts
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Allow third-party cookies
app.config['SESSION_COOKIE_SECURE'] = False  # For development (should be True in production with HTTPS)
app.config['SECRET_KEY'] = 'your_secret_key_here'

mongo = PyMongo(app)
CORS(app) 


@app.route('/')
def home():
    emprunts = emprunt.get_emprunts(mongo)

    abonnes = {str(abonne['_id']): abonne for abonne in mongo.db.abonnes.find()}
    documents = {str(document['_id']): document for document in mongo.db.documents.find()}
    genres = {str(genre['_id']): genre for genre in mongo.db.genres.find()}

    return render_template('index.html', emprunts=emprunts, abonnes=abonnes, documents=documents, genres=genres)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'Email et mot de passe sont requis!'}), 400

        user = User.find_by_email(email, mongo.db.users)
        if not user:
            return jsonify({'message': 'Email ou mot de passe incorrect!'}), 401

        password_matches = user.check_password(password)
        if not password_matches:
            return jsonify({'message': 'Email ou mot de passe incorrect!'}), 401

        # Redirection après connexion réussie
        print(f"Connexion réussie pour l'utilisateur : {email}")
        return redirect(url_for('home'))  # Redirige vers la page principale

    return render_template('users/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'Email et mot de passe sont requis!'}), 400

        if User.find_by_email(email, mongo.db.users):
            return jsonify({'message': 'Cet email est déjà enregistré!'}), 409

        # Création d'un nouvel utilisateur
        new_user = User(email, password)
        new_user.save_to_db(mongo.db.users)
        print(f"Nouvel utilisateur créé : {email}")
        return redirect(url_for('login'))  # Redirige vers la page de connexion

    return render_template('users/register.html')



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



'''@app.route('/abonnes/<abonne_id>/historique', methods=['GET'])
def afficher_historique(abonne_id):
    historique = emprunt.get_historique_emprunts(abonne_id, mongo)
    return render_template('abonnes/historique.html', historique=historique)'''

@app.route('/abonnes/<id>/historique')
def afficher_historique(id):
    # Vérifier si l'abonné existe dans la base de données
    abonne = mongo.db.abonnes.find_one({"_id": ObjectId(id)})
    if not abonne:
        return "Abonné non trouvé", 404
    
    # Récupérer l'historique des emprunts pour cet abonné
    historique = emprunt.get_historique_emprunts(id, mongo)
    
    # Passer les données à la vue HTML
    return render_template('abonnes/historique.html', abonne=abonne, historique=historique)
















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
    # Fetch all loans and pass them to the template
    emprunts = emprunt.get_emprunts(mongo)
    return render_template('emprunts/lister.html', emprunts=emprunts)


@app.route('/emprunts/<id>/', methods=['GET'])
def show_emprunt_details(id):
    em = emprunt.get_emprunt_by_id(id, mongo)
    if em:
        # Récupérer l'abonné et le document liés à cet emprunt
        abonne = mongo.db.abonnes.find_one({'_id': em['abonne_id']})
        document = mongo.db.documents.find_one({'_id': em['document_id']})
        # Passer les données complètes à la template
        return render_template('emprunts/details.html', emprunt=em, abonne=abonne, document=document)
    else:
        return "Emprunt non trouvé", 404




@app.route('/emprunts/<id>/update', methods=['GET'])
def show_update_emprunt_form(id):
    # Récupérer l'emprunt à mettre à jour par ID
    emprunt_to_update = emprunt.get_emprunt_by_id(id, mongo)
    if emprunt_to_update:
        abonnes = mongo.db.abonnes.find()
        documents = mongo.db.documents.find()
        
        # Si date_retour_prevu existe, la formater correctement
        date_retour_prevu = emprunt_to_update['date_retour_prevu'].strftime('%Y-%m-%d') if 'date_retour_prevu' in emprunt_to_update else ''
        
        return render_template('emprunts/modifier.html', 
                               emprunt=emprunt_to_update,
                               abonnes=abonnes,
                               documents=documents,
                               date_retour_prevu=date_retour_prevu)
    else:
        return "Emprunt non trouvé", 404
@app.route('/emprunts/<id>/update', methods=['POST'])
def update_emprunt(id):
    # Récupérer l'emprunt à mettre à jour par ID
    emprunt_to_update = emprunt.get_emprunt_by_id(id, mongo)
    
    if emprunt_to_update:
        # Récupérer les données du formulaire soumis
        date_retour_prevu = request.form.get('date_retour_prevu')  # Nouvelle date de retour
        abonne_id = request.form.get('abonne_id')  # ID de l'abonné
        document_id = request.form.get('document_id')  # ID du document
        
        # Mettre à jour l'emprunt avec les nouvelles données
        updated_data = {
            'date_retour_prevu': datetime.strptime(date_retour_prevu, '%Y-%m-%d') if date_retour_prevu else None,
            'abonne_id': ObjectId(abonne_id) if abonne_id else None,  # Mise à jour de l'abonné
            'document_id': ObjectId(document_id) if document_id else None,  # Mise à jour du document
        }
        
        # Mettre à jour l'emprunt dans la base de données
        mongo.db.emprunts.update_one({'_id': ObjectId(id)}, {'$set': updated_data})
        
        return redirect('/emprunts')  # Rediriger vers la liste des emprunts
    else:
        return "Emprunt non trouvé", 404

@app.route('/add_emprunt', methods=['GET'])
def show_add_emprunt_form():
    # Fetch all subscribers and available documents
    abonnes = list(mongo.db.abonnes.find())
    documents_disponibles = list(mongo.db.documents.find({"disponibilite": "Disponible"}))

    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Render the form with available subscribers and documents
    return render_template('emprunts/ajouter.html', abonnes=abonnes, documents=documents_disponibles, current_date=current_date)


@app.route('/add_emprunt', methods=['POST'])
def add_emprunt_route():
    try:
        # Récupérer les données envoyées par la requête JSON
        abonne_id = request.json.get('abonne_id')
        document_id = request.json.get('document_id')
        date_emprunt = datetime.now()
        date_retour_prevu = request.json.get('date_retour_prevu')

        # Convertir la date de retour prévue
        date_retour_prevu = datetime.strptime(date_retour_prevu, '%Y-%m-%d')

        # Vérification de la date
        if date_retour_prevu < date_emprunt:
            return jsonify({
                'error': "La date de retour prévue ne peut pas être antérieure à la date d'emprunt."
            }), 400

        # Préparation des données pour la base
        data = {
            'abonne_id': abonne_id,
            'document_id': document_id,
            'date_emprunt': date_emprunt,
            'date_retour_prevu': date_retour_prevu,
            'statut': 'emprunté'
        }

        # Ajouter à la base de données
        result = emprunt.add_emprunt(data, mongo)

        # Retourner un succès en JSON
        return jsonify({'message': "Emprunt ajouté avec succès"}), 200

    except Exception as e:
        # Retourner une erreur générique
        return jsonify({'error': f"Erreur interne : {str(e)}"}), 500


    except Exception as e:
        return jsonify({'error': f"Erreur interne : {str(e)}"}), 500
    
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





@app.route('/dashboard')
def dashboard():
    emprunts = emprunt.get_emprunts(mongo)
    total_emprunts = len(emprunts)
    total_abonnes = mongo.db.abonnes.count_documents({})
    total_documents = mongo.db.documents.count_documents({})
    
    # Corrected counting of genres
    total_genres = mongo.db.genres.count_documents({})  # Count the number of genres in the 'genres' collection

    # Pass the data to the template
    return render_template('dashboard.html', 
                           emprunts=emprunts,
                           total_emprunts=total_emprunts,
                           total_abonnes=total_abonnes,
                           total_documents=total_documents,
                           total_genres=total_genres)


if __name__== '__main__':
    print("Démarrage de l'application Flask sur le port 5000")
    app.run(debug=True, port=5000)