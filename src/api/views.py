from datetime import datetime
from flask import jsonify, request, redirect, url_for, render_template
from sqlalchemy import desc, or_, and_, func
from sqlalchemy.sql import text
from sqlalchemy.sql.sqltypes import *
from psycopg2 import errors
from src import db
from src.models import *
# from src.auth import token_auth
import random, string, re
from . import api
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from flask_login import current_user

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def bad_request_func(msg):
    return jsonify({'type': 'error', 'message': msg}), 200

@api.route('/user/get')
def user():
    datas = User.query.all()
    return jsonify([item.to_dict() for item in datas])

@api.route('/user/add', methods=['POST'])
# @token_auth.login_required
def create_user():
    if request.method == 'POST':
        datas = request.get_json()
        user = User(datas)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Admin ajouté avec succès"})

@api.route('/user/update', methods=['POST'])
# @token_auth.login_required
def update_user():
    data = request.form.to_dict(flat=False) or {}
    user = User.query.get(data['id'])
    if not user:
        return bad_request_func('Entity not found')
    del data['id']
    user.from_dict(data, files=request.files, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())

@api.route('/user/delete', methods=['POST'])
# @token_auth.login_required
def delete_user():
    data = request.get_json() or {}
    user = User.query.get(data['id'])
    if user:
        db.session.delete(User)
        db.session.commit()
        return jsonify({'response': '{} ID::{} deleted'.format('user', user
            .id)})
    else:
        return bad_request_func('Entity not found')

@api.route('/usertype/get')
def usertype():
    datas = UserType.query.all()
    return jsonify([item.to_dict() for item in datas])

@api.route('/usertype/add', methods=['POST'])
# @token_auth.login_required
def create_usertype():
    if request.method == 'POST':
        datas = request.get_json() or {}
        usertype = UserType(code=datas["code"],title=datas["title"],description=datas["description"])
        db.session.add(usertype)
        db.session.commit()
        return jsonify({"message":"Usertype cree avec succes"})

@api.route('/usertype/update', methods=['POST'])
# @token_auth.login_required
def update_usertype():
    data = request.get_json() or {}
    usertype = UserType.query.get(data['id'])
    if not usertype:
        return bad_request_func('Entity not found')
    del data['id']
    usertype.from_dict(data)
    db.session.commit()
    return jsonify(usertype.to_dict())

@api.route('/usertype/delete', methods=['POST'])
# @token_auth.login_required
def delete_usertype():
    data = request.get_json() or {}
    usertype = UserType.query.get(data['id'])
    if usertype:
        db.session.delete(UserType)
        db.session.commit()
        return jsonify({'response': '{} ID::{} deleted'.format('usertype',
            usertype.id)})
    else:
        return bad_request_func('Entity not found')

@api.route('/rules/get')
def rules():
    datas = Rules.query.all()
    return jsonify([item.to_dict() for item in datas])

@api.route('/rules/add', methods=['POST'])
# @token_auth.login_required
def create_rules():
    if request.methods == 'POST':
        datas = request.form
        rules = Rules(datas)
        db.add(rules)
        db.commit()
        return redirect(url_for('rules'))

@api.route('/rules/update', methods=['POST'])
# @token_auth.login_required
def update_rules():
    data = request.form.to_dict(flat=False) or {}
    rules = Rules.query.get(data['id'])
    if not rules:
        return bad_request_func('Entity not found')
    del data['id']
    rules.from_dict(data, files=request.files, new_rules=False)
    db.session.commit()
    return jsonify(rules.to_dict())

@api.route('/rules/delete', methods=['POST'])
# @token_auth.login_required
def delete_rules():
    data = request.get_json() or {}
    rules = Rules.query.get(data['id'])
    if rules:
        db.session.delete(Rules)
        db.session.commit()
        return jsonify({'response': '{} ID::{} deleted'.format('rules',
            rules.id)})
    else:
        return bad_request_func('Entity not found')

@api.route('/features/get')
def features():
    datas = Features.query.all()
    return jsonify([item.to_dict() for item in datas])

@api.route('/features/add', methods=['POST'])
# @token_auth.login_required
def create_features():
    if request.methods == 'POST':
        datas = request.form
        features = Features(datas)
        db.add(features)
        db.commit()
        return redirect(url_for('features'))


@api.route('/features/update', methods=['POST'])
# @token_auth.login_required
def update_features():
    data = request.form.to_dict(flat=False) or {}
    features = Features.query.get(data['id'])
    if not features:
        return bad_request_func('Entity not found')
    del data['id']
    features.from_dict(data, files=request.files, new_features=False)
    db.session.commit()
    return jsonify(features.to_dict())

@api.route('/features/delete', methods=['POST'])
# @token_auth.login_required
def delete_features():
    data = request.get_json() or {}
    features = Features.query.get(data['id'])
    if features:
        db.session.delete(Features)
        db.session.commit()
        return jsonify({'response': '{} ID::{} deleted'.format('features',
            features.id)})
    else:
        return bad_request_func('Entity not found')

# ---------- REPETITEUR -----------------
@api.route('/repetiteurs/create', methods=['POST'])
# @token_auth.login_required
def create_repetiteurs():
    if request.method == 'POST':
        datas = request.get_json()
        # image = request.files["data.image"]
        # filename = secure_filename(image.filename)
        # image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        # if image:
        #     verif_file = db.session.query(Repetiteurs).filter(Repetiteurs.image == filename).first()
        #     if verif_file:
        #         return jsonify({"message": "Désolé, l'article existe déjà"})
        # else:
        #     return jsonify({"Message": "Désolé, l'image n'existe pas !"})

        # print(data[nomcomplet])
        repetiteur = Repetiteurs(datas) 
        db.session.add(repetiteur)
        db.session.commit()
        return jsonify({"message": "Un répétietur a été ajouté avec succès"}, 201)
        
@api.route('/repetiteurs/getAll')
def getAll_repetiteurs():
    datas = Repetiteurs.query.all()
    return jsonify([item.to_dict() for item in datas])

# Afficher un repetiteur via son id
@api.route('/get_repetiteur/<int:id>',methods=['GET'])
def get_repetiteur(id): 
    data = Repetiteurs.query.get(id)
    if data:
        return jsonify(data.to_dict())
    return jsonify({'message': 'Aucun résultat trouvé !'})


# login repetiteur
@api.route('/login/repetiteur', methods=['POST'])
def login_repetiteur():
    if request.method == 'POST':
        contactWhats = request.get_json().get("contactWhats")
        passwordR = request.get_json().get("passwordR")
        repetiteur = Repetiteurs.query.filter_by(contactWhats=contactWhats).first()
        if not repetiteur or not check_password_hash(repetiteur.passwordR, passwordR):
            return jsonify("Le contact ou le mot de passse est invailde")

        #  Générer le token
        access_token = create_access_token(identity=repetiteur.id)
        # refresh_token = create_refresh_token(identity=repetiteur.nomcomplet)

        # Save the token to the database
        # new_token = Token(token=access_token)
        # db.session.add(new_token)
        # db.session.commit()

        return jsonify({
            #  "nomcomplet": repetiteur.nomcomplet,
            #  "email": repetiteur.email,
            #  "contactWhats": repetiteur.contactWhats,
            #  "lieu": repetiteur.lieu,
            #  "classPrim": repetiteur.classPrim,
            #  "classSecond": repetiteur.classSecond,
            #  "image": repetiteur.image,
            #  "passwordR": repetiteur.passwordR,
             "token": {
                 "access":access_token
                #  "refresh": refresh_token
             },
               }), 201

# Obtenir les infos du repetiteur via le token
@api.route('/getDataToken', methods=['GET'])
@jwt_required()
def getDataToken():
    current_user = get_jwt_identity()
    user_data = Repetiteurs.query.get(current_user)
    # return jsonify(data=user_data.to_dict()), 200
    return jsonify({
        "nomcomplet": user_data.nomcomplet,
        "email": user_data.email,
        "contactWhats": user_data.contactWhats,
        "lieu": user_data.lieu,
        "quartHab": user_data.quartHab,
        "classPrim": user_data.classPrim,
        "classSecond": user_data.classSecond,
        "annExp": user_data.annExp,
        "nivEtud": user_data.nivEtud,
        "image": user_data.image,
        "passwordR": user_data.passwordR
    }), 200

# Rechercher un repetiteur à partir d'un texte
@api.route('/search_repetiteur',methods=['GET'])
def get_search(): 
    name_filter = request.args.get("lieu")
    rep_query = Repetiteurs.query

    if rep_query:
        rep_query = rep_query.filter(Repetiteurs.lieu.like(f"%{name_filter}%"))
        repetiteur = rep_query.all()
        return jsonify([item.to_dict() for item in repetiteur])
    return jsonify({'message': 'Aucun résultat trouvé !'})
    # if data:
    #     return jsonify(data.to_dict())
    # return jsonify({'message': 'Aucun résultat trouvé !'})

# Modifications update
# @api.route('/repetiteurs/update/<int:id>', methods=['POST'])
# def update_repetiteurs(id):   
#     data = request.get_json()
#     repetiteurs = Repetiteurs.query.filter_by(id=id).first()
#     repetiteurs.from_dict(data)
#     db.session.commit()
#     return jsonify({
#         'nom': vendeurs.nom,
#         'email': vendeurs.email,
#         'nom_vend': vendeurs.nom_vend,
#         'telephone': vendeurs.telephone,
#         'adresse': vendeurs.adresse,
#     })

# Suppression du vendeurs
# @api.route('/vendeurs/delete/<int:id>', methods=['GET'])
# def delete_vendeurs(id):
#     vendeurs = db.session.query(Vendeurs).filter(Vendeurs.id == id).first()
#     db.session.delete(vendeurs)
#     db.session.commit()
#     return jsonify({"message": "Vendeurs supprimé avec succès"})

# ---------- Article -----------------
# @api.route('/article/add', methods=['POST'])
# # @token_auth.login_required
# def create_article():
#     if request.method == 'POST':
#         nom = request.form['nom']
#         prix = request.form['prix']
#         code_bar = request.form['code_bar']
#         cout_achat = request.form['cout_achat']
#         file_first = request.files['image_first']
#         file_two = request.files['image_two']
#         categories = request.form['categories']
#         statut = request.form['statut']

#         # Si la première image existe
#         if file_first and allowed_file(file_first.filename):
#             filename = secure_filename(file_first.filename)
#             file_first.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

#             verif_file = db.session.query(Articles).filter(Articles.image_first == filename).first()
#             if verif_file:
#                     return jsonify({"message": "Désolé, l'article existe déjà"})

#             filename_two = ""
#             # Si la deuxième image existe
#             if file_two and allowed_file(file_two.filename):
#                 filename_two = secure_filename(file_two.filename)
#                 file_two.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename_two))

#                 verif_file = db.session.query(Articles).filter(Articles.image_two == filename_two).first()
#                 if verif_file:
#                     return jsonify({"message": "Désolé, l'article existe déjà"})
#         else:
#             return jsonify({"Message": "Désolé, la première image n'existe pas !"})
        
#         # Enregistrement des données dans la BD
#         article = Articles(nom=nom, prix=prix, code_bar=code_bar, cout_achat=cout_achat, image_first=filename, image_two=filename_two, categories=categories, statut=statut)
#         db.session.add(article)
#         db.session.commit()
#         return jsonify({"message": "Un article a été ajouté avec succès"})
#         datas = request.get_json()
#         article = Articles(datas)
#         db.session.add(article)
#         db.session.commit()
#         return jsonify({"message": "Un artcle a été ajouté avec succès"})

# # Afficher la liste des artciles
# @api.route('/article/getAll')
# def getAll_article():
#     datas = Articles.query.all()
#     return jsonify([item.to_dict() for item in datas])

# # Afficher un artcile via son id
# @api.route('/get_article/<int:id>',methods=['POST', 'GET'])
# def get_article(id):
#     data = Articles.query.get(id)
#     if data:
#         return jsonify(data.to_dict())
#     return jsonify({'message': 'Aucun résultat trouvé !'})
    
# # Modifications artciles
# @api.route('/article/update/<int:id>', methods=['POST'])
# def update_article(id):
#     if request.method == "POST":
#         article = Articles.query.get_or_404(id)
#         if request.method == "POST":
#             image_first = request.files['image_first']
#             image_two = request.files['image_two']
            
#             if request.files.get('image_first'):
#                 # Supprimer une image dans le dossier
#                 os.unlink(os.path.join(current_app.config['UPLOAD_FOLDER'], article.image_first))

#                 # Remplacer l'ancienne par la nouvelle image
#                 filename = secure_filename(image_first.filename)
#                 image_first.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

#                 filename_two = ""
#                 if request.files.get('image_two'):
#                     # Supprimer une image dans le dossier
#                     os.unlink(os.path.join(current_app.config['UPLOAD_FOLDER'], article.image_two))

#                     # Remplacer l'ancienne par la nouvelle image
#                     filename_two = secure_filename(image_two.filename)
#                     image_two.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename_two))

#             else:
#                 return jsonify({"Message": "Désolé, la première image manque"})
            
#             article.nom = request.form.get('nom')
#             article.prix = request.form.get('prix')
#             article.code_bar = request.form.get('code_bar')
#             article.cout_achat = request.form.get('cout_achat')
#             article.image_first = filename
#             article.image_two = filename_two
#             article.categories = request.form.get('categories')
#             article.statut = request.form.get('statut')
#             db.session.commit()
#             return jsonify({
#             "Nom": article.nom,
#             "Prix": article.prix,
#             "Image_first": article.image_first,
#             "Code barre": article.code_bar,
#             "Image_first": article.image_first,
#             "Image_two": article.image_two,
#             "categories": article.categories,
#             "Statut": article.statut
#             })
        
# # Modification du status après le clic du btn Publié
# @api.route('/update_status_publie/<int:id>', methods=['POST'])
# def update_status_publie(id):
#     data = request.get_json()
#     new_statut = data.get('newStatut')

#     change_status = Articles.query.get(id)
#     if change_status:
#         change_status.statut = new_statut
#         db.session.commit()
#         return jsonify(success=True, newStatut=new_statut)
#     return jsonify(success=False)

# # Modification du status après le clic du btn Réfusé
# @api.route('/update_status_refuse/<int:id>', methods=['POST'])
# def update_status_refuse(id):
#     data = request.get_json()
#     new_statut = data.get('newStatut')

#     change_status = Articles.query.get(id)
#     if change_status:
#         change_status.statut = new_statut
#         db.session.commit()
#         return jsonify(success=True, newStatut=new_statut)
#     return jsonify(success=False)

# # Suppression du vendeurs
# @api.route('/article/delete/<int:id>', methods=['GET'])
# def delete_article(id):
#     # article = db.session.query(Articles).filter(Articles.id == id).first()
#     # db.session.delete(article)
#     # db.session.commit()
#     # Suppression d'informations du plats et de l'image
#     article = Articles.query.get_or_404(id)
#     try:
#         os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], article.image_first))
#         db.session.delete(article)
#     except:
#         db.session.delete(article)
#     db.session.commit()
#     return jsonify({"message": "Article supprimé avec succès"})

# ---------- PARENTS -----------------
@api.route('/parents/create', methods=['POST'])
# @token_auth.login_required
def create_parents():
    if request.method == 'POST':
        datas = request.get_json()
        parents = Parents(datas) 
        db.session.add(parents)
        db.session.commit()
        return jsonify({"message": "Un parent a été ajouté avec succès"}, 200)
    
# Affiche la liste des parents
@api.route('/parents/getAll')
def getAll_parents():
    datas = Parents.query.all()
    return jsonify([item.to_dict() for item in datas])

# Afficher un parent via son id
@api.route('/get_parent/<int:id>',methods=['GET'])
def get_parent(id): 
    data = Parents.query.get(id)
    if data:
        return jsonify(data.to_dict())
    return jsonify({'message': 'Aucun résultat trouvé !'})

# login parents
@api.route('/login/parent', methods=['POST'])
def login_parent():
    if request.method == 'POST':
        telephone = request.get_json().get("telephone")
        password_hash = request.get_json().get("password_hash")
        parent = Parents.query.filter_by(telephone=telephone).first()
        if not parent or not check_password_hash(parent.password_hash, password_hash):
            return jsonify("Le contact ou le mot de passse est invailde")

        #  Générer le token
        access_token = create_access_token(identity=parent.id)

        return jsonify({
            "token": { "access":access_token },
               }), 201

# Obtenir les infos du parent via le token
@api.route('/getDataTokenParent', methods=['GET'])
@jwt_required()
def getDataTokenParent():
    current_user = get_jwt_identity()
    user_data = Parents.query.get(current_user)
    # return jsonify(data=user_data.to_dict()), 200
    return jsonify({
        "nomcomplet_parent": user_data.nomcomplet_parent,
        "telephone": user_data.telephone,
        "lieu": user_data.lieu,
        "quartHab": user_data.quartHab,
        "password_hash": user_data.password_hash
    }), 200
