import json

from flask_cors import CORS, cross_origin
from flask import jsonify, Flask, request, url_for, render_template, Blueprint
from flask_login import login_required
from requests import auth

from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash

from Robots import bot
from Utilisateurs import user
from bbd import selectAllUsers, selectAllRobots, selectById, selectByMatricule, updatebot, select_bot_id, mycursor, \
    returnIdByMaticule

#######################
app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/login', methods=['POST'])
def login_post():
    global reponse
    oReponse = []
    oUser = []
    datas = request.get_json()
    for data in datas['login']:
        oUser.append(data)

    if not user(oUser):
        reponse = json.dumps({'success': 400, 'user': 'erreur mot de passe ou utilisateur inconnu'})
    else:
        reponse = json.dumps({'success': 200, 'user': ' utilisateur authentifié'})

    oReponse.append(reponse)
    return jsonify(oReponse)


####################------INSERT
@app.route('/register', methods=['POST'])
def create_user():
    global reponse
    oReponse = []
    try:
        if request.method == 'POST':
            # declatation de la variable tableau pour executer append
            oUser = []
            # recuperation des donnees json {"user":["sylvain","JOLY","s44854","jskdhflq@lsqjd.fr", 0, 1,1]}
            datas = request.get_json()
            # lecture du json pour recuperation en tableau via append
            for data in datas['user']:
                oUser.append(data)  # ['sylvain', 'JOLY', 's44854', 'jskdhflq@lsqjd.fr', 0, 1, 1]
            if not user(oUser):
                reponse = json.dumps({'success': 400, 'user': 'non enregisté en base de donnée'})
            else:
                reponse = json.dumps({'success': 200, 'user': ' l\'utilisateur à bien ete enregisté'})
    except Exception as e:
        return json.dumps({'success': False, 'message': 'une erreur inconnu est survenue', 'type':
            str(e) + 'api/ createBot'})
    oReponse.append(reponse)
    return jsonify(oReponse)


@app.route('/user/create_bot', methods=['POST'])
def create_bot():
    global reponse
    oReponse = []
    try:
        if request.method == 'POST':
            # declaration de la variable tableau pour executer append
            oBot = []
            # recuperation des donnees json {"bot":["nono",id_user,0,1,1]}
            datas = request.get_json()
            # lecture du json pour recuperation en tableau via append
            for data in datas['bot']:
                oBot.append(data)  # ['nono', 'id_user', 0, 1, 1]

            if not bot(oBot):
                reponse = json.dumps({'success': 400, 'bot': 'non enregisté en base de donnée'})
            else:
                reponse = json.dumps({'success': 200, 'bot': ' le robot à bien ete enregisté'})
    except Exception as e:
        return json.dumps({'success': False, 'message': 'une erreur inconnu est survenue', 'type':
            str(e) + 'api/ createBot'})
    oReponse.append(reponse)

    return jsonify(oReponse)


####################------AFFICHAGE
@app.route('/user/users', methods=['GET'])
def utilisateurs():
    try:
        datas = []
        # recuperation des users en bdd
        oUsers = selectAllUsers()
        if not oUsers:
            return jsonify({'users': 'aucun utilisateur enregistre'})
        else:
            datas.append(oUsers)
            for u in oUsers:
                username = u[1]
                print(username)
        # recuperation des robots en bdd
        oBot = selectAllRobots()
        if oBot:
            datas.append(oBot)
    except Exception as e:
        return json.dumps({'success': False, 'message': 'une erreur inconnu est survenue', 'type':
            str(e) + 'api/ Utilisateurs'})

    return jsonify({'datas': datas}), 200


@app.route('/user/mat/<matricule>', methods=['GET'])
def toto(matricule):
    print(matricule)
    oUser = selectByMatricule(matricule)
    print(oUser)

    return jsonify({'users': oUser})


@app.route('/user/user/<current_id>', methods=['GET'])
def user_id(current_id):
    user = selectById(current_id)

    return jsonify({'user': user})


@app.route('/user/bot/<current_id>', methods=['GET'])
def bot_id(current_id):
    user = selectById(current_id)

    return jsonify({'user': user})


####################------DELETE
@app.route('/user/bot/delete/<current_id>', methods=['GET'])
def delete_bot_id(current_id):
    # mettre en place une condition pour que la suppression du bot
    # se fasse que pas le créateur ou le supervisor
    user = selectById(current_id)
    return jsonify({'user': user})


@app.route('/user/<matricule>/delete/<current_id>', methods=['DELETE'])
def delete_user_id(current_id, matricule):
    print(matricule)
    search_user_id = returnIdByMaticule(matricule)
    print(search_user_id)
    if search_user_id == current_id:
        print("totot")
    else :
        print("vous n avez pas les droits")
    # mettre en place une condition pour que la suppression de l'user
    # se fasse que pas le créateur ou le supervisor
    user = selectById(current_id)
    return jsonify({'user': user})


####################------UPDATE
@app.route('/user/<matricule>/update/<current_id>', methods=['GET', 'POST'])
def update_user_id(current_id, matricule):
    # mettre en place une condition pour que lles modif du bot
    # se fasse que pas le créateur ou le supervisor
    # {"usermodif":["sylvain","M@ldeojo", "JOLY","s44854","sjoly@macif.fr", 0, 1,1]}
    global userId
    global reponse
    oReponse = []
    oUser = []
    try:
        if request.method == 'GET':
            userId = selectById(current_id)
            reponse = json.dumps({'user': str(userId)})
        if request.method == 'POST':  # and user_connect = user_creator_id
            # mettre un contraint pour modif si user connect = créateur du bot
            datas = request.get_json()
            print(datas)
            for data in datas['usermodif']:
                # if datas[1] == user_id_connect:
                oUser.append(data)  # ['nono', 'id_user', 0, 1, 1]

            oUser.append(current_id)
            oUser.append(matricule)
            print(oUser)
            if not user(oUser):
                reponse = json.dumps({'success': 400, 'user': 'modification non enregisté en base de donnée'})
            else:
                reponse = json.dumps({'success': 200, 'user': ' les modification ont bien ete enregisté'})
    except Exception as e:
        return json.dumps({'success': False, 'message': 'une erreur inconnu est survenue', 'type':
            str(e) + 'api/ createBot'})
    oReponse.append(reponse)
    return jsonify(oReponse)


@app.route('/user/<matricule>/bot/update/<current_id>', methods=['GET', 'POST'])
def update_bot_id(current_id):
    # mettre en place une condition pour que lles modif du bot
    # se fasse que pas le créateur ou le supervisor
    global bot
    global reponse
    oReponse = []
    oBot = []
    try:
        if request.method == 'GET':
            bot = select_bot_id(current_id)
            reponse = json.dumps({'bot': str(bot)})
        if request.method == 'POST':  # and user_connect = user_creator_id
            # mettre un contraint pour modif si user connect = créateur du bot
            datas = request.get_json()
            print(datas)
            for data in datas['botmodif']:
                # if datas[1] == user_id_connect:
                oBot.append(data)  # ['nono', 'id_user', 0, 1, 1]
            oBot.append(current_id)
            print(oBot)
            if not bot(oBot):
                reponse = json.dumps({'success': 400, 'bot': 'modification non enregisté en base de donnée'})
            else:
                reponse = json.dumps({'success': 200, 'bot': ' les modification ont bien ete enregisté'})
    except Exception as e:
        return json.dumps({'success': False, 'message': 'une erreur inconnu est survenue', 'type':
            str(e) + 'api/ createBot'})
    oReponse.append(reponse)
    return jsonify(oReponse)


if __name__ == '__main__':
    app.run()
