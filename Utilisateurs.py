from datetime import datetime
import hashlib

from flask import jsonify

from bbd import createUser, selectByMatricule, selectByMatriculeForlogin, updateuser


def user(datas):
    try:
        if len(datas) == 8:
            print('good')
            username = datas[0]
            lastname = datas[1]
            mdp = datas[2]
            p = hashlib.md5(mdp.encode())
            password = p.hexdigest()
            matricule = datas[3]
            mail = datas[4]
            now = datetime.now()
            dateCreate = now.strftime('%Y-%m-%d')
            supervisor = datas[5]
            admin = datas[6]
            dev = datas[7]
            createUser(username, lastname, password, matricule, mail,
                       dateCreate, supervisor, admin, dev)
            return True

        if len(datas) == 2:
            matricule = datas[0]
            mdp = datas[1]
            p = hashlib.md5(mdp.encode())
            loginPassword = p.hexdigest()
            if not selectByMatriculeForlogin(matricule, loginPassword):
                return False
            return True

        if len(datas) == 9:
            username = datas[0]
            lastname = datas[1]
            mdp = datas[2]
            p = hashlib.md5(mdp.encode())
            password = p.hexdigest()
            now = datetime.now()
            dateModifuser = now.strftime('%Y-%m-%d')
            mail = datas[3]
            supervisor = datas[4]
            admin = datas[5]
            dev = datas[6]
            userid = datas[7]
            if not updateuser(username, lastname, password, mail, dateModifuser, supervisor,
                       admin, dev, userid):
                return False
            return True
        else:
            return False
    except:
        return jsonify({'result': 'un probleme est survenu api/Utilisateur'}), 400
