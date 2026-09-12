import pytest

from conecta_4.settings import BOARD_LENGTH
from conecta_4.oracle import *
from conecta_4.square_board import SquareBoard
from conecta_4.player import *


def test_base_oracle():
    board = SquareBoard.from_list([[None, None, None, None],
                                  ['x', 'o', 'x', 'o'],
                                  ['o', 'o', 'x', 'x'],
                                  ['o', None, None, None]])

    expected = [ColumnRecommendations(0, ColumnClassification.MAYBE),
                ColumnRecommendations(1, ColumnClassification.FULL),
                ColumnRecommendations(2, ColumnClassification.FULL),
                ColumnRecommendations(3, ColumnClassification.MAYBE)]

    rappel = BaseOracle()

    assert len(rappel._get_recommendation(board, None)) == len(expected)
    assert rappel._get_recommendation(board, None) == expected


def test_equality():
    cr = ColumnRecommendations(2, ColumnClassification.MAYBE)

    assert cr == cr  # SON INDÉNTICOS
    assert cr == ColumnRecommendations(2, ColumnClassification.MAYBE)  # SON EQUIVALENTES

    # NO EQUIVALENTES

    assert cr != ColumnRecommendations(2, ColumnClassification.FULL)
    assert cr != ColumnRecommendations(3, ColumnClassification.FULL)

    # DOS OBJETOS EQUIVALES DEBEN DE TENER EL MISMO HASH. SI IMPLEMENTAMOS
    # METODO __EQ__ HAY QUE IMPLEMENTAR EL MÉTODO __HASH__


def test_hash():
    cr = ColumnRecommendations(2, ColumnClassification.MAYBE)
    assert hash(cr) == hash(ColumnRecommendations(2, ColumnClassification.MAYBE))


def test_is_winning_move():
    winner = Player('Xavier', 'x')
    loser = Player('Otto', 'o')

    empty = SquareBoard()
    almost = SquareBoard.from_list([['o', 'x', 'o', None],
                                   ['o', 'x', 'o', None],
                                   ['x', None, None, None],
                                   [None, None, None, None]])
    oracle = SmartOracle()

    for i in range(0, BOARD_LENGTH):
        assert oracle._is_winning_bet(empty, i, winner) == False
        assert oracle._is_winning_bet(empty, i, loser) == False

    for i in range(0, BOARD_LENGTH):
        assert oracle._is_winning_bet(almost, i, loser) == False

    assert oracle._is_winning_bet(almost, 2, winner)

# 1. La jugada guardada NO debe estar en el tablero guardado
def test_move_guarda_el_tablero_previo():
    p = Player('A', char='x', oracle=BaseOracle())
    b = SquareBoard()
    p.play(b)
    mv = p.last_moves[0]
    previo = SquareBoard.from_board_code(mv.board_code)
    assert previo._columns[mv.position].get_columns()[0] is None

# 2. Tras marcar BAD, esa columna deja de recomendarse
def test_to_bad_cambia_la_recomendacion():
    o = LearningOracle()
    x = Player('x', char='x'); Player('o', char='o', opponent=x)
    b = SquareBoard()
    antes = o._get_recommendation(b, x)
    mv = Move(2, b.as_code(), antes, x)
    o.to_bad(mv)
    despues = o._get_recommendation(b, x)
    assert despues[2].classification == ColumnClassification.BAD
