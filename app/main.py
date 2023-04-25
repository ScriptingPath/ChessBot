import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

import engine
import settings
from stockfish import Stockfish


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])

        data = json.loads(self.rfile.read(content_length).decode("utf-8"))
        moves = data.get("moves")
        next_move = data.get("next_move")

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write(bytes(engine.get_best_move(
            next_move=next_move, moves=moves, stockfish=stockfish), "utf8"))


def reset_stockfish():
    global stockfish
    stockfish = Stockfish(path=settings.get_value("stockfish_path"), depth=settings.get_value(
        "stockfish_depth"), parameters=settings.get_value("stockfish_params"))


def main():
    if not os.path.exists("settings.json"):
        settings.create_settings()
    
    reset_stockfish()

    with HTTPServer(('', 9211), handler) as server:
        print("Server Started")
        server.serve_forever()


while True:
    main()
    print("Server Restarted")
