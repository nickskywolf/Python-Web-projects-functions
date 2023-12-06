import json
import logging
import mimetypes
import os
import pathlib
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import socket
from threading import Thread

HTTP_IP = "127.0.0.1"
HTTP_PORT = 3000
SOCKET_IP = "127.0.0.1"
SOCKET_PORT = 5000
JSON_PATH = "storage/data.json"


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message.html":
            self.send_html_file("message.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 400)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())

    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        send_data_to_socket(data)
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()


def run_http_server(ip, port):
    server_address = (ip, port)
    http = HTTPServer(server_address, HttpHandler)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        http.server_close()


def send_data_to_socket(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(data, (SOCKET_IP, SOCKET_PORT))
    client_socket.close()


def run_socket_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    server_socket.bind(server)
    print("Server listening")
    try:
        while True:
            data, address = server_socket.recvfrom(1024)
            save_data(data)
    except KeyboardInterrupt:
        logging.info("Server closed")
    finally:
        server_socket.close()


def save_data(data):
    data_parse = urllib.parse.unquote_plus(data.decode())
    try:
        # Форматування даних
        data_dict = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        # Додавання словника
        if not os.path.exists(JSON_PATH.split("/")[0]):
            os.mkdir("storage")
        if not os.path.exists(JSON_PATH):
            with open(JSON_PATH, "w", encoding="utf-8") as f:
                json.dump({}, f)
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            json_dict = (
                {date: data_dict} if os.stat(JSON_PATH).st_size == 0 else json.load(f)
            )
        json_dict.update({date: data_dict})
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(json_dict, f, indent=4, ensure_ascii=False)

    # обробка помилок
    except ValueError as err:
        logging.error(f"Field parse data: {err}")
    except OSError as err:
        logging.error(f"Field OSError: {err}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    http_server = Thread(target=run_http_server, args=(HTTP_IP, HTTP_PORT))
    http_server.start()
    socket_server = Thread(target=run_socket_server, args=(SOCKET_IP, SOCKET_PORT))
    socket_server.start()
