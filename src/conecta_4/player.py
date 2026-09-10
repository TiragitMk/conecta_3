from random import choice

from conecta_4.oracle import *
from conecta_4.square_board import *
from conecta_4.move import *
from conecta_4.settings import BOARD_LENGTH

class Player:
    """
    Jugador máquina. No decide por sí mismo, pregunta a su oráculo y elige entre las recomendaciones.
    """
    def __init__(self, name, char = None, oracle = BaseOracle(), opponent = None):
        self.name = name
        self.char = char
        self._oracle = oracle
        self.opponent = opponent

        # Jugadas de la partida, de la más reciente a la más antigua.
        self.last_moves = []

    @property
    def opponent(self):
        """
        Rival de este player. Lo necesita SmartOracle para simular la respuesta del contrario.
        """
        return self._opponent
    @opponent.setter
    def opponent(self, other):
        self._opponent = other
        if other is not None:
            other._opponent = self

    def play(self, board):
        """
        Elige la mejor columna donde jugar de las recomendaciones del oráculo.
        :param board: SquareBoard
        :return: None
        """
        (best, recommendations) = self._ask_oracle(board)
        self._play_on(board, best.index, recommendations)

    def _play_on(self, board, position, recommendations ):
        """
        Juega en la posición elegida de las jugadas recomendadas y registra la jugada en last_moves.
        Anteriormente registraba el tablero después de jugar, se ha modificado para registrarla al momento de decidir.
        :param board: SquareBoard
        :param position: columna elegida
        :param recommendations: recomendaciones que había al decidir
        :return: None
        """
        self.last_moves.insert(0, Move(position, board.as_code(), recommendations, self))
        board.add(self.char, position)

    def _ask_oracle(self, board):
        """
        Pregunta al oráculo para que devuelva las jugadas posibles.
        Devuelve una tupla (mejor recomendación, lista completa).
        :param board: SquareBoard
        :return: (ColumnRecommendations, list)
        """
        recommendations = self._oracle._get_recommendation(board, self)
        best = self._choose_a_recommendation(recommendations)
        return (best, recommendations)

    def _choose_a_recommendation(self, recommendations):
        """
        Elige una de las recomendaciones que da el oráculo.
        Descarta las columnas llenas, ordena por puntuación de mayor a menor y si todas empatan, sortea al azar.
        :param recommendations: lista de ColumnRecommendations
        :return: ColumnRecommendations
        """
        valid_recommendations = list(filter(lambda x:
                                            x.classification != ColumnClassification.FULL,
                                            recommendations))
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
    Esta clase no se testea porque son valores introducidos por el usuario, aunque se pueden testear valores.
    Solo cambia de dónde sale la jugada (el oráculo es el humano), el resto lo hereda directamente.
    """
    def __init__(self, name, char = None):
        # No recibe oráculo: se queda con el BaseOracle por defecto, que nunca usa.
        super().__init__(name, char)

    def _ask_oracle(self, board):
        """
        Pide input al "oráculo humano". No hace falta que clasifique (None).
        :param board: SquareBoard
        :return: (ColumnRecommendations, None)
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
    """
    Agrupa las validaciones de la entrada por teclado.
    No guarda estado, por eso todos sus métodos son estáticos y nunca se crean instancias de esto.
    """
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
    Le pide al oraculo la mejor recomendación de su base de datos de recomendaciones.
    Es el jugador que aprende, al perder avisa a su oráculo.
    """
    def _on_lose(self):
        """
        Sobrescribe el hook pasando las jugadas de la partida al oráculo para
        que las reclasifique. Si el oráculo no sabe aprender, back_track tampoco hace nada.
        """
        self._oracle.back_track(self.last_moves)
