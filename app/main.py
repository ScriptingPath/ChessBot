import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

import engine
import settings
import chess.engine

chess_engine = chess.engine.SimpleEngine.popen_uci([x for x in settings.get_value(
    "engine_command").split()], timeout=settings.get_value("engine_timeout"))


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])

        data = json.loads(self.rfile.read(content_length).decode("utf-8"))
        pieces = data.get("pieces")
        turn = data.get("turn")
        action = data.get("action")

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if action == "restart_engine":
            print("Restarting engine...")
            restart_engine()
            print("Engine restarted")

            self.wfile.write(bytes("ok", "utf-8"))

            return

        advisor_boxes_settings = settings.get_value("advisor_boxes")

        self.wfile.write(bytes(
            json.dumps({
                "move": engine.get_best_move(pieces=pieces, turn=turn, engine=chess_engine),
                "from_box_color": advisor_boxes_settings.get("from_box_color"),
                "to_box_color": advisor_boxes_settings.get("to_box_color"),
                "border_size": advisor_boxes_settings.get("border_size"),
                "border_radius": advisor_boxes_settings.get("border_radius")
            }), "utf8"))


def restart_engine():
    global chess_engine

    if chess_engine:
        chess_engine.quit()

    chess_engine = chess.engine.SimpleEngine.popen_uci([x for x in settings.get_value(
        "engine_command").split()], timeout=settings.get_value("engine_timeout"))


def main():
    if not os.path.exists("settings.json"):
        settings.create_settings()

    with HTTPServer(('', settings.get_value("server_port")), handler) as server:
        print(f"Local server started on 127.0.0.1:{server.server_port}")
        server.serve_forever()


while True:
    main()
    print("Local server dead, restarting...")
