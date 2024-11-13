from bson import ObjectId
from datetime import datetime


def add_genre(data, mongo):
    genre = {
        "genre": data['genre']  
    }
    mongo.db.genres.insert_one(genre)
    return {"message": "Genre ajouté avec succès!"}


def get_genres(mongo):
    genres = mongo.db.genres.find()
    result = []
    for genre in genres:
        genre['_id'] = str(genre['_id']) 
        result.append(genre)
    return result

def get_genre_by_id(id, mongo):
    genre = mongo.db.genres.find_one({"_id": ObjectId(id)})
    if genre:
        genre['_id'] = str(genre['_id'])  
        return genre
    return None


def delete_genre(id, mongo):
    result = mongo.db.genres.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return {"message": "Genre supprimé avec succès!"}
    else:
        return {"message": "Genre non trouvé"}, 404

def update_genre(id, data, mongo):
    updated_genre = {
        "genre": data['genre'],  
    }
    mongo.db.genres.update_one({"_id": ObjectId(id)}, {"$set": updated_genre})
    return {"message": "Genre mis à jour avec succès!"}
