// ==UserScript==
// @name         LichessBot
// @namespace    https://github.com/ScriptingPath/ChessBot
// @version      1.0
// @description  ChessBot For Lichess
// @author       ScriptingPath
// @grant        GM_xmlhttpRequest
// @connect      127.0.0.1
// @match        *://*.lichess.org/*
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// ==/UserScript==

const SERVER_PORT = 9211;

var last_board_childs = null;
var observer = null;
var interval = null;

var tags = {
    "moves_box": "l4x",
    "move": "kwdb",
    "board": "cg-board",
    "puzzle_move": "move",
    "piece": "piece"
}


var classes = {
    "puzzle_moves_box": ".tview2",
    "white_orientation": ".orientation-white",
    "black_orientation": ".orientation-black",
    "button": ".button"
}


var vertical = {}
var horizontal = {}


function get_pieces() {
    var pieces = [];
    var board = get_board();

    Array.from(board.querySelectorAll(tags.piece)).forEach(function (elem) {
        var text_split = elem.className.split(" ");
        var color_char = text_split[0][0];
        var piece_char = text_split[1] == "knight" ? "n" : text_split[1][0];
        var piece_position = get_piece_position(elem);

        pieces.push(`${piece_position} ${color_char == "w" ? piece_char.toUpperCase() : piece_char.toLowerCase()}`);
    })

    return pieces;
}


function get_board() {
    return document.querySelector(tags.board);
}


function get_piece_position(elem) {
    var style = window.getComputedStyle(elem);
    var matrix = new WebKitCSSMatrix(style.transform);

    var x = matrix.m41;
    var y = matrix.m42;

    return `${Object.keys(horizontal).find(key => horizontal[key] === x)}${Object.keys(vertical).find(key => vertical[key] === y)}`;
}

function get_board_square_size() {
    return get_board_size() / 8;
}


function get_board_size() {
    return get_board().offsetHeight;
}


function get_board_orientation() {
    if (document.querySelector(classes.white_orientation)) {
        return "white";
    } else if (document.querySelector(classes.black_orientation)) {
        return "black";
    } else {
        return "white";
    }
}



function set_cords() {
    var square_size = get_board_square_size();

    if (get_board_orientation() == "white") {
        horizontal = {
            "a": square_size * 0,
            "b": square_size * 1,
            "c": square_size * 2,
            "d": square_size * 3,
            "e": square_size * 4,
            "f": square_size * 5,
            "g": square_size * 6,
            "h": square_size * 7
        }

        vertical = {
            "8": square_size * 0,
            "7": square_size * 1,
            "6": square_size * 2,
            "5": square_size * 3,
            "4": square_size * 4,
            "3": square_size * 5,
            "2": square_size * 6,
            "1": square_size * 7
        }
    } else {
        horizontal = {
            "a": square_size * 7,
            "b": square_size * 6,
            "c": square_size * 5,
            "d": square_size * 4,
            "e": square_size * 3,
            "f": square_size * 2,
            "g": square_size * 1,
            "h": square_size * 0
        }

        vertical = {
            "8": square_size * 7,
            "7": square_size * 6,
            "6": square_size * 5,
            "5": square_size * 4,
            "4": square_size * 3,
            "3": square_size * 2,
            "2": square_size * 1,
            "1": square_size * 0
        }
    }
}


function draw_move(move, from_color, to_color, border_size, border_radius) {
    var from = move.slice(0, -2);
    var to = move.slice(2);

    var board = get_board();

    var from_square = document.createElement("square");
    from_square.className = "from";
    from_square.setAttribute("style", `transform: translate(${horizontal[from[0]]}px, ${vertical[from[1]]}px);
    border: ${border_size} solid ${from_color};
    border-radius: ${border_radius}`);
    board.appendChild(from_square);

    var to_square = document.createElement("square");
    to_square.className = "to";
    to_square.setAttribute("style", `transform: translate(${horizontal[to[0]]}px, ${vertical[to[1]]}px);
    border: ${border_size} solid ${to_color};
    border-radius: ${border_radius}`);

    board.appendChild(to_square);
}


function remove_draw() {
    var board = get_board();

    Array.from(board.querySelectorAll(".from")).forEach(function (elem) {
        elem.remove();
    })

    Array.from(board.querySelectorAll(".to")).forEach(function (elem) {
        elem.remove();
    })
}

function get_best_move() {
    set_cords();

    GM_xmlhttpRequest({
        method: "POST",
        url: "http://127.0.0.1:9211/",
        data: JSON.stringify({
            "pieces": get_pieces(),
            "turn": get_board_orientation()
        }),

        headers: {
            "Content-Type": "application/json; charset=utf-8"
        },

        onload: function (response) {
            var data = JSON.parse(response.responseText)

            if (data != "None" && data != null && data != undefined) {
                remove_draw();

                draw_move(data["move"], data["from_box_color"], data["to_box_color"], data["border_size"], data["border_radius"]);

            } else {
                console.error(`Engine Error: Response is ${data}`);
            }
        }
    });
}

function restart_engine() {
    GM_xmlhttpRequest({
        method: "POST",
        url: "http://127.0.0.1:9211/",
        data: JSON.stringify({
            "action": "restart_engine"
        }),

        headers: {
            "Content-Type": "application/json; charset=utf-8"
        },
    })
}

(function () {
    'use strict';

    document.addEventListener('keydown', function (event) {
        if (event.code == 'KeyX') {
            get_best_move();
        } else if (event.code == 'KeyR') {
            restart_engine();
        }
    });

})();