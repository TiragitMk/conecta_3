from conecta_4.linear_board import LinearBoard
from conecta_4.settings import BOARD_LENGTH
from conecta_4.list_utils import *

class SquareBoard:
    @classmethod
    def from_list(cls, list_of_list):
        board = cls()
        board._columns = map_list(list_of_list, LinearBoard.from_list)
        return board
    @classmethod
    def from_str_board(cls, str_board):
        """
        str -> LinearBoard -> SquareBoard
        :param str_board:
        :return:
        """
        #Tokenizamos
        list_of_strings = str_board.split('|')
        #Vamos a crear una lista de listas
        matrix = explode_list(list_of_strings)
        #Cambiamos '.' por None
        matrix = replace_all(matrix, '.', None)
        #Transformamos a SquareBoard
        return cls.from_list(matrix)
    @classmethod
    def from_board_code(cls, board_code):
        return cls.from_str_board(board_code.str_board)

    #Dunders. Que cosas le puede preguntar python
    def __init__(self):
        self._columns = make_list_from_factory(BOARD_LENGTH, LinearBoard)
    def __repr__(self):
        return f'{self.__class__}:{self._columns}'
    def __len__(self):
        return len(self._columns)
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return self._columns == other._columns
    def __hash__(self):
        return hash(tuple(self._columns))
    #Metodos. Qué cosas puede hacer mi clase
    def is_full(self):
        result = True
        for linear_board in self._columns:
            result = result and linear_board.is_full()
        return result
    def add(self, char, column):
        result = self._columns[column].add(char)
        return result
    def as_matrix(self):
        result = []
        for column in self._columns:
            result.append(column._columns)
        return result
        #return map_list(self._columns, LinearBoard.get_columns)
    def as_code(self):
        return BoardCode(self)

    def is_victory(self, char):
        return (self._any_vertical_victory(char) or
                self._any_descending_diagonal(char) or
                self._any_ascending_diagonal(char) or
                self._any_horizontal_victory(char))

    def _any_vertical_victory(self, char):
        result = False
        for linear_board in self._columns:
            result = result or linear_board.is_victory(char)
        return result

    def _any_horizontal_victory(self, char):
        #result = True
        transpose_matrix = transpose(self.as_matrix())
        transpose_board = SquareBoard.from_list(transpose_matrix)
        #for linear_board in transpose_board:
        #    result = result and linear_board.is_victory(char)
        return transpose_board._any_vertical_victory(char)

    def _any_descending_diagonal(self, char):
        matrix = self.as_matrix()
        dm = displace_matrix(matrix)
        displace_board = SquareBoard.from_list(dm)
        return displace_board._any_horizontal_victory(char)

    def _any_ascending_diagonal(self, char):
        matrix = self.as_matrix()
        rm = reverse_matrix(matrix)
        reverse_board = SquareBoard.from_list(rm)
        return reverse_board._any_descending_diagonal(char)

class BoardCode:
    def __init__(self, board):
        self._str_board = colpase_matrix(board.as_matrix())
    @property
    def str_board(self):
        return self._str_board
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return self._str_board == other.str_board
    def __hash__(self):
        return hash(self._str_board)
    def __repr__(self):
        return f'{self._str_board}:{self.__class__}'






