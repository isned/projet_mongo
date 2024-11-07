from datetime import datetime
from bson import ObjectId  # Importation d'ObjectId depuis bson

# CREATE - Ajouter un abonné
def add_abonne(data, mongo):
    abonne = {
        "nom": data['nom'],
        "prenom": data['prenom'],
        "adresse": data['adresse'],
        "date_inscription": datetime.now(),
        "emprunts_en_cours": [],
        "historique_emprunts": []
    }
    mongo.db.abonnes.insert_one(abonne)
    return {"message": "Abonné ajouté avec succès!"}

# READ - Récupérer tous les abonnés
def get_abonnes(mongo):
    abonnes = mongo.db.abonnes.find()
    result = []
    for abonne in abonnes:
        abonne['_id'] = str(abonne['_id'])  # Convertir l'ObjectId en string pour l'affichage
        result.append(abonne)
    return result

# READ - Récupérer un abonné par son ID
def get_abonne_by_id(id, mongo):
    abonne = mongo.db.abonnes.find_one({"_id": ObjectId(id)})  # Utilisation de ObjectId ici
    if abonne:
        abonne['_id'] = str(abonne['_id'])  # Convertir l'ObjectId en string
        return abonne
    return None

# UPDATE - Mettre à jour un abonné
def update_abonne(id, data, mongo):
    result = mongo.db.abonnes.update_one(
        {"_id": ObjectId(id)},  # Utilisation de ObjectId ici
        {"$set": data}  # Mise à jour des champs spécifiés
    )
    if result.modified_count > 0:
        return {"message": "Abonné mis à jour avec succès!"}
    return {"message": "Aucune modification apportée"}, 400

# DELETE - Supprimer un abonné
def delete_abonne(id, mongo):
    result = mongo.db.abonnes.delete_one({"_id": ObjectId(id)})  # Utilisation de ObjectId ici
    if result.deleted_count > 0:
        return {"message": "Abonné supprimé avec succès!"}
    return {"message": "Abonné non trouvé"}, 404