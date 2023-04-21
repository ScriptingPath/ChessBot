import io
from typing import Optional

import chess
import chess.pgn
import settings
from stockfish import Stockfish


def get_best_move(moves: str, stockfish: Stockfish) -> Optional[str]:
    if moves == None or moves == "":
        return "e2e4"

    game = chess.pgn.read_game(io.StringIO(moves))

    board = game.board()

    for move in game.mainline_moves():
        board.push(move)

    stockfish.set_fen_position(board.fen())

    return stockfish.get_best_move()
