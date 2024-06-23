from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from forms.forms import LoginForm, RegisterForm, AdminForm, OfferForm, UserLoginForm
from flask_hashing import Hashing
from functools import wraps
import uuid, random, segno, os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ucmdr9svikk09u:p6bbe7b97c0c4d57bea5a20829f9199e99f1ae7823921e178f56f1ab8e2d9a55f@cav8p52l9arddb.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d7dlbls6hnsghl"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['WTF_CSRF_SECRET_KEY '] = 'UzZnVa8nMk1KDuXL7SDccO9f0aRV89cf'
app.secret_key = 'UzZnVa8nMk1KDuXL7SDccO9f0aRV89cf'

hashing = Hashing(app)

db = SQLAlchemy(app)

# Importation des modèles Flask et la base de données SQLAlchemy
from .models.models import Admin, User, Ebillet, Offer

with app.app_context():
    db.create_all()


#decorators
# ici il s'agit d'un décorateur souvent utilisé dans  flask, c'est une fonction qui est exécuter avant la fonction de la route et elle permet de vérifier si l'utilisateur User est connecter
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# ici meme schéma que celui du dessus mais pour les utilisateur Admin
def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('admin_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


#template filters
#fonction qui sera utilisé dans les templates
@app.template_filter('length')
def get_length(arr):
    return len(arr)


# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')



@app.route('/offers')
def offers():
    # Définition des offres
    offers_data = Offer.query.all()
    return render_template('offers.html', offers_data=offers_data)


# Page de panier
@app.route('/cart')
def cart():
    # Si le panier existe dans la session
    if 'cart' not in session:
        session['cart'] = []

    # Récupérez le panier de la session
    cart_offers = session['cart']
    cart_details = []

    for offer_id in cart_offers:
        # Récupérez les détails de l'offre à partir des données de produits
        offer_details = Offer.query.get(offer_id)
        if offer_details:
            cart_details.append(offer_details)

    return render_template('cart.html', carts=cart_details)


# Route pour mettre à jour le panier
@app.route('/update_cart', methods=['POST'])
def update_cart():
    data = request.get_json()
    success = False
    # Vérification des données JSON contiennent la clé 'action'
    if 'action' not in data:
        return jsonify({'message': 'Action non spécifiée dans les données JSON'}), 400

    action = data.get('action')
    cart = session.get('cart')

    # Vérifie si cart est None, initialise la liste vide si c'est le cas
    if cart is None:
        cart = []

    if action == 'add':
        # Ajouter une offre au panier
        offer_id = int(data.get('offer_id'))
        # vérifie si l'offre existe déjà dans le panier
        if offer_id in cart:
            return jsonify({'success': False, 'message': 'Offre déjà présente dans le panier!'})

        cart.append(offer_id)
        success = True
        message = "L'offre a été ajoutée au panier!"

    elif action == 'remove':
        # Supprimer une offre du panier
        offer_id = int(data.get('offer_id'))

        if offer_id in cart:
            cart.remove(offer_id)
            success = True
            message = f"L'offre a été supprimée du panier!"
        else:
            message = f"L'offre n'a pas été trouvée dans le panier."
    else:
        return jsonify({'success': success, 'message': 'Action non reconnue.'}), 400

    # Mettre à jour le panier dans la session
    session['cart'] = cart
    return jsonify({'success': success, 'message': message})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user') and session.get('is_admin') == False:
        return redirect(url_for('offers'))
    
    form = UserLoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        # Recherchez l'utilisateur dans la base de données
        user = User.query.filter_by(email=form.email.data).first()

        if user and hashing.check_value(user.password, form.password.data, salt=app.config['SECRET_KEY']):
            # Si l'utilisateur existe et le mot de passe correspond, connectez-le
            session['user'] = user.id
            session["is_admin"] = False
            flash('Connexion réussie!', 'success')
            if request.args.get('next'):
                return redirect(request.args.get('next'))
            # Redirigez l'utilisateur vers la page de paiement après connexion réussie
            return redirect(url_for('offers'))
        else:
            flash('Échec de la connexion. Vérifiez votre nom d\'utilisateur et votre mot de passe.', 'danger')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user') and session.get('is_admin') == False:
        return redirect(url_for('offers'))
    
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        exist_user = User.query.filter_by(email=form.email.data).all()
        if len(exist_user) == 0:
            # Créer une instance de l'utilisateur avec les données du formulaire
            new_user = User(
                firstname=form.firstname.data,
                lastname=form.lastname.data,
                email=form.email.data,
                password=hashing.hash_value(form.password.data, salt=app.config['SECRET_KEY']),
                username=f'{form.firstname.data.strip()}{form.lastname.data.strip()}',
                code= uuid.uuid4(),
            )
            # Ajouter l'utilisateur à la session de base de données
            db.session.add(new_user)

            # Valider les changements
            db.session.commit()

            flash('utilisateur inscris avec succès', 'success')
            # Rediriger vers la page de connexion après l'inscription
            return redirect(url_for('login'))
        else:
            flash('Email déjà utiliser!', 'danger')

    # Afficher le formulaire d'inscription
    return render_template('register.html', form=form)



@app.route('/checkout')
@login_required
def checkout():
    # Vérifier si l'utilisateur est connecté
    if 'user' not in session:
        # Rediriger l'utilisateur vers la page de connexion s'il n'est pas connecté
        return redirect(url_for('login'))

    # renvoie la page check out avec un prix fictif qui ne sera pas stocker ni enregistrer avec un bouton payer pour passer au prochain étape
    return render_template('checkout.html')


def generate_random_key(length=8, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXZabcdefghijklmnopqrstuvwxyz1234567890'):
    result = ''
    for i in range(length):
        result += random.choices(allowed_chars)[0]
    return result

def generate_qrcode(data, offer_code):
    # Générer un code QR factice avec les données fournies
    qrcode = segno.make_qr(data)
    filename = f'{offer_code}.png'
    filepath = os.path.join(os.path.dirname(__file__), 'static', 'qrcode', filename)
    qrcode.save(
        filepath,
        scale=10,
        border=2,
    )
    return filename


@app.route('/confirmation')
@login_required
def confirmation():
    if 'user' not in session:
        # Redirigez l'utilisateur vers la page de connexion s'il n'est pas connecté
        return redirect(url_for('login'))
    
    # Récupérer des infos de la session puis génération du qrcode
    # control du type d'uilisateur
    if session.get('is_admin') == True:
        flash('Vous ne possedez pas les droit pour effectuer une telle action', 'danger')
        return redirect(url_for('admin_dashboard')) 
    
    user = User.query.get(session.get('user'))

    if not session['cart'] or len(session['cart']) <= 0:
        flash('Cette session a expiré', 'danger')
        return redirect(url_for('offers'))

    cart_offers = session['cart']

    # recuperation des info de l'offre
    offer_details = Offer.query.get(cart_offers[0])
    # génerer le qrcode
    qrcode_filename = generate_qrcode(f'{user.code}.{offer_details.code}', offer_details.code)

    if len(qrcode_filename) > 0:
        session['cart'] = None
        #Enregistrement de l'e-billet
        ebillet = Ebillet(user_id=user.id, offer_id=offer_details.id, final_key=f'{user.code}.{offer_details.code}')
        db.session.add(ebillet)
        db.session.commit()

    # flash('Qrcode générer avec succès!', 'success')
    
    # Afficher la page de confirmation avec les détails de la commande
    return render_template('confirmation.html', qrcode_filename=qrcode_filename)


# Page d'administration
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('user') and session.get('is_admin') == True:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm(request.form)
    if request.method == 'POST':
        # Logique de vérification des informations de connexion admin
        if form.validate_on_submit():
            admin = Admin.query.filter_by(username=form.username.data).first()
            if admin and admin.password:
                if hashing.check_value(admin.password, form.password.data, salt=app.config['SECRET_KEY']):
                    session["user"] = admin.id
                    session["is_admin"] = True
                    if request.args.get('next'):
                        return redirect(request.args.get('next'))
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Échec de la connexion admin. Vérifiez votre nom d\'utilisateur et votre mot de passe.', 'danger')
            else:
                flash('Une erreur s\'est produite veuillez réessayer plus tard', 'danger')
        else:
            flash('Échec de la connexion admin. Vérifiez votre nom d\'utilisateur et votre mot de passe.', 'danger')            

    return render_template('admin_login.html', form=form)


# register
@app.route('/admin/register',  methods=['GET', 'POST'])
def admin_register():
    if session.get('user') and session.get('is_admin') == True:
        return redirect(url_for('admin_dashboard'))
    
    form = AdminForm(request.form)
    if request.method == 'POST':
        # Logique de vérification des informations de connexion admin
        if form.validate_on_submit():
            exist_username = Admin.query.filter_by(username=form.username.data).all()
            if len(exist_username) == 0:
                new_admin = Admin(username=form.username.data, password=hashing.hash_value(form.password.data, salt=app.config['SECRET_KEY']))
                db.session.add(new_admin)
                db.session.commit()
                flash('Inscription admin réussie!', 'success')
                return redirect(url_for('admin_login'))
            else:
                flash('Pseudo déjà utilisé.', 'danger')
        else:
            flash('Échec de la connexion admin. Vérifiez votre nom d\'utilisateur et votre mot de passe.', 'danger')

    return render_template('admin_register.html', form=form)


# Route pour vérifier les codes 
@app.route('/scan', methods=['POST'])
@admin_login_required
def scan_qrcode():
    data = request.get_json()
    success = False

    # Vérification des données JSON contiennent la clé 'action'
    if 'code' not in data:
        return jsonify({'message': 'Action non spécifiée dans les données JSON'}), 400

    # récupérer le ebillet
    ebillet = Ebillet.query.filter_by(final_key=data['code']).first()
    user = None
    offer = None
    if ebillet and ebillet.status:
        user = User.query.get(ebillet.user_id)
        offer = Offer.query.get(ebillet.offer_id)
        # modification du status
        ebillet.status = 'valider'
        db.session.add(ebillet)
        db.session.commit()
        success = True
    else:
        return jsonify({'success': success, 'message': 'Ebillet non valide!'}), 400

    return jsonify({'success': success, 'message': f'Ebillet de {user.lastname} {user.firstname} pour l\'offre {offer.title} est validé!'})


# afficher le tableau de bord admin
@app.route('/admin/dashboard')
@admin_login_required
def admin_dashboard():
    # Logique pour vérifier si l'administrateur est connecté, généralement gérée par un système de session
    user_list = User.query.all()
    offers_list = Offer.query.all()
    print(offers_list)
    # Si l'administrateur est connecté, rend la page du tableau de bord admin
    return render_template('admin_dashboard.html', user_list=user_list, user_list_count=len(user_list),  offers_list=offers_list, offers_list_count=len(offers_list))


@app.route('/admin/add_offer', methods=['GET', 'POST'])
@admin_login_required
def admin_add_offer():
    form = OfferForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            exist_offer = Offer.query.filter_by(title=form.title.data).all()
            if len(exist_offer) == 0:
                new_offer = Offer(title=form.title.data, description=form.description.data, code=generate_random_key())
                db.session.add(new_offer)
                db.session.commit()
                flash('Ajouter avec succès!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Offre déjà existant!', 'danger')
        else:
            flash('Vérifiez vos champs puis réessayer', 'danger')
    
    return render_template('admin_add_offer.html', form=form)  # Afficher le formulaire d'ajout d'offre



@app.route('/admin/edit_offer', methods=['GET', 'POST'])
@admin_login_required
def admin_edit_offer():
    if not request.args.get('id'):
        return redirect(url_for('admin_dashboard')) 
    
    offer = Offer.query.get(int(request.args.get('id')))

    if not offer:
        flash('l\'offre n\'existe pas!', 'danger')
        return redirect(url_for('admin_dashboard')) 
    
    form = OfferForm(title=offer.title, description=offer.description)
    if request.method == 'POST':
        if form.validate_on_submit():
            offer.title = form.title.data
            offer.description = form.description.data
            db.session.add(offer)
            db.session.commit()
            flash('Modifier avec succès!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Offre déjà existant!', 'danger')
        return redirect(url_for('admin_dashboard'))  # Redirection vers le tableau de bord admin après l'édition de l'offre
        # Logique pour afficher le formulaire d'édition d'offre
    return render_template('admin_edit_offer.html', form=form)  # Affichage du formulaire d'édition d'offre



@app.route('/admin/delete_offer', methods=['GET', 'POST'])
@admin_login_required
def admin_delete_offer():
    if not request.args.get('id'):
        return redirect(url_for('admin_dashboard')) 
    
    offer = Offer.query.get(int(request.args.get('id')))

    if not offer:
        flash('l\'offre n\'existe pas!', 'danger')
        return redirect(url_for('admin_dashboard')) 
    if request.method == 'POST':
        if int(request.form['offer_id']) == offer.id:
            db.session.delete(offer)
            db.session.commit()
            flash('Supprimer avec succès!', 'success')
            return redirect(url_for('admin_dashboard'))  # Redirigez vers le tableau de bord admin
    
    return render_template('admin_delete_offer.html', offer=offer)  # Affichage du formulaire d'édition d'offre


@app.route('/admin/scan_ebillet')
@admin_login_required
def scan_ebillet():
    return render_template('scan_ebillet.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('is_admin', None)
    # déconnexion
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()

