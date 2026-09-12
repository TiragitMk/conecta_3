import pytest

from conecta_4.linear_board import *
from conecta_4.settings import VICTORY_STRIKE, BOARD_LENGTH

def test_empty_board():
    empty = LinearBoard()
    assert empty is not None
    assert empty.is_full() == False
    assert empty.is_victory('x') == False
    assert empty.get_columns() == [None] * BOARD_LENGTH
    assert len(empty.get_columns()) == BOARD_LENGTH

def test_from_list():
    # LinearBoard ES data.
    data = ['x', 'o', None, None]
    board = LinearBoard.from_list(data)
    assert board.get_columns() == ['x', 'o', None, None]
    assert board.get_columns() is data
    data[2] = 'x'
    assert board.get_columns()[2] == 'x'
    assert LinearBoard.from_list([]).get_columns() == []

def test_equality():
    assert LinearBoard() == LinearBoard()
    assert LinearBoard.from_list(['x', None, None, None]) == LinearBoard.from_list(['x', None, None, None])
    assert LinearBoard.from_list(['x', None, None, None]) != LinearBoard.from_list(['o', None, None, None])
    assert LinearBoard.from_list(['x', 'o', None, None]) != LinearBoard.from_list(['o', 'x', None, None])
    assert LinearBoard() != [None] * BOARD_LENGTH
    assert LinearBoard() != None

def test_add_full():
    # Este test asume que el tablero siempre es simétrico, pues BOARD_LENGTH también es altura.
    board = LinearBoard()
    for i in range(BOARD_LENGTH):
        assert not board.is_full()
        board.add('x')
        assert board != LinearBoard()
    assert board.is_full()

def test_add_get_columns():
    board = LinearBoard()
    board.add('x')
    assert board.get_columns() == ['x', None, None, None]
    board.add('o')
    assert board.get_columns() == ['x', 'o', None, None]
    board.add('x')
    board.add('o')
    assert board.get_columns() == ['x', 'o', 'x', 'o']
    board.add('x')
    assert board.get_columns() == ['x', 'o', 'x', 'o']
    assert len(board.get_columns()) == BOARD_LENGTH

def test_victory():
    board = LinearBoard()
    for i in range(VICTORY_STRIKE):
        board.add('x')
    assert board.is_victory('o') == False
    assert board.is_victory('x') == True

def test_tie():
    board = LinearBoard()

    board.add('o')
    board.add('o')
    board.add('x')
    board.add('o')

    assert board.is_tie ('x', 'o')



