from datetime import datetime

from flask import jsonify

from bbd import createBot, updatebot


def bot(datas):
    try:
        if datas:
            if len(datas) == 5:
                botname = datas[0]
                now = datetime.now()
                dateCreate = now.strftime('%Y-%m-%d')
                usercrator = datas[1]
                # prise en charge des droits
                supervisor = datas[2]
                admin = datas[3]
                dev = datas[4]
                # envoy vers base de donnée
                createBot(botname, dateCreate, usercrator, supervisor, admin, dev)
            if len(datas) == 6:
                botname = datas[0]
                now = datetime.now()
                dateModification = now.strftime('%Y-%m-%d')
                # prise en charge des droits
                supervisor = datas[2]
                admin = datas[3]
                dev = datas[4]
                bot_id = datas[5]
                # envoy vers base de donnée
                if updatebot(botname, supervisor, admin, dev, bot_id, dateModification):
                    return True
                else:
                    return False
    except Exception as e:
        return jsonify({'result': 'un probleme est survenu'}), 400