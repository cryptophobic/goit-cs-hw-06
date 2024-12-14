import os
from flask import Flask, request, render_template, send_from_directory
from flask_sock import Sock
from multiprocessing import Process
import socket
import json
from datetime import datetime
from pymongo import MongoClient

# MongoDB setup
MONGO_URI = "mongodb://mongo:27017/"
DB_NAME = "messages_db"
COLLECTION_NAME = "messages"

# Flask app setup
app = Flask(__name__, static_folder='front-init', template_folder='front-init')
sock = Sock(app)

# Static file handling
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('front-init', path)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        send_to_socket_server(username, message)
        return "Message sent!"
    return render_template('message.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html'), 404

# Socket communication
def send_to_socket_server(username, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 5000))
    data = json.dumps({"username": username, "message": message}).encode('utf-8')
    client_socket.sendall(data)
    client_socket.close()

# Socket server for MongoDB interaction
def socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 5000))
    server_socket.listen(5)

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    while True:
        conn, addr = server_socket.accept()
        data = conn.recv(1024)
        if data:
            message = json.loads(data.decode('utf-8'))
            message["date"] = datetime.now().isoformat()
            collection.insert_one(message)
        conn.close()

# Main entry point
def main():
    # Start socket server in a separate process
    socket_process = Process(target=socket_server)
    socket_process.start()

    # Start Flask app
    app.run(host='0.0.0.0', port=3000, debug=True)

    # Ensure the socket process is terminated on exit
    socket_process.join()

if __name__ == "__main__":
    main()
