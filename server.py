import time
from flask import Flask, request
import sqlite3 as sql

'''
Подключение необходимых библиотек.
'''

con = sql.connect('users.db')
cur = con.cursor()
result = cur.execute("""SELECT * FROM users""").fetchall()

'''
Подключение базы данных.
'''

users = []
passwords = []
for i in result:
    users.append(i[0])
    passwords.append(i[1])

messages = []
app = Flask(__name__)


@app.route("/messages")
def messages_view():
    new_messages = []
    after = float(request.args['after'])
    for message in messages:
        if int(message['time']) > int(after):
            new_messages.append(message)
    return {"messages": new_messages}
    '''
    Отображение новых сообщений.
    '''


@app.route("/send", methods=['POST', 'GET'])
def send_view():
    data = request.json
    username = data["username"]
    password = data["password"]
    number = int(users.index(username))

    if username not in users or str(password) != str(passwords[number]):
        return {"ok": False}

    '''
    Проверка входных данных.
    '''
    text = data["text"]
    messages.append({"username": username, "text": text, "time": time.time()})
    '''
    Добавление сообщения.
    '''

    return {"ok": True}


@app.route("/auth", methods=['POST', 'GET'])
def auth_view():
    data = request.json
    username = data["username"]
    password = data["password"]

    if username not in users:
        con = sql.connect('users.db')
        cur = con.cursor()
        users.append(username)
        passwords.append(password)
        cur.execute(f"INSERT INTO users VALUES('{username}', '{password}')")
        con.commit()

        '''
        Добавление нового пользователя.
        '''

        return {"ok": True}
    else:
        number = int(users.index(username))
        if str(password) == str(passwords[number]):
            return {"ok": True}
        else:
            return {"ok": False}
    '''
    Проверка входных данных.
    '''


'''
Запуск приложения.
'''
app.run()
