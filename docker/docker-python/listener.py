from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import socketserver
from time import sleep
import requests
import optimizer
from threading import Thread

PORT = 57821


class handler(BaseHTTPRequestHandler):

    def __init__(self, request: bytes, client_address: tuple[str, int], server: socketserver.BaseServer) -> None:
        super().__init__(request, client_address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = "Not supported\n"
        self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        message = "OK\n"
        self.wfile.write(bytes(message, "utf8"))

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        try:
            data = json.loads(post_data)
        except:
            data = "Error"

        opti = optimizer.Optimizer()
        setattr(opti, 'data', data)
        opti_thread = Thread(target=opti.calc)
        opti_thread.start()


def main():
    # optimizer.Optimizer()
    with HTTPServer(('', PORT), handler) as server:
        server.serve_forever()


if __name__ == '__main__':
    main()
