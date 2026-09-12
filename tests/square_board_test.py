import pytest
from conecta_4.square_board import *

def test_empty_board():

    board = SquareBoard()

    assert len(board) == BOARD_LENGTH
    for column in board._columns:
        assert isinstance(column, LinearBoard)
    assert board._columns[0] is not board._columns[1]
    assert board.is_full() == False
    assert board.is_victory('o') == False
    assert board.is_victory ('x') == False

def test_from_list_as_matrix():
    matrix = [['x', None, None, None], ['o', 'x', None, None], [None] * 4, [None] * 4]
    board = SquareBoard.from_list(matrix)
    assert board.as_matrix() == matrix

def test_from_board_code():
    original = SquareBoard.from_str_board('xo..|o...|x...|....')
    rebuilt = SquareBoard.from_board_code(original.as_code())
    assert isinstance(rebuilt, SquareBoard)
    assert rebuilt == original
    assert rebuilt is not original
    assert rebuilt.as_matrix()[0] is not original.as_matrix()[0]
    rebuilt.add('x', 3)
    assert rebuilt != original
    assert SquareBoard.from_board_code(SquareBoard().as_code()) == SquareBoard()

def test_horizontal_victory():
    horizontal = SquareBoard.from_list([['x', None, None, None, None, None, ],
                                     ['x', None, None, None, None, None, ],
                                     ['x', 'x', 'x', None, None, None, ],
                                     ['x', 'o', 'o', None, None, None, ],
                                     ['x', 'o', 'o', None, None, None, ]])
    assert horizontal.is_victory('x')
    assert horizontal.is_victory('o') == False

def test_vertical_victory():
    vertical =  SquareBoard.from_list([['x', 'x', 'x', 'x', 'o', ],
                                     [None, None, None, None, None, ],
                                     [None, None, None, None, None, ],
                                     [None, None, None, None, None, ],
                                     [None, None, None, None, None, ]])
    assert vertical.is_victory('x')
    assert vertical.is_victory('o') == False

def test_sinking_victory():
    vertical =  SquareBoard.from_list([['x', 'o', 'x', 'o',  ],
                                     ['x', 'x', 'o', None,  ],
                                     ['o', 'o', None, None,  ],
                                     ['o', 'x', None, None,  ],
                                     ['x', None, None, None,  ]])
    assert vertical.is_victory('x') == False
    assert vertical.is_victory('o')

def test_rising_victory():
    vertical =  SquareBoard.from_list([['o', 'o', None, None,  ],
                                     ['o', 'x', None, None,  ],
                                     ['x', 'o', 'x', 'o',  ],
                                     ['x', 'o', 'x', 'x',  ],
                                     ['o', 'x', 'o', None,  ]])
    assert vertical.is_victory('x')
    assert vertical.is_victory('o') == False