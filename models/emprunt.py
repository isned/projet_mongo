from datetime import datetime
from bson import ObjectId





'''def add_emprunt(data, mongo):
    # Check if the document is available before adding the loan
    document = mongo.db.documents.find_one({"_id": ObjectId(data['document_id'])})
    if not document or document.get('statut') != 'Disponible':  # Fixed line
        return {"message": "Le document n'est pas disponible pour un emprunt."}, 400
    
    # Prepare the emprunt (loan) data
    emprunt = {
        "abonne_id": data['abonne_id'],
        "document_id": data['document_id'],
        "date_emprunt": datetime.now(),
        "date_retour_prevu": data['date_retour_prevu'],
        "statut": "emprunté"
    }
    
    # Insert the emprunt into the database
    mongo.db.emprunts.insert_one(emprunt)'''


def add_emprunt(data, mongo):
    # Vérifier si le document est disponible avant d'ajouter l'emprunt
    document = mongo.db.documents.find_one({"_id": ObjectId(data['document_id'])})
    if not document or document.get('disponibilite') != 'Disponible':  # Vérification de la disponibilité
        return {"message": "Le document n'est pas disponible pour un emprunt."}, 400
    
    # Préparer les données de l'emprunt
    emprunt = {
        "abonne_id": data['abonne_id'],
        "document_id": data['document_id'],
        "date_emprunt": datetime.now(),
        "date_retour_prevu": data['date_retour_prevu'],
        "statut": "emprunté"
    }
    
    # Insérer l'emprunt dans la base de données
    mongo.db.emprunts.insert_one(emprunt)
    
    return {"message": "Emprunt ajouté avec succès."}, 200

'''def get_emprunts(mongo):
    emprunts = mongo.db.emprunts.find()
    result = []
    for emprunt in emprunts:
        # Récupérer l'abonné par ID
        abonne = mongo.db.abonnes.find_one({"_id": ObjectId(emprunt['abonne_id'])})
        if abonne:
            abonne['_id'] = str(abonne['_id'])
            emprunt['abonne'] = abonne  # Ajouter les détails de l'abonné à l'emprunt
        
        # Récupérer le document par ID
        document = mongo.db.documents.find_one({"_id": ObjectId(emprunt['document_id'])})
        if document:
            document['_id'] = str(document['_id'])
            emprunt['document'] = document  # Ajouter les détails du document à l'emprunt
        
        # Vérifier si la date de retour est passée et mettre à jour le statut
        if datetime.now() >= emprunt['date_retour_prevu']:
            emprunt['statut'] = 'retourné'
        
        emprunt['_id'] = str(emprunt['_id'])  # Convertir l'ObjectId en string pour l'affichage
        result.append(emprunt)
    return result'''


def get_emprunts(mongo):
    emprunts = mongo.db.emprunts.find()
    result = []
    for emprunt in emprunts:
        # Récupérer l'abonné par ID
        abonne = mongo.db.abonnes.find_one({"_id": ObjectId(emprunt['abonne_id'])})
        if abonne:
            abonne['_id'] = str(abonne['_id'])  # Convertir l'ObjectId en string pour l'affichage
            emprunt['abonne'] = abonne
        
        # Récupérer le document par ID
        document = mongo.db.documents.find_one({"_id": ObjectId(emprunt['document_id'])})
        if document:
            document['_id'] = str(document['_id'])  # Convertir l'ObjectId en string pour l'affichage
            emprunt['document'] = document
        
        # Vérifier si la date de retour est passée et mettre à jour le statut
        if datetime.now() >= emprunt['date_retour_prevu']:
            emprunt['statut'] = 'retourné'
        
        emprunt['_id'] = str(emprunt['_id'])  # Convertir l'ObjectId en string pour l'affichage
        result.append(emprunt)
    
    return result

def get_emprunt_by_id(id, mongo):
    emprunt = mongo.db.emprunts.find_one({"_id": ObjectId(id)})
    if emprunt:
        # Récupérer l'abonné et le document
        abonne = mongo.db.abonnes.find_one({"_id": ObjectId(emprunt['abonne_id'])})
        document = mongo.db.documents.find_one({"_id": ObjectId(emprunt['document_id'])})
        
        if abonne:
            abonne['_id'] = str(abonne['_id'])
            emprunt['abonne'] = abonne
        if document:
            document['_id'] = str(document['_id'])
            emprunt['document'] = document
        
        # Vérifier si la date de retour est passée et mettre à jour le statut
        if datetime.now() >= emprunt['date_retour_prevu']:
            emprunt['statut'] = 'retourné'
        
        emprunt['_id'] = str(emprunt['_id'])
        return emprunt
    return None

def delete_emprunt(id, mongo):
    result = mongo.db.emprunts.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return {"message": "Emprunt supprimé avec succès!"}
    else:
        return {"message": "Emprunt non trouvé"}, 404

def update_emprunt(id, data, mongo):
    # Vérifier si la date de retour prévue est dans le passé
    statut = "emprunté"
    if datetime.now() >= data['date_retour_prevu']:
        statut = "retourné"
    
    updated_emprunt = {
        "abonne_id": data['abonne_id'],
        "document_id": data['document_id'],
        "date_emprunt": datetime.now(),
        "date_retour_prevu": data['date_retour_prevu'],
        "statut": statut,  # Mettre à jour le statut
    }
    
    mongo.db.emprunts.update_one({"_id": ObjectId(id)}, {"$set": updated_emprunt})
    return {"message": "Emprunt mis à jour avec succès!"}