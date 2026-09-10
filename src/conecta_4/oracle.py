from enum import Enum
from conecta_4.square_board import *
from conecta_4.settings import BOARD_LENGTH
from copy import deepcopy

class ColumnClassification(Enum):
    FULL = -1
    MAYBE = 10
    WIN = 100
    LOSE = 1
    BAD = 5

class ColumnRecommendations:
    """
    Recomendación del oráculo sobre una columna concreta con índice y clasificación.
    """
    def __init__(self, index, classification):
        self.index = index
        self.classification = classification
    # "Iguales" aquí significa empatar en puntuación, no ser la misma columna ni hash(a)==hash(b).
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return self.classification == other.classification
    def __hash__(self):
        return hash ((self.index, self.classification))
    def __repr__(self):
        return f'{self.__class__}: {self.classification}'

class BaseOracle:
    """
    Solo distingue columnas llenas de columnas jugables, juega al azar.
    """

    def _get_recommendation(self, board, player):
        """
        Obtenemos recomendaciones por column y las guardamos en una lista.
        :param board: SquareBoard a evaluar
        :param player: jugador para el que se evalúa
        :return: lista con una ColumnRecommendations por columna
        """
        result = [] #[(0, FULL), (1, MAYBE), (2, FULL), (3, MAYBE)]
        for i in range(len(board)):
            result.append(self._get_columns_recommendations(board, i, player))
        return result

    def _get_columns_recommendations(self, board, i, player):
        """
        Evalúa una elección de columna en llena o posible.
        """
        classification = ColumnClassification.MAYBE
        if board._columns[i].is_full():
            classification = ColumnClassification.FULL
        return ColumnRecommendations(i, classification)

    #Para Learning Oracle. Tenemos que clasificar entre buena o mal
    def full_or_win(self, board, player):
        """
        True si en esta posición NO queda ninguna opción buena posible, es decir, si la jugada estaba forzada.
        Lo usa back_track para decidir si sigue retrocediendo o se para.
        :param board: SquareBoard
        :param player: jugador
        :return: bool
        """
        recomendaciones = self._get_recommendation(board, player)
        result = True
        for recomendacion in recomendaciones:
            if(recomendacion.classification == ColumnClassification.WIN) or (recomendacion.classification == ColumnClassification.MAYBE):
                result = False
                break
        return result

    def back_track(self, list_of_moves):
        """
        Hook para LearningOracle.back_track.
        """
        pass
    def to_bad(self, move):
        """
        Igual que con back_track.
        """
        pass

class SmartOracle(BaseOracle):
    """
    Añade una jugada ("ronda") de anticipación al detectar jugadas perdedoras o ganadoras.
    """

    def _get_columns_recommendations(self, board, i, player):
        """
        Hereda de BaseOracle y si la columna es jugable, la mete a WIN o LOSE simulando la jugada.
        """
        recommendations = super()._get_columns_recommendations(board, i, player)
        if recommendations.classification == ColumnClassification.MAYBE:
            if self._is_winning_bet(board, i, player):
                recommendations.classification = ColumnClassification.WIN
            elif self._is_losing_bet(board, i, player):
                recommendations.classification = ColumnClassification.LOSE
        return recommendations
    #Para verlo, vamos a crear un tablero temporal con deepcopy y jugar en el
    def _play_on_temporal_board(self, board, index, player):
        """
        Juega sobre una deepcopy.
        """
        temporal_board = deepcopy(board)
        temporal_board.add(player.char, index)
        return temporal_board

    #vamos a ver si gana la jugada en el tablero temporal
    def _is_winning_bet(self, board, index, player):
        """
        True si jugar en index da la victoria inmediata al player. Simula tablero.
        """
        temporal_bet = self._play_on_temporal_board(board, index, player)
        return temporal_bet.is_victory(player.char)

    #vamos a ver si pierde la jugada en el tablero temporal
    def _is_losing_bet(self, board, index, player):
        """
        True si tras jugar en index el rival puede ganar en su turno
        siguiente en alguna columna. Simula tablero.
        """
        temporal_bet = self._play_on_temporal_board(board, index, player)
        losing_bet = False
        for i in range(0, BOARD_LENGTH):
            if self._is_winning_bet(temporal_bet, i, player.opponent):
                losing_bet = True
                break
        return losing_bet

class MemoizationOracle(SmartOracle):
    """
    MEmoiza el _get_recommendation.
    """
    def __init__(self):
        super().__init__()
        # Caché: clave 'codigo_del_tablero@ficha' -> lista de recomendaciones.
        self.memo_recommendations = {}

    def _make_key(self, board_code, player):
        """
        Construye la clave de la caché.
        """
        return f'{board_code.str_board}@{player.char}' # x..o|xx.o|....@o

    def _get_recommendation(self, board, player):
        """
        Si la posición ya está en la caché la devuelve; si no, la calcula
        con la lógica heredada del Smart y la guarda.
        :param board: SquareBoard
        :param player: jugador
        :return: lista de ColumnRecommendations
        """
        key = self._make_key(board.as_code(), player)
        #Para cachear primero hay que mirar la caché y ver si no está
        if key not in self.memo_recommendations:
            self.memo_recommendations[key] = super()._get_recommendation(board, player)
        return self.memo_recommendations[key]

class LearningOracle(MemoizationOracle):
    """
    Reclasifica y mira hacia atrás (back_track).
    La caché pasa a ser la memoria del programa para guardar jugadas BAD.
    """
    def to_bad(self, move):
        """
        Marca como BAD la columna jugada en ese Move, reescribiendo la entrada correspondiente de la caché.
        """
        #Crear la clave
        key = self._make_key(move.board_code, move.player)
        #Reclasificamos
        recomendaciones = self._get_recommendation(
            SquareBoard.from_board_code(move.board_code), move.player)
        recomendaciones[move.position] = ColumnRecommendations(move.position, ColumnClassification.BAD)
        #Sustituimos en nuestro dict la recomendación
        self.memo_recommendations[key] = recomendaciones

    def back_track(self, list_of_moves):
        """
        Repasa las jugadas y las reclasifica.
        La lista viene de la más reciente a la más antigua. Se detiene cuando encuentra
        una posición donde se incumplen requisitos de full_or_win.
        :param list_of_moves: jugadas del jugador que ha perdido
        :return: None
        """
        for move in list_of_moves:
            self.to_bad(move)
            board = SquareBoard.from_board_code(move.board_code)
            if not self.full_or_win(board, move.player):
                break
