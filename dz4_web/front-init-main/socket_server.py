import socket
import json

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

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 5000)
udp_socket.bind(server_address)

while True:
    data, address = udp_socket.recvfrom(1024)
    data = data.decode()
    username, message = data.split(',')

    save_message(username, message)

udp_socket.close()
