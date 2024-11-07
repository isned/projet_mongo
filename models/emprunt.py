from datetime import datetime

# CREATE - Ajouter un emprunt
def add_emprunt(data, mongo):
    emprunt = {
        "abonne_id": data['abonne_id'],
        "document_id": data['document_id'],
        "date_emprunt": datetime.now(),
        "date_retour_prevu": data['date_retour_prevu'],
        "statut": "emprunté"
    }
    mongo.db.emprunts.insert_one(emprunt)

    # Mettre à jour la disponibilité du document
    mongo.db.documents.update_one(
        {"_id": data['document_id']},
        {"$set": {"disponibilite": False}}
    )

    # Ajouter l'emprunt à l'historique de l'abonné
    mongo.db.abonnes.update_one(
        {"_id": data['abonne_id']},
        {"$push": {"emprunts_en_cours": emprunt}}
    )

    return {"message": "Emprunt enregistré avec succès!"}

# READ - Récupérer tous les emprunts
def get_emprunts(mongo):
    emprunts = mongo.db.emprunts.find()
    result = []
    for emprunt in emprunts:
        emprunt['_id'] = str(emprunt['_id'])  # Convertir ObjectId en string
        result.append(emprunt)
    return result

# READ - Récupérer un emprunt par son ID
def get_emprunt_by_id(id, mongo):
    emprunt = mongo.db.emprunts.find_one({"_id": mongo.ObjectId(id)})
    if emprunt:
        emprunt['_id'] = str(emprunt['_id'])  # Convertir ObjectId en string
        return emprunt
    return None  # Retourne None si l'emprunt n'existe pas

# UPDATE - Mettre à jour un emprunt
def update_emprunt(id, data, mongo):
    result = mongo.db.emprunts.update_one(
        {"_id": mongo.ObjectId(id)},
        {"$set": data}  # Mise à jour des champs spécifiés
    )
    if result.modified_count > 0:
        return {"message": "Emprunt mis à jour avec succès!"}
    return {"message": "Aucune modification apportée"}, 400

# DELETE - Supprimer un emprunt
def delete_emprunt(id, mongo):
    result = mongo.db.emprunts.delete_one({"_id": mongo.ObjectId(id)})
    if result.deleted_count > 0:
        # Remettre la disponibilité du document à True
        mongo.db.documents.update_one(
            {"_id": mongo.ObjectId(id)}, 
            {"$set": {"disponibilite": True}}
        )
        return {"message": "Emprunt supprimé avec succès!"}
    return {"message": "Emprunt non trouvé"}, 404