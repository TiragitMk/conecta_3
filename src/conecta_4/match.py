class Match:
    """
    Partida entre dos jugadores. Asigna las fichas, junta a los rivales,
    gestiona turnos y consulta al tablero quién ha ganado.
    No conoce las reglas, se las pregunta al tablero.
    """
    def __init__(self, player1, player2):
        # char hardcoded.
        player1.char = 'o'
        player2.char = 'x'
        player1.opponent = player2 # Esto lo permite el @opponent.setter con opponent.

        self._players = {'o': player1, 'x': player2}
        self._round = [player1, player2]

    @property
    def get_next_player(self):
        """
        Mira el jugador. Empieza siempre en el primero.
        Aunque se use como atributo (sin paréntesis), MODIFICA el estado,
        porque invierte la lista de turnos en cada lectura.
        :return: jugador al que le toca mover
        """
        next_player = self._round[0]
        self._round.reverse()
        return next_player

    def get_player(self, char):
        """
        Mira la ficha del jugador.
        :param char: ficha del personaje
        :return: jugador
        """
        return self._players[char]

    def get_winner(self, board):
        """
        Mira en el tablero si la ficha ha ganado y devuelve el jugador que gana.
        :param board: SquareBoard
        :return: player ganador o None
        """
        if board.is_victory('x'):
            return self.get_player('x')
        if board.is_victory('o'):
            return self.get_player('o')
        else:
            return None

    def get_loser(self, board):
        """
        Mira en el tablero si la ficha ha perdido y devuelve el jugador que pierde.
        :param board: SquareBoard
        :return: player perdedor o None
        """
        if board.is_victory('x'):
            return self.get_player('o')
        if board.is_victory('o'):
            return self.get_player('x')

    def play_more(self):
        """
        Pregunta al usuario si quiere jugar una partida más.
        Repite hasta recibir 's' o 'n'.
        :return: bool
        """
        result = True
        while True:
            answer = input('¿Le apetece una partida más? S/N')
            if answer.lower() == 's':
                result = True
                break
            elif answer.lower() == 'n':
                result = False
                break
        return result
