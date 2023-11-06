import http.server
import socketserver
import socket
import json
from datetime import datetime

# Порт HTTP сервера
PORT_HTTP = 3000

# Вказуємо абсолютний шлях до папки, де знаходяться файли
FILES_PATH = 'F:/Python/Game/web/dz4_web/'

# Відкриваємо файл data.json для зберігання даних
data_file = "storage/data.json"
data = {}

# Створюємо HTTP обробник, який буде обслуговувати HTTP запити
class HttpHandler(http.server.SimpleHTTPRequestHandler):
    # Розрізняємо HTTP GET запити
    def do_GET(self):
        path = FILES_PATH + self.path[1:]  # Формуємо абсолютний шлях до файлу
        try:
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open(FILES_PATH + 'index.html', 'rb') as f:
                    self.wfile.write(f.read())
            elif self.path == '/message':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open(FILES_PATH + 'message.html', 'rb') as f:
                    self.wfile.write(f.read())
            elif self.path == '/style.css':
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                with open(FILES_PATH + 'style.css', 'rb') as f:
                    self.wfile.write(f.read())
            elif self.path == '/logo.png':
                self.send_response(200)
                self.send_header('Content-type', 'image/png')
                self.end_headers()
                with open(FILES_PATH + 'logo.png', 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open(FILES_PATH + 'error.html', 'rb') as f:
                    self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(FILES_PATH + 'error.html', 'rb') as f:
                self.wfile.write(f.read())

# Запуск HTTP сервера в окремому потоці
def start_http_server():
    httpd = socketserver.TCPServer(("", PORT_HTTP), HttpHandler)
    print("HTTP сервер на порту", PORT_HTTP)
    httpd.serve_forever()

# Запуск HTTP сервера в окремому потоці
import threading
http_thread = threading.Thread(target=start_http_server)
http_thread.start()
