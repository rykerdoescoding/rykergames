from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests
socketio = SocketIO(app, cors_allowed_origins="*")

LOG_FILE = "chat.log"

# Save messages to file
def append_message_to_file(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(message) + "\n")

# Load previous messages
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

# Send previous messages on new connection
@socketio.on('connect')
def handle_connect():
    messages = load_messages_from_file()
    for msg in messages:
        emit('receive_message', msg)

# Handle incoming messages
@socketio.on('send_message')
def handle_message(data):
    append_message_to_file(data)
    emit('receive_message', data, broadcast=True)

if __name__ == '__main__':
    # Run server over HTTPS
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        ssl_context=('cert.pem', 'key.pem')  # <-- Use your SSL certificate files
    )
