from datetime import datetime
from PyQt5 import QtWidgets, QtCore
import clientui
import requests


class Messenger(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.Send.pressed.connect(self.send_message)

        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)

    def print_message(self, message):
        t = message['time']
        dt = datetime.fromtimestamp(t)
        dt = dt.strftime('%H:%M:%S')
        self.textBrowser.append(dt + ' ' + message['name'])
        self.textBrowser.append(message['text'])
        self.textBrowser.append('')

    def get_messages(self):
        try:
            response = requests.get(
                'https://0583a10d6095.ngrok.io/messages',
                params={'after': self.after}
            )
        except:
            return
        messages = response.json()['messages']
        for message in messages:
            self.print_message(message)
            self.after = message['time']

    def send_message(self):
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()
        try:
            response = requests.post(
                'https://0583a10d6095.ngrok.io/send',
                json={
                    'name': name,
                    'text': text
                }
            )
        except:
            self.textBrowser.append('Сервер недоступен')
            self.textBrowser.append('Попробуйте позднее')
            self.textBrowser.append('')
            return

        if response.status_code != 200:
            self.textBrowser.append('Проверьте имя и текст')
            self.textBrowser.append('')
            return

        self.textEdit.setText('')


app = QtWidgets.QApplication([])
window = Messenger()
window.show()
app.exec()
