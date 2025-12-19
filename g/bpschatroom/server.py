from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

LOG_FILE = "chat.log"

def append_message_to_file(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(message) + "\n")

def load_messages_from_file():
    messages = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    messages.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
    return messages

@socketio.on('connect')
def handle_connect():
    # Send previous messages to the new client
    messages = load_messages_from_file()
    for msg in messages:
        emit('receive_message', msg)

@socketio.on('send_message')
def handle_message(data):
    append_message_to_file(data)
    # Broadcast the message to all connected clients
    emit('receive_message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
