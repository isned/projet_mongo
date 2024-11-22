from bson import ObjectId
from bson.objectid import ObjectId
from bson import ObjectId

def add_document(data, mongo):
    
    genre_id = ObjectId(data['genre'])  
    document = {
        "titre": data['titre'],
        "auteur": data['auteur'],
        "genre": genre_id, 
        "date_publication": data['date_publication'],
        "disponibilite": data['disponibilite']
    }
    mongo.db.documents.insert_one(document)
    return {"message": "Document ajouté avec succès!"}

def get_documents(mongo):
    documents = mongo.db.documents.aggregate([
        {
            "$lookup": {
                "from": "genres",  
                "localField": "genre",  
                "foreignField": "_id",  
                "as": "genre_info"  
            }
        },
        {
            "$unwind": "$genre_info"  
        }
    ])
    
    result = []
    for document in documents:
        document['_id'] = str(document['_id'])  
        
       
        genre_name = document['genre_info'].get('genre_name', 'Nom du genre non défini')
        document['genre'] = genre_name  
        del document['genre_info']  
        result.append(document)
    
    return result



def get_document_by_id(id, mongo):
    document = mongo.db.documents.aggregate([
        {
            "$match": {
                "_id": ObjectId(id)  
            }
        },
        {
            "$lookup": {
                "from": "genres",  
                "localField": "genre",  
                "as": "genre_info"  
            }
        },
        {
            "$unwind": "$genre_info"  
        }
    ])
    
    document = list(document)
    if document:
        document = document[0]
        document['_id'] = str(document['_id'])  
        document['genre'] = document['genre_info']['genre_name']  
        del document['genre_info']  
        return document
    return None


def update_document(id, data, mongo):
    
    
    genre = mongo.db.genres.find_one({"genre": data['genre']})
    
    
    if not genre:
        genre = mongo.db.genres.insert_one({"genre": data['genre']})
        genre_id = genre.inserted_id  
    else:
        genre_id = genre['_id']  
    
   
    updated_document = {
        "titre": data['titre'],
        "auteur": data['auteur'],
        "genre": ObjectId(genre_id),  
        "date_publication": data['date_publication'],
        "disponibilite": data['disponibilite']
    }

   
    mongo.db.documents.update_one({"_id": ObjectId(id)}, {"$set": updated_document})

    return {"message": "Document mis à jour avec succès!"}

def delete_document(id, mongo):
  
    result = mongo.db.documents.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count > 0:
        return {"message": "Document supprimé avec succès!"}
    else:
        return {"message": "Document non trouvé"}, 404


