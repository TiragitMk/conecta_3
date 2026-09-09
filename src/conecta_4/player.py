from random import choice

from conecta_4.oracle import *
from conecta_4.square_board import *
from conecta_4.move import *
from conecta_4.settings import BOARD_LENGTH

class Player:
    def __init__(self, name, char = None, oracle = BaseOracle(), opponent = None):
        self.name = name
        self.char = char
        self._oracle = oracle
        self.opponent = opponent

        #Quiero guardar la tirada
        self.last_moves = []

    @property
    def opponent(self):
        return self._opponent
    @opponent.setter
    def opponent(self, other):
        self._opponent = other
        if other is not None:
            other._opponent = self

    def play(self, board):
        """
        Elige la mejor columna donde jugar. Estas me las recomienda el oráculo
        :param board:
        :return:
        """
        (best, recommendations) = self._ask_oracle(board)
        self._play_on(board, best.index, recommendations)

    def _play_on(self, board, position, recommendations ):
        """
        Jugamos en la pocisión elegida de las jugadas recomendadas
        :param board:
        :param position:
        :param recommendation:
        :return:
        """
        board.add(self.char, position)
        self.last_moves.insert(0, Move(position, board.as_code(),recommendations, self)) #Más adelante quiero guardar recomendaciones, juagada, char. etc....
                                        #Lo haré con un insert en una tupla
    def _ask_oracle(self, board):
        """
        Pregunto al oráculo para que me de las posibles jugadas
        :param board:
        :return:
        """
        recommendations = self._oracle._get_recommendation(board, self)
        best = self._choose_a_recommendation(recommendations)
        return (best, recommendations)

    def _choose_a_recommendation(self, recommendations):
        """
        Elijo una de las recomendaciones que me da el oráculo
        :param board:
        :return:
        """
        valid_recommendations = list(filter(lambda x:
                                            x.classification != ColumnClassification.FULL,
                                            recommendations))
        #Ordenamos la lista de mayor a menor
        valid_recommendations = sorted(valid_recommendations, key = lambda x : x.classification.value, reverse = True)
        if all_the_same_score(valid_recommendations):
            return choice(valid_recommendations)
        else:
            return valid_recommendations[0]
    #Hooks
    def _on_lose(self):
        pass


class HumanPlayer(Player):
    """
    Esta clase no se testea porque son valores introducidos por el usuario
    Testeamos los valores que introduce el usuario
    """
    def __init__(self, name, char = None):
        super().__init__(name, char)

    def _ask_oracle(self, board):
        """
        Mi oráculo es el jugador humano. Le pido que me de la posición a través de pantalla
        :param board:
        :return:
        """
        while True:
            position = input("Tu turno! Selecciona una columna: ")
            #Comprobaciones de entrada correcta
            if (HumanEntryVerifications._is_int(position) and
                HumanEntryVerifications._is_in_range(board,int(position)) and
                HumanEntryVerifications._is_not_full(board, int(position))):
                position = int(position)
                return (ColumnRecommendations(position,None), None)


class HumanEntryVerifications:
    @staticmethod
    def _is_int(cadena):
        try:
            num = int(cadena)
            return True
        except:
            return False

    @staticmethod
    def _is_not_full(board, col):
        return not board._columns[col].is_full()

    @staticmethod
    def _is_in_range(board, col):
        return 0 <= col < len(board)

class ReportingPlayer(Player):
    """
    Le pide al oraculo la mejor recomendación de su base de datos de recomendaciones
    """
    def _on_lose(self):
        self._oracle.back_track(self.last_moves)




