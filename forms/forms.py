from wtforms import StringField, PasswordField, SubmitField, TextAreaField, EmailField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = StringField(label='Nom d\'utilisateur', validators=[DataRequired(message='Le champs est requis')])
    password = PasswordField(label='Mot de passe', validators=[DataRequired(message='Le champs est requis')])
    submit = SubmitField('Se connecter')

class UserLoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(message='Le champs est requis')])
    password = PasswordField(label='Mot de passe', validators=[DataRequired(message='Le champs est requis')])
    submit = SubmitField('Se connecter')

class RegisterForm(FlaskForm):
    firstname = StringField(label='Prénom', validators=[DataRequired(message='Le champs est requis')])
    lastname = StringField(label='Nom', validators=[DataRequired(message='Le champs est requis')])
    email = EmailField(label='Email', validators=[DataRequired(message='Le champs est requis')])
    password = PasswordField(label='Mot de passe', validators=[DataRequired(message='Le champs est requis'),  EqualTo('confirm', message='Mot de passe non identique')])
    confirm = PasswordField(label='Confirmez le mot de passe :', validators=[DataRequired(message='Le champs est requis')] )
    submit = SubmitField('S\'inscrire')

class AdminForm(FlaskForm):
    username = StringField(label='Pseudo :', validators=[DataRequired(message='Le champs est requis')])
    password = PasswordField(label='Mot de passe :', validators=[DataRequired(message='Le champs est requis'), EqualTo('confirm', message='Mot de passe non identique')])
    confirm = PasswordField(label='Confirmez le mot de passe :', validators=[DataRequired(message='Le champs est requis')])
    submit = SubmitField('S\'inscrire')

class OfferForm(FlaskForm):
    title = StringField(label='Titre :', validators=[DataRequired(message='Le champs est requis')])
    description = TextAreaField(label='Description :', validators=[DataRequired(message='Le champs est requis')])
