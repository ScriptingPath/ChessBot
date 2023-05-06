import os
import settings
if not os.path.exists("settings.json"):
    settings.create_settings()

import json

from http.server import BaseHTTPRequestHandler, HTTPServer

import engine

from threading import Thread
import sys
import console
import ui_core
import traceback


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        console.log("Received request")

        try:
            content_length = int(self.headers['Content-Length'])

            data = json.loads(self.rfile.read(content_length).decode("utf-8"))
            pieces = data.get("pieces")
            turn = data.get("turn")
            action = data.get("action")

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            if action == "restart_engine":
                console.log("Restarting engine...")
                engine.restart_engine()
                console.log("Engine restarted")

                self.wfile.write(bytes("ok", "utf-8"))

                return

            advisor_boxes_settings = settings.get_value("advisor_boxes")

            self.wfile.write(bytes(
                json.dumps({
                    "move": engine.get_best_move(pieces=pieces, turn=turn),
                    "from_box_color": advisor_boxes_settings.get("from_box_color"),
                    "to_box_color": advisor_boxes_settings.get("to_box_color"),
                    "border_size": advisor_boxes_settings.get("border_size"),
                    "border_radius": advisor_boxes_settings.get("border_radius")
                }), "utf8"))
        except Exception:
            console.log(traceback.format_exc())


def main():
    console.clear_log()

    server_thread = Thread(target=thread, daemon=True)
    server_thread.start()

    ui_core.start()

    try:
        engine.chess_engine.quit()
    except:
        pass

    console.clear_log()

    sys.exit()


def start_server():
    with HTTPServer(('', settings.get_value("server_port")), handler) as server:
        console.log(f"Local server started on 127.0.0.1:{server.server_port}")
        server.serve_forever()


def thread():
    while True:
        start_server()
        console.log("Local server dead, restarting...")


if __name__ == '__main__':
    main()
