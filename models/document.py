from bson import ObjectId

from bson.objectid import ObjectId

# CREATE - Ajouter un document
'''def add_document(data, mongo):
    document = {
        "titre": data['titre'],
        "auteur": data['auteur'],
        "genre": data['genre'],
        "date_publication": data['date_publication'],
        "disponibilite": data['disponibilite']
    }
    mongo.db.documents.insert_one(document)
    return {"message": "Document ajouté avec succès!"}'''
from bson import ObjectId

# CREATE - Ajouter un document avec un genre qui est une référence à la collection genres
def add_document(data, mongo):
    # Vérifier si le genre existe dans la collection genres
    genre = mongo.db.genres.find_one({"genre": data['genre']})
    
    # Si le genre n'existe pas, on peut le créer
    if not genre:
        genre = mongo.db.genres.insert_one({"genre": data['genre']})
        genre_id = genre.inserted_id  # Récupérer l'ObjectId du genre ajouté
    else:
        genre_id = genre['_id']  # Récupérer l'ObjectId du genre existant
    
    # Créer le document en ajoutant l'ObjectId du genre
    document = {
        "titre": data['titre'],
        "auteur": data['auteur'],
        "genre": ObjectId(genre_id),  # Utilisation de l'ObjectId du genre
        "date_publication": data['date_publication'],
        "disponibilite": data['disponibilite']
    }
    mongo.db.documents.insert_one(document)
    return {"message": "Document ajouté avec succès!"}


# READ - Récupérer tous les documents
'''def get_documents(mongo):
    documents = mongo.db.documents.find()
    result = []
    for document in documents:
        document['_id'] = str(document['_id'])  # Convertir l'ObjectId en string pour l'affichage
        result.append(document)
    return result'''

def get_documents(mongo):
    documents = mongo.db.documents.aggregate([
        {
            "$lookup": {
                "from": "genres",  # Nom de la collection genres
                "localField": "genre",  # Champ genre dans la collection documents
                "foreignField": "_id",  # L'ObjectId dans la collection genres
                "as": "genre_info"  # Alias pour les informations sur le genre
            }
        },
        {
            "$unwind": "$genre_info"  # Décomposer le tableau genre_info
        }
    ])
    
    result = []
    for document in documents:
        document['_id'] = str(document['_id'])  # Convertir l'ObjectId en string pour l'affichage
        document['genre'] = document['genre_info']['genre']  # Remplacer le champ genre par le nom du genre
        del document['genre_info']  # Supprimer l'alias 'genre_info'
        result.append(document)
    
    return result


# READ - Récupérer un document par son ID
'''def get_document_by_id(id, mongo):
    document = mongo.db.documents.find_one({"_id": ObjectId(id)})  # Utilisation de ObjectId ici
    if document:
        document['_id'] = str(document['_id'])  # Convertir l'ObjectId en string
        return document
    return None'''


def get_document_by_id(id, mongo):
    document = mongo.db.documents.aggregate([
        {
            "$match": {
                "_id": ObjectId(id)  # Chercher le document avec l'ID donné
            }
        },
        {
            "$lookup": {
                "from": "genres",  # Nom de la collection genres
                "localField": "genre",  # Champ genre dans la collection documents
                "foreignField": "_id",  # L'ObjectId dans la collection genres
                "as": "genre_info"  # Alias pour les informations sur le genre
            }
        },
        {
            "$unwind": "$genre_info"  # Décomposer le tableau genre_info
        }
    ])
    
    document = list(document)
    if document:
        document = document[0]
        document['_id'] = str(document['_id'])  # Convertir l'ObjectId en string
        document['genre'] = document['genre_info']['genre']  # Remplacer le champ genre par le nom du genre
        del document['genre_info']  # Supprimer l'alias 'genre_info'
        return document
    return None




'''def delete_document(id, mongo):
    """Supprimer un document dans la base de données"""
    result = mongo.db.documents.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count > 0:
        return {"message": "Document supprimé avec succès!"}
    else:
        return {"message": "Document non trouvé"}, 404'''


def delete_document(id, mongo):
    """Supprimer un document dans la base de données"""
    result = mongo.db.documents.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count > 0:
        return {"message": "Document supprimé avec succès!"}
    else:
        return {"message": "Document non trouvé"}, 404








def get_document_by_id(id,mongo):
    """Récupérer un document par son ID"""
    return mongo.db.documents.find_one({"_id": ObjectId(id)})

'''def update_document(id, data, mongo):
    """Mettre à jour un document dans la base de données"""
    updated_document = {
        "titre": data['titre'],
        "auteur": data['auteur'],
        "genre": data['genre'],
        "date_publication": data['date_publication'],
        "disponibilite": data['disponibilite']
    }

    # Mise à jour du document dans la base de données
    mongo.db.documents.update_one({"_id": ObjectId(id)}, {"$set": updated_document})

    return {"message": "Document mis à jour avec succès!"}'''



def update_document(id, data, mongo):
    """Mettre à jour un document dans la base de données"""
    # Vérifier si le genre existe dans la collection genres
    genre = mongo.db.genres.find_one({"genre": data['genre']})
    
    # Si le genre n'existe pas, on peut le créer
    if not genre:
        genre = mongo.db.genres.insert_one({"genre": data['genre']})
        genre_id = genre.inserted_id  # Récupérer l'ObjectId du genre ajouté
    else:
        genre_id = genre['_id']  # Récupérer l'ObjectId du genre existant
    
    # Créer le document mis à jour en ajoutant l'ObjectId du genre
    updated_document = {
        "titre": data['titre'],
        "auteur": data['auteur'],
        "genre": ObjectId(genre_id),  # Utilisation de l'ObjectId du genre
        "date_publication": data['date_publication'],
        "disponibilite": data['disponibilite']
    }

    # Mise à jour du document dans la base de données
    mongo.db.documents.update_one({"_id": ObjectId(id)}, {"$set": updated_document})

    return {"message": "Document mis à jour avec succès!"}





def get_documents(mongo):
    documents = mongo.db.documents.find()
    result = []
    for document in documents:
        document['_id'] = str(document['_id'])  # Convertir l'ObjectId en string
        result.append(document)
    return result