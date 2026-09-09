class Match:
    def __init__(self, player1, player2):
        #Asignamos los char a mano. Después se elegiran al azar.
        player1.char = 'o'
        player2.char = 'x'
        #Tenemos que fijar el oponente
        player1.opponent = player2

        self._players = {'o': player1, 'x': player2}
        self._round = [player1, player2]

    @property
    def get_next_player(self):
        """
        Mira el jugador. Empieza siempre en el primer
        :return:
        """
        next_player = self._round[0]
        self._round.reverse()
        return next_player

    def get_player(self, char):
        """
        Mira la ficha del jugador
        :param char:
        :return:
        """
        return self._players[char]

    def get_winner(self, board):
        """
        Mira en el tablero si la ficha ha ganado y devuelve el jugador
        :param board:
        :return:
        """
        if board.is_victory('x'):
            return self.get_player('x')
        if board.is_victory('o'):
            return self.get_player('o')
        else:
            return None

    def get_loser(self, board):
        """
        Mira en el tablero si la ficha ha perdido y devuelve el jugador
        :param board:
        :return:
        """
        if board.is_victory('x'):
            return self.get_player('o')
        if board.is_victory('o'):
            return self.get_player('x')

    def play_more(self):
        """
        Pregunta al usuario si quiere jugar una partida más
        :return:
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








