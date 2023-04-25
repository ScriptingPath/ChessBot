import chess
import chess.pgn
from stockfish import Stockfish


def get_stockfish_move(fen: str, stockfish: Stockfish):
    stockfish.set_fen_position(fen)

    return stockfish.get_best_move()


def find_game(moves: str):
    with open("data/openings", "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith(moves):
                return line


def get_best_move(moves: list, next_move: int, stockfish: Stockfish):
    if moves == None or moves == "":
        return "e2e4"

    board = chess.Board()

    for move in moves:
        board.push_san(move)

    find_result = find_game(moves=" ".join(str(x) for x in board.move_stack).strip())

    if find_result:
        return find_result.split()[next_move - 1]
    else:
        return f"{get_stockfish_move(fen=board.fen(), stockfish=stockfish)} stockfish"
