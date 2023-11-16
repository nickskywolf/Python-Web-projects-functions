from http.server import HTTPServer, BaseHTTPRequestHandler
import mimetypes
import urllib.parse
from pathlib import Path
import socket
import json

BASE_DIR = Path()

class HttpRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        print(route.query)
        
        if route.path == '/':
            self.send_html('index.html')
        elif route.path == '/style.css':
            self.send_static('style.css')
        elif route.path == '/logo.png':
            self.send_static('logo.png')
        elif route.path == '/contact':
            self.send_html('contact.html')
        elif route.path == '/message':
            self.send_html('message.html')
        else:
            self.send_html('error.html', 404)

    def do_POST(self):
        if self.path == '/message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data_str = post_data.decode('utf-8')
            post_data_dict = urllib.parse.parse_qs(post_data_str)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("Message received!", "utf-8"))
            self.send_message_to_socket(post_data_dict)

    def send_html(self, filename, status_code=200):
        file_path = BASE_DIR.joinpath(filename)
        print("Attempting to open HTML file:", file_path)
        try:
            with open(file_path, 'rb') as file:
                self.send_response(status_code)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            print("HTML file not found:", file_path)
            self.send_html('error.html', 404)

    def send_static(self, filename, status_code=200):
        file_path = BASE_DIR.joinpath(filename)
        print("Attempting to open static file:", file_path)
        try:
            with open(file_path, 'rb') as file:
                self.send_response(status_code)
                mime_type, *_ = mimetypes.guess_type(filename)
                if mime_type:
                    self.send_header('Content-Type', mime_type)
                else:
                    self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            print("Static file not found:", file_path)
            self.send_html('error.html', 404)

    def send_message_to_socket(self, message_dict):
        try:
            socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = ('localhost', 5000)
            message_json = json.dumps(message_dict)
            socket_client.sendto(message_json.encode('utf-8'), server_address)
            print(f"Data sent to {server_address}: {message_json}")
        except Exception as e:
            print(f"Error sending data to socket: {e}")
        finally:
            socket_client.close()

def run_server():
    address = ('localhost', 3000)
    http_server = HTTPServer(address, HttpRequestHandler)
    
    try:
        print(f"Server is running at http://{address[0]}:{address[1]}")
        http_server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")
    finally:
        http_server.server_close()

if __name__ == '__main__':
    run_server()
