





from bson import ObjectId
from datetime import datetime
from bson.objectid import ObjectId

# CREATE - Ajouter un document
def add_abonne(data, mongo):
    abonne = {
        "nom": data['nom'],
        "prenom": data['prenom'],
        "adresse": data['adresse'],
        "date_inscription": data['date_inscription'],
      
    }
    mongo.db.abonnes.insert_one(abonne)
    return {"message": "Abonné ajouté avec succès!"}

# READ - Récupérer tous les documents
def get_abonnes(mongo):
    abonnes = mongo.db.aboones.find()
    result = []
    for abonne in abonnes:
        abonne['_id'] = str(abonne['_id'])  # Convertir l'ObjectId en string pour l'affichage
        result.append(abonne)
    return result

# READ - Récupérer un document par son ID
def get_abonne_by_id(id, mongo):
    abonne = mongo.db.abonnes.find_one({"_id": ObjectId(id)})  # Utilisation de ObjectId ici
    if abonne:
        abonne['_id'] = str(abonne['_id'])  # Convertir l'ObjectId en string
        return abonne
    return None



def delete_abonne(id, mongo):
    """Supprimer un document dans la base de données"""
    result = mongo.db.abonnes.delete_one({"_id": ObjectId(id)})
    
    if result.deleted_count > 0:
        return {"message": "Abonné supprimé avec succès!"}
    else:
        return {"message": "Abonné non trouvé"}, 404







def get_abonne_by_id(id,mongo):
    """Récupérer un document par son ID"""
    return mongo.db.abonnes.find_one({"_id": ObjectId(id)})

def update_abonne(id, data, mongo):
    """Mettre à jour un document dans la base de données"""
    updated_abonne = {
        "nom": data['nom'],
        "prenom": data['prenom'],
        "adresse": data['adresse'],
        "date_inscription": data['date_inscription'],
        
    }

    # Mise à jour du document dans la base de données
    mongo.db.abonnes.update_one({"_id": ObjectId(id)}, {"$set": updated_abonne})

    return {"message": "Abonné mis à jour avec succès!"}