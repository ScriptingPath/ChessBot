import settings

import chess
import chess.engine
import chess.pgn
import chess.polyglot


def get_engine_move(board: chess.Board, engine: chess.engine.SimpleEngine):
    return engine.play(board=board, limit=chess.engine.Limit(time=settings.get_value("engine_max_thinking_time"), depth=settings.get_value("engine_depth"))).move.uci()


def get_best_move(pieces: list[str], turn: str, engine: chess.engine.SimpleEngine):
    if not pieces:
        return None

    board = chess.Board()
    board.clear()
    board.turn = chess.WHITE if turn == "white" else chess.BLACK

    for piece in pieces:
        splited = piece.split()
        position = splited[0]
        piece_char = splited[1]

        board.set_piece_at(square=chess.parse_square(
            position), piece=chess.Piece.from_symbol(piece_char))

    if not board.is_game_over():
        return get_engine_move(board=board, engine=engine)
