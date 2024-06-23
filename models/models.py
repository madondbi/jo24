#from flask_sqlalchemy import SQLAlchemy
from app import db



# Définition du modèle User
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    selected_offer = db.Column(db.String(50))
    # selon l'énoncer il faut le champs pour enrgistrer le code de l'utilisateur
    code = db.Column(db.String(120), nullable=False)


    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}', '{self.selected_offer}', '{self.code}')"



class Offer(db.Model):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    # selon l'énoncer il faut le champs pour enrgistrer le code de l'offre
    code = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)


    def __repr__(self):
        return f"Offer('{self.title}', '{self.description}')"



# Définition du modèle Admin
class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Admin(username='{self.username}')"


# Définition du modèle Ebillet
class Ebillet(db.Model):
    __tablename__ = 'ebillets'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    offer_id = db.Column(db.Integer, db.ForeignKey('offers.id'), nullable=False)
    final_key = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), default='non authentique')

    # Relation avec le modèle User
    user = db.relationship('User', backref=db.backref('ebillets', lazy=True))

    # Relation avec le modèle Offer
    offer = db.relationship('Offer', backref=db.backref('ebillets', lazy=True))

    def __repr__(self):
        return f"Ebillet(user_id='{self.user_id}', offer_id='{self.offer_id}', status='{self.status}')"
