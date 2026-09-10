class Move:
    """
    Registro de una jugada. Es lo que guarda el Player en last_moves.

    position: columna elegida
    board_code: BoardCode del tablero
    recommendation: recomendaciones que tenía el oráculo
    player: quién jugó
    """
    def __init__(self, position, board_code, recommendation, player ):
        self.position = position
        self.board_code = board_code
        self.recommendation = recommendation
        self.player = player
