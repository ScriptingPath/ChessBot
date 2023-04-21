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

var tags = {
    "moves_box": "l4x",
    "move_number": "i5z",
    "move": "kwdb",
    "board": "cg-board",
    "puzzle_move": "move",
    "index_number": "index"
}


var classes = {
    "puzzle_moves_box": ".tview2",
    "white_orientation": ".orientation-white",
    "black_orientation": ".orientation-black"
}


var vertical = {}
var horizontal = {}


function get_moves() {
    var moves_box = document.querySelector(tags.moves_box);
    var puzzle_box = document.querySelector(classes.puzzle_moves_box);

    if (moves_box) {
        var moves = "";

        Array.from(moves_box.childNodes).forEach(function (elem) {
            if (elem.tagName == tags.move_number.toUpperCase()) {
                moves += `${elem.textContent}. `;

            } else if (elem.tagName == tags.move.toUpperCase()) {
                moves += `${elem.textContent} `;
            }
        })

        return moves.trim();

    } else if (puzzle_box) {
        var moves = "";

        Array.from(puzzle_box.childNodes).forEach(function (elem) {
            if (elem.tagName == tags.index_number.toUpperCase()) {
                moves += `${elem.textContent}. `;
            } else if (elem.tagName == tags.puzzle_move.toUpperCase()) {
                moves += `${elem.textContent} `;
            }
        })

        return moves.trim();
    }
}


function get_moves_count() {
    var moves_box = document.querySelector(tags.moves_box);
    var puzzle_box = document.querySelector(classes.puzzle_moves_box);

    if (moves_box) {
        return moves_box.querySelectorAll(tags.move).length;
    } else if (puzzle_box) {
        return puzzle_box.querySelectorAll(tags.puzzle_move).length;
    }
}


function get_board_square_size() {
    return get_board_size() / 8;
}


function get_board_size() {
    return document.querySelector(tags.board).parentNode.style.width.replace("px", "");
}


function get_board_orientation() {
    if (document.querySelector(classes.white_orientation)) {
        return "white"
    } else if (document.querySelector(classes.black_orientation)) {
        return "black"
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


function draw_move(move) {
    var from = move.slice(0, -2)
    var to = move.slice(2)

    var board = document.querySelector(tags.board);

    var from_square = document.createElement("square");
    from_square.className = "from";
    from_square.setAttribute("style", `transform: translate(${horizontal[from[0]]}px, ${vertical[from[1]]}px);
    border: 2px solid #0000ff;
    border-radius: 10px`)
    board.appendChild(from_square);

    var to_square = document.createElement("square");
    to_square.className = "to";
    to_square.setAttribute("style", `transform: translate(${horizontal[to[0]]}px, ${vertical[to[1]]}px);
    border: 2px solid #ff0000;
    border-radius: 10px`)

    board.appendChild(to_square);
}


function remove_draw() {
    Array.from(document.querySelector(tags.board).querySelectorAll(".from")).forEach(function (elem) {
        elem.remove();
    })

    Array.from(document.querySelector(tags.board).querySelectorAll(".to")).forEach(function (elem) {
        elem.remove();
    })
}


(function () {
    'use strict';

    document.addEventListener('keydown', function (event) {
        if (event.code == 'KeyX') {

            GM_xmlhttpRequest({
                method: "POST",
                url: "http://127.0.0.1:9211/",
                data: get_moves(),

                headers: {
                    "Content-Type": "application/json"
                },

                onload: function (response) {
                    var data = response.responseText

                    if (data != "None" && data != null && data != undefined) {
                        set_cords();
                        remove_draw();
                        draw_move(response.responseText.split(" ")[0])
                    } else {
                        console.error(`Engine Error: Response is ${data}`)
                    }

                }
            });
        }
    });

})();

