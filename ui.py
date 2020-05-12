from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from datetime import datetime
import messengerui
import requests


class MessengerApp(QtWidgets.QMainWindow, messengerui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.last_time = 0
        self.pushButton.pressed.connect(self.button_send)
        '''
        Подключаю кнопку отправки.
        '''
        self.pushButton_2.pressed.connect(self.button_update)
        '''
        Подключаю кнопку обновления сообщений.
        '''

    '''
    По нажатию кнопки "send" происходит отправка сообщения и авторизация.
    '''

    def send_message(self, username, password, text):
        response = requests.post(
            "http://127.0.0.1:5000/auth",
            json={"username": username, "password": password}
        )
        if not response.json()['ok']:
            self.add_to_chat('*wrong password*')
            return

        response = requests.post(
            "http://127.0.0.1:5000/send",
            json={"username": username, "password": password, "text": text}
        )
        if not response.json()['ok']:
            self.add_to_chat('*wrong login information*')
            return
        '''
        Данные переходят на сервер.
        На сервере происходит проверка пароля.
        Из сервера приходит резудьтат проверки.
        '''

    def update_messages(self):
        response = requests.get("http://127.0.0.1:5000/messages",
                                params={'after': self.last_time})

        '''
        Подключение к серверу.
        '''
        messages = response.json()["messages"]

        for message in messages:
            normal_form_time = datetime.fromtimestamp(message["time"])
            normal_form_time = normal_form_time.strftime('%d/%m/%Y %H:%M:%S')
            self.add_to_chat(str(message["username"] + ' ' + normal_form_time))
            self.add_to_chatstr(str(message["text"]))
            self.add_to_chat('')

            self.last_time = message["time"]
        '''
        Добавление сообщения.
        '''

    def button_send(self):
        try:
            self.send_message(
                self.textEdit_2.toPlainText(),
                self.textEdit_3.toPlainText(),
                self.textEdit.toPlainText()
            )
        except:
            self.add_to_chat('*something went wrong*')

        self.textEdit.setText('')
        self.textEdit.repaint()
        '''
        Кнопка отправки сообщения.
        '''

    def button_update(self):
        response = requests.get("http://127.0.0.1:5000/messages",
                                params={'after': self.last_time})
        messages = response.json()["messages"]
        '''
        Кнопка обновления экрана сообщений.
        '''

        for message in messages:
            normal_time = datetime.fromtimestamp(message["time"])
            normal_time = normal_time.strftime('%d/%m/%Y %H:%M:%S')
            self.add_to_chat(message["username"] + ' ' + normal_time)
            self.add_to_chat(message["text"])
            self.add_to_chat('')

            self.last_time = message["time"]

    def add_to_chat(self, text):
        self.textBrowser.append(text)
        self.textBrowser.repaint()
        '''
        Отображение сообщения в экране сообщений.
        '''

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?",
                                     QMessageBox.Yes |
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        '''
        Сообщение о выходе из программы.
        '''


app = QtWidgets.QApplication([])
window = MessengerApp()
window.show()
'''
Отображение интерфейса.
'''
app.exec_()
