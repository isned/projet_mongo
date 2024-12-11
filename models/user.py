class User:
    def __init__(self, email, password=None):
        self.email = email
        if password:
            self.password = password  
        else:
            self.password = None

    def check_password(self, password):
        """Check if the entered password matches the stored plain password."""
        if self.password:
            return self.password == password  
        return False

    @staticmethod
    def find_by_email(email, users_collection):
        """Recherche un utilisateur par email dans la collection."""
        user_data = users_collection.find_one({"email": email})
        if user_data:
            return User(email=user_data['email'], password=user_data['password'])
        return None

    def save_to_db(self, users_collection):
        """Enregistre l'utilisateur dans la base de données."""
        users_collection.insert_one({
            "email": self.email,
            "password": self.password  
        })