'''from datetime import datetime
from bson import ObjectId








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



def get_emprunts(mongo):
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
        date_retour_prevu_str = emprunt.get('date_retour_prevu')
        
        if date_retour_prevu_str:
            try:
                # Convertir la chaîne en datetime
                date_retour_prevu = datetime.strptime(date_retour_prevu_str, "%Y-%m-%d")
                
                # Comparer la date de retour prévue avec la date actuelle
                if datetime.now() >= date_retour_prevu:
                    emprunt['statut'] = 'retourné'
            except ValueError as e:
                print(f"Erreur de format de date pour {date_retour_prevu_str}: {e}")
        
        emprunt['_id'] = str(emprunt['_id'])  # Convertir l'ObjectId en string pour l'affichage
        result.append(emprunt)
    return result




from datetime import datetime

def get_emprunt_by_id(id, mongo):
    emprunt = mongo.db.emprunts.find_one({"_id": ObjectId(id)})
    if emprunt:
        # Conversion de date_retour_prevu en datetime
        date_retour_prevu_str = emprunt.get('date_retour_prevu')
        if date_retour_prevu_str:  # Vérifie que la date n'est pas None ou absente
            try:
                date_retour_prevu = datetime.strptime(date_retour_prevu_str, "%Y-%m-%d")
                # Comparaison après conversion
                if datetime.now() >= date_retour_prevu:
                    emprunt['statut'] = 'retourné'
            except ValueError as e:
                print(f"Erreur de format de date: {date_retour_prevu_str} - {e}")
        
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
    return {"message": "Emprunt mis à jour avec succès!"}'''

from datetime import datetime
from bson import ObjectId


# Function to add a loan (emprunt)
def add_emprunt(data, mongo):
    # Check if the document is available before adding the loan
    document = mongo.db.documents.find_one({"_id": ObjectId(data['document_id'])})
    if not document or document.get('disponibilite') != 'Disponible':  # Check availability
        return {"message": "Le document n'est pas disponible pour un emprunt."}, 400

    # Prepare the loan data
    emprunt = {
        "abonne_id": data['abonne_id'],
        "document_id": data['document_id'],
        "date_emprunt": datetime.now(),
        "date_retour_prevu": data['date_retour_prevu'],
        "statut": "emprunté"
    }

    # Insert the loan into the database
    mongo.db.emprunts.insert_one(emprunt)

    return {"message": "Emprunt ajouté avec succès."}, 200


from datetime import datetime

def get_emprunts(mongo):
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
        date_retour_prevu = emprunt.get('date_retour_prevu')
        
        if date_retour_prevu:
            # Si date_retour_prevu est déjà un objet datetime, pas besoin de conversion
            if isinstance(date_retour_prevu, datetime):
                # Comparer la date de retour prévue avec la date actuelle
                if datetime.now() >= date_retour_prevu:
                    emprunt['statut'] = 'retourné'
            else:
                try:
                    # Sinon, si c'est une chaîne, la convertir en datetime
                    date_retour_prevu = datetime.strptime(date_retour_prevu, "%Y-%m-%d")
                    # Comparer la date de retour prévue avec la date actuelle
                    if datetime.now() >= date_retour_prevu:
                        emprunt['statut'] = 'retourné'
                except ValueError as e:
                    print(f"Erreur de format de date pour {date_retour_prevu}: {e}")
        
        emprunt['_id'] = str(emprunt['_id'])  # Convertir l'ObjectId en string pour l'affichage
        result.append(emprunt)
    return result


# Fonction pour obtenir un emprunt spécifique par ID
def get_emprunt_by_id(id, mongo):
    emprunt = mongo.db.emprunts.find_one({"_id": ObjectId(id)})
    if emprunt:
        # Récupérer la date de retour prévue
        date_retour_prevu_str = emprunt.get('date_retour_prevu')
        if date_retour_prevu_str:  # S'assurer que la date existe
            try:
                # Si c'est déjà un datetime, on le laisse tel quel
                if isinstance(date_retour_prevu_str, datetime):
                    date_retour_prevu = date_retour_prevu_str
                else:
                    # Sinon, on la convertit à partir de la chaîne (si c'est une chaîne de caractères)
                    date_retour_prevu = datetime.strptime(date_retour_prevu_str, "%Y-%m-%d")
                
                # Comparer après la conversion
                if datetime.now() >= date_retour_prevu:
                    emprunt['statut'] = 'retourné'
            except ValueError as e:
                print(f"Erreur de format de date: {date_retour_prevu_str} - {e}")

        emprunt['_id'] = str(emprunt['_id'])  # Convertir l'ObjectId en string pour l'affichage
        return emprunt
    return None



# Function to delete a loan by ID
def delete_emprunt(id, mongo):
    result = mongo.db.emprunts.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return {"message": "Emprunt supprimé avec succès!"}
    else:
        return {"message": "Emprunt non trouvé"}, 404


# Function to update a loan
def update_emprunt(id, data, mongo):
    # Check if the planned return date is in the past
    statut = "emprunté"
    if datetime.now() >= data['date_retour_prevu']:
        statut = "retourné"

    updated_emprunt = {
        "abonne_id": data['abonne_id'],
        "document_id": data['document_id'],
        "date_emprunt": datetime.now(),
        "date_retour_prevu": data['date_retour_prevu'],
        "statut": statut,  # Update the status
    }

    mongo.db.emprunts.update_one({"_id": ObjectId(id)}, {"$set": updated_emprunt})
    return {"message": "Emprunt mis à jour avec succès!"}