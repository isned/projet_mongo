from bson import ObjectId


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

# UPDATE - Mettre à jour un document
'''def update_document(id, data, mongo):
    result = mongo.db.documents.update_one(
        {"_id": ObjectId(id)},  # Utilisation de ObjectId ici
        {"$set": data}  # Mise à jour des champs spécifiés
    )
    if result.modified_count > 0:
        return {"message": "Document mis à jour avec succès!"}
    return {"message": "Aucune modification apportée"}, 400'''

# UPDATE - Modifier un document
def update_document(id, data, mongo):
    updated_document = {
        "titre": data['titre'],
        "auteur": data['auteur'],
        "genre": data['genre'],
        "date_publication": data['date_publication'],
        "disponibilite": data['disponibilite']
    }
    mongo.db.documents.update_one({"_id": ObjectId(id)}, {"$set": updated_document})
    return {"message": "Document mis à jour avec succès!"}

# DELETE - Supprimer un document
def delete_document(id, mongo):
    result = mongo.db.documents.delete_one({"_id": ObjectId(id)})  # Utilisation de ObjectId ici
    if result.deleted_count > 0:
        return {"message": "Document supprimé avec succès!"}
    return {"message": "Document non trouvé"}, 404