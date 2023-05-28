import time
from datetime import datetime

from flask import Flask, request, abort

app = Flask(__name__)
db = [
    {
        'time': time.time(),
        'name': 'Jack',
        'text': 'Привет всем!',
    },
    {
        'time': time.time(),
        'name': 'Mary',
        'text': 'Привет, Jack!',
    },
]


@app.route("/")
def hello():
    return 'Hello world'


@app.route("/status")
def status():
    dt_now = datetime.now()
    return {
        'status': True,
        'name': 'Messenger',
        'time1': time.asctime(),
        'time2': time.time(),
        'time3': dt_now,
        'time4': str(dt_now),
        'time5': dt_now.strftime('%Y/%m/%d time: %H:%M:%S'),
        'time6': dt_now.isoformat()
    }


@app.route("/send", methods=['POST'])
def send_message():
    data = request.json

    if not isinstance(data, dict):
        return abort(400)
    if set(data.keys()) != {'name', 'text'}:
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)

    name = data['name']
    text = data['text']

    if not isinstance(name, str) or not isinstance(text, str) or \
            name == '' or text == '':
        return abort(400)

    message = {
        'time': time.time(),
        'name': name,
        'text': text,
    }
    db.append(message)
    return {'ok': True}


@app.route("/messages")
def get_messages():
    """messages from db after given timestamp"""

    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    result = []
    for message in db:
        if message['time'] > after:
            result.append(message)
            if len(result) >= 100:
                break

    return {'messages': result}


app.run()
