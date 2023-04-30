import json

default_settings = {
    "engine_command": None,  # path to engine with args
    "engine_timeout": 15,  # timeout for starting and thinking
    "engine_max_thinking_time": 2,
    "engine_depth": 15,  # strength (change it for speed)
    # WARNING! If you change the port here, change it in the script as well
    "server_port": 9211,

    "advisor_boxes": {
        "from_box_color": "#0000FF",
        "to_box_color": "#ff0000",
        "border_size": "3px",
        "border_radius": "0px"
    }
}


def get_value(key: str):
    return read_settings().get(key)


def read_settings() -> str:
    with open("settings.json", "r", encoding="utf-8") as file:
        return json.loads(file.read())


def create_settings() -> None:
    with open("settings.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(default_settings))
