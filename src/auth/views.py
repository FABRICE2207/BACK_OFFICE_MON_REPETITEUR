from flask import jsonify, request, redirect, url_for, render_template, flash
from .. import db, mail
from . import auth
from src.models import *
from flask_login import login_user, login_required, logout_user,  current_user

# Login 
@auth.route("/")
def index():
    return render_template('auth/login.html')

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# ------------ LOGIN ADMIN ----------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
        # return render_template('auth/login.html')

    if request.method == 'POST':
        email = request.form.get('email')
        password_hash = request.form.get('password_hash') 
        user = User.query.filter_by(email=email).first() # Vérifie si l'email existe dans la bd
        if not user or not check_password_hash(user.password_hash, password_hash): # Compare si le mdp saisie est égale a celui du mdp hashé dans la bd
            flash('Email ou mot de passe invalide !')
            return render_template('auth/login.html') # si user n'existe pas retourne sur le login
        login_user(user)
        return redirect(url_for("dashboard.dashboard")) # si user existe, retourne sur le dashboard
    
# Login repetieur
@auth.route('/login/repetiteur', methods=['POST'])
def login_repetiteur():
    if request.method == 'POST':
        contactWhats = request.json["contactWhats"]
        passwordR = request.json["passwordR"]
        repetiteur = Repetiteurs.query.filter_by(contactWhats=contactWhats).first()
        if not repetiteur or not check_password_hash(repetiteur.passwordR, passwordR):
            return jsonify({"Erreur": "Le contact ou le mot de passse est invailde"}), 401
        return jsonify({"Nom et prenom": repetiteur.nomcomplet, "Contact": repetiteur.contactWhats })