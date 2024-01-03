import os
import json
from Flask import Flask, render_template, request, redirect, url_for
import socket
from datetime import datetime

app = Flask(__name__)

def save_message(username, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    message_data = {
        timestamp: {
            "username": username,
            "message": message
        }
    }

    storage_file = os.path.join("storage", "data.json")
    with open(storage_file, "r+") as file:
        data = json.load(file)
        data.update(message_data)
        file.seek(0)
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
    username = request.form['username']
    message_text = request.form['message']

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 5000)
    message_to_send = f"{username},{message_text}"
    udp_socket.sendto(message_to_send.encode(), server_address)


    save_message(username, message_text)

    return redirect(url_for('index'))

@app.route('/message.html')
def message_page():
    return render_template('message.html')

@app.route('/error.html')
def error_page():
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(port=3000, threaded=True)

