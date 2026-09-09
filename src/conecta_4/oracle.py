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
    def __init__(self, index, classification):
        self.index = index
        self.classification = classification
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return self.classification == other.classification
    def __hash__(self):
        return hash ((self.index, self.classification))
    #Si quiero imprimir las recomendaciones que me está dando necesito un __repr__
    def __repr__(self):
        return f'{self.__class__}: {self.classification}'

class BaseOracle:

    def _get_recommendation(self, board, player):
        """
        Obtenemos recomenciones por column y las guardamos en una lista
        :param board:
        :param player:
        :return:
        """
        result = [] #[(0, FULL), (1, MAYBE), (2, FULL), (3, MAYBE)]
        for i in range(len(board)):
            result.append(self._get_columns_recommendations(board, i, player))
        return result

    def _get_columns_recommendations(self, board, i, player):
        classification = ColumnClassification.MAYBE
        if board._columns[i].is_full():
            classification = ColumnClassification.FULL
        return ColumnRecommendations(i, classification)

    #Para Learning Oracle. Tenemos que clasificar entre buena o mal
    def full_or_win(self, board, player):
        """
        Distinguimos entre full o win
        :param board:
        :param player:
        :return:
        """
        #Genero las recomendaciones
        recomendaciones = self._get_recommendation(board, player)
        #Detectamos las recomendaciones
        result = True
        for recomendacion in recomendaciones:
            if(recomendacion.classification == ColumnClassification.WIN) or (recomendacion.classification == ColumnClassification.MAYBE):
                result = False
                break
        return result
    #Hacer un hook
    def back_track(self, list_of_moves):
        pass
    def to_bad(self, move):
        pass

class SmartOracle(BaseOracle):
    #Ver si estamos si al poner en el MAYBE se gana o se pierde
    def _get_columns_recommendations(self, board, i, player):
        recommendations = super()._get_columns_recommendations(board, i, player)
        if recommendations.classification == ColumnClassification.MAYBE:
            if self._is_winning_bet(board, i, player):
                recommendations.classification = ColumnClassification.WIN
            elif self._is_losing_bet(board, i, player):
                recommendations.classification = ColumnClassification.LOSE
        return recommendations
    #Para verlo, vamos a crear un tablero temporal con deepcopy y jugar en el
    def _play_on_temporal_board(self, board, index, player):
        temporal_board = deepcopy(board)
        temporal_board.add(player.char, index)
        return temporal_board

    #vamos a ver si gana la jugada en el tablero temporal
    def _is_winning_bet(self, board, index, player):
        temporal_bet = self._play_on_temporal_board(board, index, player)
        return temporal_bet.is_victory(player.char)

    #vamos a ver si pierde la jugada en el tablero temporal
    def _is_losing_bet(self, board, index, player):
        temporal_bet = self._play_on_temporal_board(board, index, player)
        losing_bet = False
        for i in range(0, BOARD_LENGTH):
            if self._is_winning_bet(temporal_bet, i, player.opponent):
                losing_bet = True
                break
        return losing_bet

class MemoizationOracle(SmartOracle):
    """
    Vamos a memorizar el get_recommendation
    """
    def __init__(self):
        super().__init__()
        self.memo_recommendations = {}

    def _make_key(self, board_code, player):
        return f'{board_code.str_board}@{player.char}' # x..o|xx.o|....@o

    def _get_recommendation(self, board, player):
        """
        Vamos a memorizar el get_recommendation
        :param board:
        :param player:
        :return:
        """
        key = self._make_key(board.as_code(), player)
        #Para cachear primero hay que mirar la caché y ver si no está
        if key not in self.memo_recommendations:
            self.memo_recommendations[key] = super()._get_recommendation(board, player)
        return self.memo_recommendations[key]

class LearningOracle(MemoizationOracle):
    """
    Va a hacer dos cosas: Reclasificar y mirar hacia atrás (back_track)
    """
    def to_bad(self, move):
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
        Repasa las jugadas y las reclasifica
        :param list_of_moves:
        :return:
        """
        for move in list_of_moves:
            self.to_bad(move)
            board = SquareBoard.from_board_code(move.board_code)
            if not self.full_or_win(board, move.player):
                break



























