from datetime import datetime
from bson import ObjectId



def add_emprunt(data, mongo):
    emprunt = {
        "abonne_id": data['abonne_id'],
        "document_id": data['document_id'],
        "date_emprunt": datetime.now(),
        "date_retour_prevu": data['date_retour_prevu'],
        "statut": "emprunté"
    }
    mongo.db.emprunts.insert_one(emprunt)


def get_emprunts(mongo):
    emprunts= mongo.db.emprunts.find()
    result = []
    for emprunt in emprunts:
        emprunt['_id'] = str(emprunt['_id'])  # Convertir l'ObjectId en string pour l'affichage
        result.append(emprunt)
    return result

def get_emprunt_by_id(id, mongo):
    emprunt = mongo.db.emprunts.find_one({"_id": ObjectId(id)})
    if emprunt:
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
    updated_emprunt = {
         "abonne_id": data['abonne_id'],
        "document_id": data['document_id'],
        "date_emprunt": datetime.now(),
        "date_retour_prevu": data['date_retour_prevu'],
       
        "statut": "emprunté",
    }
    mongo.db.emprunts.update_one({"_id": ObjectId(id)}, {"$set": updated_emprunt})
    return {"message": "Emprunt mis à jour avec succès!"}