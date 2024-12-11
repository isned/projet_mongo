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

app.config['SESSION_COOKIE_SAMESITE'] = 'None'  
app.config['SESSION_COOKIE_SECURE'] = False  
app.config['SECRET_KEY'] = 'your_secret_key_here'

mongo = PyMongo(app)
CORS(app) 


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('login'))
@app.route('/', methods=['GET', 'POST'])
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

        print(f"Connexion réussie pour l'utilisateur : {email}")
        return redirect(url_for('dashboard'))  

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

        new_user = User(email, password)
        new_user.save_to_db(mongo.db.users)
        print(f"Nouvel utilisateur créé : {email}")
        return redirect(url_for('login'))  

    return render_template('users/register.html')


@app.route('/abonnes', methods=['GET'])
def abonnes_lister():
    abonnes = abonne.get_abonnes(mongo)  
    return render_template('abonnes/lister.html', abonnes=abonnes)

@app.route('/abonnes/<id>/', methods=['GET'])
def show_abonne_details(id):
    ab = abonne.get_abonne_by_id(id, mongo)
    if ab:
        return render_template('abonnes/details.html', abonne=ab)
    else:
        return "Abonné non trouvé", 404

@app.route('/abonnes/<id>/update', methods=['GET'])
def show_update_abonne_form(id):
    abonne_to_update = abonne.get_abonne_by_id(id, mongo)
    if abonne_to_update:
        return render_template('abonnes/modifier.html', abonne=abonne_to_update)
    else:
        return "Abonné non trouvé", 404

@app.route('/abonnes/<id>/update', methods=['POST'])
def update_abonne(id):
    data = request.form
    if not data:
        return "Aucune donnée fournie", 400
    result = abonne.update_abonne(id, data, mongo)
    return redirect('/abonnes')

@app.route('/abonnes/<id>/delete', methods=['GET'])
def delete_abonne_route(id):
    result = abonne.delete_abonne(id, mongo)
    if 'message' in result:
        return redirect('/abonnes')
    else:
        return "Erreur lors de la suppression", 404

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



@app.route('/abonnes/<id>/historique')
def afficher_historique(id):
    
    abonne = mongo.db.abonnes.find_one({"_id": ObjectId(id)})
    if not abonne:
        return "Abonné non trouvé", 404
    
    historique = emprunt.get_historique_emprunts(id, mongo)
    
    return render_template('abonnes/historique.html', abonne=abonne, historique=historique)
















@app.route('/add_document', methods=['GET'])
def show_add_document_form():
    genres = list(mongo.db.genres.find())  
    print("Genres récupérés :", genres)   
    return render_template('documents/ajouter.html', genres=genres)


@app.route('/add_document', methods=['POST'])
def add_document_route():
   
    titre = request.form['titre']
    auteur = request.form['auteur']
    genre_id = request.form['genre_id']  
    date_publication = request.form['date_publication']
    disponibilite = request.form['disponibilite']
    
    data = {
        'titre': titre,
        'auteur': auteur,
        'genre': genre_id,  
        'date_publication': date_publication,
        'disponibilite': disponibilite
    }
    
   
    result = document.add_document(data, mongo)
    
    return redirect('/documents')


@app.route('/documents', methods=['GET'])
def documents_lister():
    documents = document.get_documents(mongo) 
    genres = list(mongo.db.genres.find())  
   
    return render_template('documents/lister.html', documents=documents,genres=genres)




@app.route('/documents/<id>/', methods=['GET'])
def show_document_details(id):
   
    doc = document.get_document_by_id(id, mongo)  
    if doc:
        return render_template('documents/details.html', document=doc)  
    else:
        return "Document non trouvé", 404  

@app.route('/documents/<id>/update', methods=['GET'])
def show_update_form(id):
   
    document_to_update = document.get_document_by_id(id, mongo)
    
    if document_to_update:
        
        genres = mongo.db.genres.find()
        return render_template('documents/modifier.html', document=document_to_update, genres=genres)
    else:
        return "Document non trouvé", 404



@app.route('/documents/<id>/update', methods=['POST'])
def update_document(id):
    data = request.form
    genre_id = ObjectId(data['genre'])  
    
    
    genre = mongo.db.genres.find_one({"_id": genre_id})
    if not genre:
        return "Genre non trouvé", 400

    updated_document = {
        "titre": data['titre'],
        "auteur": data['auteur'],
        "genre": genre_id,  
        "date_publication": data['date_publication'],
        "disponibilite": data['disponibilite']
    }

    mongo.db.documents.update_one({"_id": ObjectId(id)}, {"$set": updated_document})

    return redirect('/documents')  




@app.route('/documents/<id>/', methods=['PUT'])
def update_document_route(id):
    data = document.get_document_by_id(id, mongo)
    if data:
        return render_template('documents/update.html', document=data)
    return jsonify({"message": "Document non trouvé"}), 404


@app.route('/documents/<id>/delete', methods=['GET'])
def delete_document_route(id):
    try:
      
        result = document.delete_document(id, mongo)

       
        if 'message' in result:
            return redirect('/documents')  
        else:
            return "Erreur lors de la suppression du document", 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500









@app.route('/emprunts', methods=['GET'])
def emprunts_lister():
   
    emprunts = emprunt.get_emprunts(mongo)
    return render_template('emprunts/lister.html', emprunts=emprunts)


@app.route('/emprunts/<id>/', methods=['GET'])
def show_emprunt_details(id):
    em = emprunt.get_emprunt_by_id(id, mongo)
    if em:
       
        abonne = mongo.db.abonnes.find_one({'_id': em['abonne_id']})
        document = mongo.db.documents.find_one({'_id': em['document_id']})
      
        return render_template('emprunts/details.html', emprunt=em, abonne=abonne, document=document)
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
@app.route('/emprunts/<id>/update', methods=['POST'])
def update_emprunt(id):
  
    emprunt_to_update = emprunt.get_emprunt_by_id(id, mongo)
    
    if emprunt_to_update:
       
        date_retour_prevu = request.form.get('date_retour_prevu') 
        abonne_id = request.form.get('abonne_id')  
        document_id = request.form.get('document_id')  
        
      
        updated_data = {
            'date_retour_prevu': datetime.strptime(date_retour_prevu, '%Y-%m-%d') if date_retour_prevu else None,
            'abonne_id': ObjectId(abonne_id) if abonne_id else None,  
            'document_id': ObjectId(document_id) if document_id else None,  
        }
        
       
        mongo.db.emprunts.update_one({'_id': ObjectId(id)}, {'$set': updated_data})
        
        return redirect('/emprunts')  
    else:
        return "Emprunt non trouvé", 404

@app.route('/add_emprunt', methods=['GET'])
def show_add_emprunt_form():
   
    abonnes = list(mongo.db.abonnes.find())
    documents_disponibles = list(mongo.db.documents.find({"disponibilite": "Disponible"}))

 
    current_date = datetime.now().strftime('%Y-%m-%d')

   
    return render_template('emprunts/ajouter.html', abonnes=abonnes, documents=documents_disponibles, current_date=current_date)


@app.route('/add_emprunt', methods=['POST'])
def add_emprunt_route():
    try:
      
        abonne_id = request.json.get('abonne_id')
        document_id = request.json.get('document_id')
        date_emprunt = datetime.now()
        date_retour_prevu = request.json.get('date_retour_prevu')

        date_retour_prevu = datetime.strptime(date_retour_prevu, '%Y-%m-%d')

        if date_retour_prevu < date_emprunt:
            return jsonify({
                'error': "La date de retour prévue ne peut pas être antérieure à la date d'emprunt."
            }), 400

      
        data = {
            'abonne_id': abonne_id,
            'document_id': document_id,
            'date_emprunt': date_emprunt,
            'date_retour_prevu': date_retour_prevu,
            'statut': 'emprunté'
        }

       
        result = emprunt.add_emprunt(data, mongo)

        return jsonify({'message': "Emprunt ajouté avec succès"}), 200

    except Exception as e:
       
        return jsonify({'error': f"Erreur interne : {str(e)}"}), 500


    except Exception as e:
        return jsonify({'error': f"Erreur interne : {str(e)}"}), 500
    
    return redirect('/emprunts')



@app.route('/emprunts/<id>/delete', methods=['GET'])
def delete_emprunt_route(id):
    result = emprunt.delete_emprunt(id, mongo)
    if 'message' in result:
        return redirect('/emprunts')
    else:
        return "Erreur lors de la suppression", 404






















@app.route('/genres', methods=['GET'])
def genres_lister():
    genres = genre.get_genres(mongo)  
    return render_template('genres/lister.html', genres=genres)

@app.route('/genres/<id>/', methods=['GET'])
def show_genre_details(id):
    g = genre.get_genre_by_id(id, mongo)
    if g:
        return render_template('genres/details.html', genre=g)
    else:
        return "Genre non trouvé", 404

@app.route('/genres/<id>/update', methods=['GET'])
def show_update_genre_form(id):
    genre_to_update = genre.get_genre_by_id(id, mongo)
    if genre_to_update:
        return render_template('genres/modifier.html', genre=genre_to_update)
    else:
        return "Genre non trouvé", 404

@app.route('/genres/<id>/update', methods=['POST'])  
def update_genre(id):
    data = request.form
    if not data:
        return "Aucune donnée fournie", 400
    result = genre.update_genre(id, data, mongo)
    return redirect('/genres')

@app.route('/genres/<id>/delete', methods=['GET'])
def delete_genre_route(id):
    result = genre.delete_genre(id, mongo)
    if 'message' in result:
        return redirect('/genres')  
    else:
        return "Erreur lors de la suppression", 404

@app.route('/add_genre', methods=['GET'])
def show_add_genre_form():
    
    return render_template('genres/ajouter.html')

@app.route('/add_genre', methods=['POST'])
def add_genre_route():
    genre_name = request.form['genre_name']  
    
    data = {
        'genre_name': genre_name,  
    }
    
    result = genre.add_genre(data, mongo)
    return redirect('/genres')





@app.route('/dashboard')
def dashboard():
    emprunts = emprunt.get_emprunts(mongo)
    total_emprunts = len(emprunts)
    total_abonnes = mongo.db.abonnes.count_documents({})
    total_documents = mongo.db.documents.count_documents({})
    total_genres = mongo.db.genres.count_documents({})

    documents_disponibles = mongo.db.documents.count_documents({'disponibilite': 'Disponible'})
    documents_non_disponibles = mongo.db.documents.count_documents({'disponibilite': 'Indisponible'})
   
     
    return render_template('dashboard.html', 
                           emprunts=emprunts,
                           total_emprunts=total_emprunts,
                           total_abonnes=total_abonnes,
                           total_documents=total_documents,
                           total_genres=total_genres,
                           documents_disponibles=documents_disponibles,
                           documents_non_disponibles=documents_non_disponibles,
                          )






if __name__== '__main__':
    print("Démarrage de l'application Flask sur le port 5000")
    app.run(debug=True, port=5000)