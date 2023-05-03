import settings

import chess
import chess.engine
import chess.pgn
import chess.polyglot

chess_engine = chess.engine.SimpleEngine.popen_uci([x for x in settings.get_value(
    "engine_command").split()], timeout=settings.get_value("engine_timeout"))


def restart_engine():
    global chess_engine

    if chess_engine:
        chess_engine.quit()

    chess_engine = chess.engine.SimpleEngine.popen_uci([x for x in settings.get_value(
        "engine_command").split()], timeout=settings.get_value("engine_timeout"))


def get_engine_move(board: chess.Board):
    return chess_engine.play(board=board, limit=chess.engine.Limit(time=settings.get_value("engine_max_thinking_time"), depth=settings.get_value("engine_depth"))).move.uci()


def get_best_move(pieces: list[str], turn: str):
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
        return get_engine_move(board=board)
