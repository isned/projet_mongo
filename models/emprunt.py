from datetime import datetime, timedelta

# CREATE - Ajouter un emprunt
def add_emprunt(data, mongo):
    emprunt = {
        "abonne_id": data['abonne_id'],
        "document_id": data['document_id'],
        "date_emprunt": datetime.now(),
        "date_retour_prevu": data['date_retour_prevu'],
        "date_retour_effectif": None,  # Pour être défini lors du retour
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
        emprunt['retard'] = check_retard(emprunt)
        result.append(emprunt)
    return result

# READ - Récupérer l'historique des emprunts pour un abonné
def get_emprunts_by_abonne(abonne_id, mongo):
    emprunts = mongo.db.emprunts.find({"abonne_id": abonne_id})
    result = []
    for emprunt in emprunts:
        emprunt['_id'] = str(emprunt['_id'])
        emprunt['retard'] = check_retard(emprunt)
        result.append(emprunt)
    return result

# Vérifier le retard d'un emprunt
def check_retard(emprunt):
    if emprunt['date_retour_effectif'] is None and datetime.now() > emprunt['date_retour_prevu']:
        return "En retard"
    return "À jour" if emprunt['date_retour_effectif'] else "À rendre"

# UPDATE - Enregistrer le retour d'un emprunt
def enregistrer_retour(id, mongo):
    emprunt = mongo.db.emprunts.find_one({"_id": mongo.ObjectId(id)})
    if not emprunt:
        return {"message": "Emprunt non trouvé"}, 404

    # Mettre à jour la date de retour et le statut
    result = mongo.db.emprunts.update_one(
        {"_id": mongo.ObjectId(id)},
        {"$set": {"date_retour_effectif": datetime.now(), "statut": "retourné"}}
    )

    # Remettre la disponibilité du document à True
    mongo.db.documents.update_one(
        {"_id": emprunt['document_id']},
        {"$set": {"disponibilite": True}}
    )

    if result.modified_count > 0:
        return {"message": "Retour enregistré avec succès!"}
    return {"message": "Aucune modification apportée"}, 400

# DELETE - Supprimer un emprunt
def delete_emprunt(id, mongo):
    emprunt = mongo.db.emprunts.find_one({"_id": mongo.ObjectId(id)})
    if not emprunt:
        return {"message": "Emprunt non trouvé"}, 404

    result = mongo.db.emprunts.delete_one({"_id": mongo.ObjectId(id)})
    if result.deleted_count > 0:
        # Remettre la disponibilité du document à True
        mongo.db.documents.update_one(
            {"_id": emprunt['document_id']},
            {"$set": {"disponibilite": True}}
        )
        return {"message": "Emprunt supprimé avec succès!"}
    return {"message": "Aucune modification apportée"}, 400