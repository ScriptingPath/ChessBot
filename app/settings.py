import json
import os
from typing import Optional

default_settings = {
    "stockfish_path": "stockfish.exe",
    "stockfish_depth": 15,

    "stockfish_params": {
        "Debug Log File": "",
        "Contempt": 0,
        "Min Split Depth": 0,
        "Threads": 1,
        "Ponder": "false",
        "Hash": 16,
        "MultiPV": 1,
        "Skill Level": 20,
        "Move Overhead": 10,
        "Minimum Thinking Time": 20,
        "Slow Mover": 100,
        "UCI_Chess960": "false",
        "UCI_LimitStrength": "false",
        "UCI_Elo": 1350,
    }
}


def get_value(key: str) -> Optional[str]:
    return read_settings().get(key)


def read_settings() -> str:
    with open("settings.json", "r", encoding="utf-8") as file:
        return json.loads(file.read())


def create_settings() -> None:
    with open("settings.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(default_settings))
