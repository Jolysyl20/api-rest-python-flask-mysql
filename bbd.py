import mysql.connector
from flask import jsonify

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gestion_utilisateurs"
)
mycursor = mydb.cursor()

####################____________METHODES SQL

####################____________USERS
SELECT_ALL_USERS = 'SELECT * FROM USERS INNER JOIN rights ON users.id = rights.user_id'
SELECT_MATRICULE = "SELECT id FROM USERS WHERE MATRICULE ="
SELECT_MATRICULE_FOR_LOGIN = "SELECT password FROM USERS WHERE MATRICULE = "
SELECT_ALL_FOR_MATRICULE = "SELECT * FROM USERS INNER JOIN rights ON users.id = rights.user_id WHERE MATRICULE = "
SELECT_ALL_WHERE_ID = 'SELECT * FROM USERS INNER JOIN rights ON users.id = rights.user_id  ' \
                      'WHERE USERS.id = '

INSERT_ROLE_USERS = "INSERT INTO RIGHTS (supervisor, administrator, developer, user_id) Values"
INSERT_USERS = "INSERT INTO users (users.username, users.lastname, users.matricule, users.password, " \
               "users.mail, users.date_created) values"
# ('toto', 'tata', 'code', 'dyy@dh.fr', '2022-01-11 22:45:06')
UPDATE_USER = "UPDATE USERS INNER JOIN rights ON users.id = rights.user_id " \
              "SET USERS.USERNAME = %s, USERS.LASTNAME = %s, USERS.PASSWORD = %s, USERS.MAIL = %s, " \
              "USERS.DATEMODIFUSER = %s, RIGHTS.SUPERVISOR = %s, " \
              "RIGHTS.ADMINISTRATOR = %s, RIGHTS.DEVELOPER = %s WHERE users.id = %s"

####################____________ROBOTS
SELECT_ALL_ROBOTS = 'SELECT * FROM ROBOTS INNER JOIN rights ON robots.id = rights.robot_right_id'
INSERT_ROLE_ROBOTS = "INSERT INTO RIGHTS (supervisor, administrator, developer, user_id, robot_right_id) Values"
INSERT_ROBOT = "INSERT INTO ROBOTS (name, date_created, id_user_creator_id ) values "
SELECT_ROBOTS = "SELECT id FROM ROBOTS WHERE NAME = "
SELECT_ROBOTS_BY_ID = "SELECT * FROM ROBOTS INNER JOIN rights ON robots.id = rights.robot_right_id WHERE robots.id = "

UPDATE_BOT = "UPDATE ROBOTS INNER JOIN rights ON robots.id = rights.robot_right_id " \
             "SET ROBOTS.NAME = %s, RIGHTS.SUPERVISOR = %s, " \
             "RIGHTS.ADMINISTRATOR = %s, RIGHTS.DEVELOPER = %s WHERE robots.id = %s"


def selectAllUsers():
    mycursor.execute(SELECT_ALL_USERS)
    users = mycursor.fetchall()

    data = []
    for user in users:
        data.append(user)

    mycursor.close()
    mydb.close()
    return data


def selectAllRobots():
    mycursor.execute(SELECT_ALL_ROBOTS)
    bots = mycursor.fetchall()
    data = []
    if not bots:
        for bot in bots:
            data.append(bot)
    else:
        data = None

    mycursor.close()
    mydb.close()
    return data


def select_bot_id(bot_id):
    mycursor.execute(SELECT_ROBOTS_BY_ID + "\'" + bot_id + "\'")
    oBotAndRights = mycursor.fetchall()
    print(oBotAndRights)

    mycursor.close()
    mydb.close()
    return True


def updatebot(botname, supervisor, admin, dev, bot_id, dateModification):
    botname = "\'" + str(botname) + "\'"
    supervisor = str(supervisor)
    admin = str(admin)
    dev = str(dev)
    bot_id = str(bot_id)
    dateModification = "\'" + str(dateModification) + "\'"
    mycursor.execute(UPDATE_BOT % (botname, supervisor, admin, dev, dateModification, bot_id))

    mydb.commit()
    mycursor.close()
    mydb.close()
    return True


def updateuser(username, lastname, password, mail, datemodifuser, supervisor, admin, dev, userid):
    try:
        username = "\'" + str(username) + "\'"
        lastname = "\'" + str(lastname) + "\'"
        password = "\'" + str(password) + "\'"
        mail = "\'" + str(mail) + "\'"
        supervisor = str(supervisor)
        admin = str(admin)
        dev = str(dev)
        userid = str(userid)
        datemodifuser = "\'" + str(datemodifuser) + "\'"
        mycursor.execute(UPDATE_USER % (username, lastname, password, mail, datemodifuser,
                                        supervisor, admin, dev, userid))
        mydb.commit()
        mycursor.close()
        mydb.close()
        return True

    except Exception as e:
        return jsonify({'result': 'un probleme est survenu sur updateuserbdd'}), 400


def selectById(id):
    try:
        mycursor.execute(SELECT_ALL_WHERE_ID + "\'" + id + "\'")
        user = mycursor.fetchall()
        print(user)
        mycursor.close()
        mydb.close()
        user = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return user[0]
    except Exception as e:
        reponse = ["erreur de connexion " + str(e)]
        return reponse


def selectByMatricule(matricule):
    mycursor.execute(SELECT_ALL_FOR_MATRICULE + "\'" + matricule + "\'")
    user = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return user


def selectByMatriculeForlogin(matricule, loginPassword):
    mycursor.execute(SELECT_MATRICULE_FOR_LOGIN + "\'" + matricule + "\'")
    oPassUser = mycursor.fetchall()
    password = oPassUser[0]
    password = str(password)
    characters = "'/(),.[]"
    for x in range(len(characters)):
        password = password.replace(characters[x], "")
    print(password)
    print(loginPassword)
    if not password == loginPassword:
        return False

    mycursor.close()
    mydb.close()
    return True


def createUser(username, lastname, password, matricule, mail, dateCreate, supervisor, admin, dev):
    password = str(password)
    supervisor = str(supervisor)
    admin = str(admin)
    dev = str(dev)

    # insertion d'un nouvel utilistateur
    mycursor.execute(INSERT_USERS + "(\'" + username + "\', " + "\'" + lastname + "\', " + "\'" + matricule + "\', "
                     + "\'" + password + "\'," + "\'" + mail + "\', " + "\'" + dateCreate + "\')")

    # recherche par matricule

    user_id = returnIdByMaticule(matricule)

    # insert via id du matricule
    mycursor.execute(INSERT_ROLE_USERS + "(\'" + supervisor + "\', " + "\'" + admin + "\', " + "\'"
                     + dev + "\', " + "\'" + user_id + "\')")

    # envoi vers base de donne
    mydb.commit()
    mycursor.close()
    mydb.close()
    return True


def createBot(botname, dateCreate, usercreator, supervisor, admin, dev):
    botname = str(botname)
    dateCreate = str(dateCreate)
    usercreator = str(usercreator)
    supervisor = str(supervisor)
    admin = str(admin)
    dev = str(dev)
    print(INSERT_ROBOT + "(\'" + botname + "\', " + "\'" + dateCreate + "\'," + " \'" + usercreator + "\')")
    mycursor.execute(INSERT_ROBOT + "(\'" + botname + "\', " + "\'" + dateCreate + "\'," + " \'" + usercreator + "\')")
    # recherche par nom
    mycursor.execute(SELECT_ROBOTS + "\'" + botname + "\'")
    oSearch_bot_id = mycursor.fetchall()
    search_bot_id = oSearch_bot_id[0]
    search_bot_id = str(search_bot_id)
    characters = "'/(),.[]"
    for x in range(len(characters)):
        search_bot_id = search_bot_id.replace(characters[x], "")
    print(search_bot_id)
    bot_id = str(search_bot_id)

    # insert via id du matricule
    print(INSERT_ROLE_ROBOTS + "(\'" + supervisor + "\', " + "\'" + admin + "\', "
          + "\'" + dev + "\', " + "\'" + usercreator + "\', " + "\'" + bot_id + "\')")
    mycursor.execute(INSERT_ROLE_ROBOTS + "(\'" + supervisor + "\', " + "\'" + admin + "\', "
                     + "\'" + dev + "\', " + "\'" + usercreator + "\', " + "\'" + bot_id + "\')")
    # envoi vers base de donne
    mydb.commit()

    mycursor.close()
    mydb.close()
    return True

def returnIdByMaticule(matricule):

    mycursor.execute(SELECT_MATRICULE + "\'" + matricule + "\'")
    # l'id est sous format [(00, )] je le sors de l'array et le converti en string
    oSearch_user_id = mycursor.fetchall()
    search_user_id = oSearch_user_id[0]
    search_user_id = str(search_user_id)
    characters = "'/(),.[]"
    for x in range(len(characters)):
        search_user_id = search_user_id.replace(characters[x], "")
    mydb.commit()
    mycursor.close()
    mydb.close()
    return search_user_id