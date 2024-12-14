import asyncio
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from multiprocessing import Process
import websockets
from datetime import datetime
import json
from pymongo import MongoClient
import os

logging.basicConfig(level=logging.INFO)

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        file_name = '/front-init/index.html' if parsed_url.path == '/' else parsed_url.path
        # self.debue(file_name)

        if os.path.exists(file_name):
            self.send_html_file(file_name)
        else:
            self.send_html_file("/front-init/error.html", 404)

    def debue(self, text):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # a = os.getcwd()
        self.wfile.write(bytes(text, "utf-8"))

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        parsed_data = parse_qs(post_data.decode("utf-8"))
        username = parsed_data.get("username")[0]
        message = parsed_data.get("message")[0]

        message_data = json.dumps({"username": username, "message": message})

        async def send_message():
            uri = "ws://localhost:5001"
            async with websockets.connect(uri) as websocket:
                await websocket.send(message_data)

        asyncio.run(send_message())

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Message sent!")

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as file:
            self.wfile.write(file.read())


class WebSocketServer:
    def __init__(self):
        self.client = MongoClient("mongodb://mongodb:27017/")
        self.db = self.client["message_db"]
        self.collection = self.db["messages"]

    async def ws_handler(self, websocket):
        async for message in websocket:
            data = json.loads(message)

            date = datetime.now().strftime  ("%Y-%m-%d %H:%M:%S.%f")

            message_data = {
                "date": date,
                "username": data["username"],
                "message": data["message"],
            }

            self.collection.insert_one(message_data)

            websocket.send(json.dumps(message_data))
            logging.info(f"Saved message: {message_data}")


async def run_websocket_server():
    server = WebSocketServer()
    async with websockets.serve(server.ws_handler, "0.0.0.0", 5001):
        logging.info("WebSocket server started on port 5001")
        await asyncio.Future()


def start_websocket_server():
    asyncio.run(run_websocket_server())


def run_http_server():
    server_address = ("", 3000)
    httpd = HTTPServer(server_address, HttpHandler)
    logging.info("HTTP server started on port 3000")
    httpd.serve_forever()


if __name__ == "__main__":
    http_process = Process(target=run_http_server)
    ws_process = Process(target=start_websocket_server)

    http_process.start()
    ws_process.start()

    http_process.join()
    ws_process.join()