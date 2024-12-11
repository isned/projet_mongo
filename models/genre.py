from bson import ObjectId
from datetime import datetime

def add_genre(data, mongo):
    genre = {
        "genre_name": data['genre_name'],  # Vérifiez si cette clé existe
    }
    mongo.db.genres.insert_one(genre)
    return {"message": "Genre ajouté avec succès!"}

def update_genre(id, data, mongo):
    updated_genre = {
        "genre_name": data['genre_name'], 
    }
    mongo.db.genres.update_one({"_id": ObjectId(id)}, {"$set": updated_genre})
    return {"message": "Genre mis à jour avec succès!"}

# READ - Récupérer tous les documents
def get_genres(mongo):
    genres = mongo.db.genres.find()
    result = []
    for genre in genres:
        genre['_id'] = str(genre['_id'])  # Convertir l'ObjectId en string
        genre['genre_name'] = genre.pop('genre_name')  # Remplacer 'genre' par 'genre_name'
        result.append(genre)
    return result

# READ - Récupérer un document par son ID
def get_genre_by_id(id, mongo):
    genre = mongo.db.genres.find_one({"_id": ObjectId(id)})
    if genre:
        genre['_id'] = str(genre['_id'])
        genre['genre_name'] = genre.pop('genre_name')  # Remplacer 'genre' par 'genre_name'
        return genre
    return None

# DELETE - Supprimer un document
def delete_genre(id, mongo):
    result = mongo.db.genres.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return {"message": "Genre supprimé avec succès!"}
    else:
        return {"message": "Genre non trouvé"}, 404

# UPDATE - Mettre à jour un document
'''def update_genre(id, data, mongo):
    updated_genre = {
        "genre_name": data['genre_name'],  # Changer genre en genre_name
    }
    mongo.db.genres.update_one({"_id": ObjectId(id)}, {"$set": updated_genre})
    return {"message": "Genre mis à jour avec succès!"}'''
