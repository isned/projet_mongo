from bson import ObjectId

from bson.objectid import ObjectId

# CREATE - Ajouter un document
def add_document(data, mongo):
    document = {
        "titre": data['titre'],
        "auteur": data['auteur'],
        "genre": data['genre'],
        "date_publication": data['date_publication'],
        "disponibilite": data['disponibilite']
    }
    mongo.db.documents.insert_one(document)
    return {"message": "Document ajouté avec succès!"}

# READ - Récupérer tous les documents
def get_documents(mongo):
    documents = mongo.db.documents.find()
    result = []
    for document in documents:
        document['_id'] = str(document['_id'])  # Convertir l'ObjectId en string pour l'affichage
        result.append(document)
    return result

# READ - Récupérer un document par son ID
def get_document_by_id(id, mongo):
    document = mongo.db.documents.find_one({"_id": ObjectId(id)})  # Utilisation de ObjectId ici
    if document:
        document['_id'] = str(document['_id'])  # Convertir l'ObjectId en string
        return document
    return None



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

def update_document(id, data, mongo):
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

    return {"message": "Document mis à jour avec succès!"}




def get_documents(mongo):
    documents = mongo.db.documents.find()
    result = []
    for document in documents:
        document['_id'] = str(document['_id'])  # Convertir l'ObjectId en string
        result.append(document)
    return result