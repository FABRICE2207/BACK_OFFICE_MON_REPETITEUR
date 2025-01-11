from flask import Flask, flash
from datetime import datetime
from email.policy import default
from flask import jsonify, request, redirect, url_for, render_template, flash
# from flask_login import login_required
from sqlalchemy import desc, or_, and_, func
from sqlalchemy.sql import text
from sqlalchemy.sql.sqltypes import *
from psycopg2 import errors
from .. import db
from . import dash
from src.models import *
# from src.auth import token_auth
import random, string, re
from werkzeug.utils import secure_filename
import os
import datetime
import time
from flask_login import login_user, login_required, current_user

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# Dashboard
@dash.route("/dashboard")
@login_required
def dashboard():
    # Pour compter les nombres
    count_vendeur = Vendeurs.query.count()
    count_arti_soumis = Articles.query.filter_by(statut="soumis").count()
    count_arti_valid  = Articles.query.filter_by(statut="validé").count()
    count_arti_annul = Articles.query.filter_by(statut="annulé").count()
    count_arti_pub = Articles.query.filter_by(statut="publié").count()
    return render_template('dashboard/dashboard.html', count_arti_annul=count_arti_annul, count_arti_valid=count_arti_valid, count_arti_soumis=count_arti_soumis, count_arti_pub=count_arti_pub, count_vendeur=count_vendeur, first_name=current_user.first_name, last_name=current_user.last_name)

# Articles
ROWS_PER_PAGE_ARTICLE = 5
@dash.route("/liste_articles")
# @login_required
def liste_articles():
    # datas = Articles.query.all()
    page = request.args.get('page', 1, type=int)
    datas = Articles.query.paginate(page=page, per_page=ROWS_PER_PAGE_ARTICLE)
    return render_template('dashboard/liste_article.html', datas=datas, first_name=current_user.first_name, last_name=current_user.last_name)

# Affiche un article dans le Pop-up
@dash.route('/get_article/<int:id>',methods=["POST", "GET"])
def get_article(id):
    if request.method == 'POST':
        id = request.form['id']
        get_article = Articles.query.get(id)
    return jsonify({'htmlresponse': render_template('dashboard/response.html', get_article=get_article)})

# Vendeurs
@dash.route("/liste_vendeurs")
# @login_required
def liste_vendeurs():
    datas = Vendeurs.query.all()
    return render_template('dashboard/liste_vendeurs.html', datas=datas, first_name=current_user.first_name, last_name=current_user.last_name)

# Profile
@dash.route("/profile")
# @login_required
def profile():
    # datas = Vendeurs.query.all()
    return render_template('dashboard/profile.html', first_name=current_user.first_name, last_name=current_user.last_name)

# Ajout article
@dash.route("/ajout_article", methods=['GET', 'POST'])
# @login_required
def ajout_article():
    if request.method == "GET":
        return render_template('dashboard/ajout_article.html', first_name=current_user.first_name, last_name=current_user.last_name)

    if request.method == "POST":
        nom = request.form['nom']
        code_bar = request.form['code_bar']
        prix = request.form['prix']
        cout_achat = request.form['nom']
        file_first = request.files['image_first']
        file_two = request.files['image_two']
        categories = request.form['categories']
        statut = request.form['statut']

        # Si la première image existe
        if file_first and allowed_file(file_first.filename):
            filename = secure_filename(file_first.filename)
            file_first.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            verif_file = db.session.query(Articles).filter(Articles.image_first == filename).first()
            if verif_file:
                flash("Désolé, l'article existe déjà")
                return redirect(url_for('dashboard.ajout_article'))

            filename_two = ""
            # Si la deuxième image existe
            if file_two and allowed_file(file_two.filename):
                filename_two = secure_filename(file_two.filename)
                file_two.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename_two))

                verif_file = db.session.query(Articles).filter(Articles.image_two == filename_two).first()
                if verif_file:
                    flash("Désolé, l'article existe déjà")
                    return redirect(url_for('dashboard.ajout_article'))
        else:
            flash("Désolé, la première image n'existe pas !")
            return redirect(url_for('dashboard.ajout_article'))

        articles = Articles(nom=nom, code_bar=code_bar, prix=prix, cout_achat=cout_achat, image_first=filename, image_two=filename_two, categories=categories, statut=statut)
        db.session.add(articles)
        db.session.commit()
        return redirect(url_for("dashboard.liste_articles"))
    
# Modification de l'article
@dash.route("/modif_article/<int:id>", methods=['GET', 'POST'])
def modif(id):
    article = Articles.query.filter_by(id=id).first()

    if request.method == 'POST':
        if article:
            db.session.delete(article)
            db.session.commit()

            image_first = request.files['image_first']
            image_two = request.files['image_two']
            
            if request.files.get('image_first'):
                # Supprimer une image dans le dossier
                os.unlink(os.path.join(current_app.config['UPLOAD_FOLDER'], article.image_first))

                # Remplacer l'ancienne par la nouvelle image
                filename = secure_filename(image_first.filename)
                image_first.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

                filename_two = ""
                if request.files.get('image_two'):
                    # Supprimer une image dans le dossier
                    os.unlink(os.path.join(current_app.config['UPLOAD_FOLDER'], article.image_two))

                    # Remplacer l'ancienne par la nouvelle image
                    filename_two = secure_filename(image_two.filename)
                    image_two.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename_two))

            else:
                flash("Désolé, la première image manque")
            
            nom = request.form['nom']
            code_bar = request.form['code_bar']
            prix = request.form['prix']
            cout_achat = request.form['cout_achat']
            article.image_first = filename
            article.image_first = filename_two
            categories = request.form['categories']
            statut = request.form['statut']

            article = Articles(id=id, nom=nom, code_bar=code_bar, prix=prix, cout_achat=cout_achat, image_first=filename, image_two=filename_two, categories=categories, statut=statut)

            db.session.add(article)
            db.session.commit()
            return redirect(url_for("dashboard.liste_articles"))
        
    return render_template('dashboard/modif_article.html', article=article, first_name=current_user.first_name, last_name=current_user.last_name)