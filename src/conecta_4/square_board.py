from conecta_4.linear_board import LinearBoard
from conecta_4.settings import BOARD_LENGTH
from conecta_4.list_utils import *

class SquareBoard:
    """
    Lista de BOARD_LENGTH columnas LinearBoard.
    """

    @classmethod
    def from_list(cls, list_of_list):
        """
        Convierte a SquareBoard a partir de una matriz (LoL).
        Las listas recibidas no se copian, se reutilizan tal cual.
        """
        board = cls()
        board._columns = map_list(list_of_list, LinearBoard.from_list)
        return board

    @classmethod
    def from_str_board(cls, str_board):
        """
        Construye desde un str del tablero.
        str -> LinearBoard -> SquareBoard
        :param str_board: str moldeada tipo 'xo..|o...|....|....'
        :return: SquareBoard
        """
        list_of_strings = str_board.split('|')
        matrix = explode_list(list_of_strings)
        matrix = replace_all(matrix, '.', None)
        return cls.from_list(matrix)
    @classmethod
    def from_board_code(cls, board_code):
        """
        Construye desde un objeto BoardCode.
        Permite obtener una posición almacenada.
        """
        return cls.from_str_board(board_code.str_board)

    def __init__(self):
        self._columns = make_list_from_factory(BOARD_LENGTH, LinearBoard)
    def __repr__(self):
        return f'{self.__class__}:{self._columns}'
    def __len__(self):
        return len(self._columns)
    # Dos tableros con las mismas fichas son iguales.
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return self._columns == other._columns
    def __hash__(self):
        return hash(tuple(self._columns))

    def is_full(self):
        """
        True si todas las columnas están llenas. Sirve para detectar empate.
        """
        result = True
        for linear_board in self._columns:
            result = result and linear_board.is_full()
        return result
    def add(self, char, column):
        """
        Coloca una ficha char en column, aprovechándose de LinearBoard.add.
        """
        result = self._columns[column].add(char)
        return result
    def as_matrix(self):
        """
        Devuelve el tablero como matriz (LoL).
        Son las listas internas, no copias. Construir otro tablero con
        esta matriz haría que ambos compartieran memoria (aliasing).
        """
        result = []
        for column in self._columns:
            result.append(column._columns)
        return result
    def as_code(self):
        """
        Devuelve el BoardCode de la posición actual.
        """
        return BoardCode(self)

    def is_victory(self, char):
        """
        True si char tiene una racha ganadora en cualquiera de las 4 direcciones posibles.
        """
        return (self._any_vertical_victory(char) or
                self._any_descending_diagonal(char) or
                self._any_ascending_diagonal(char) or
                self._any_horizontal_victory(char))

    def _any_vertical_victory(self, char):
        """
        Pregunta a cada columna si tiene racha.
        """
        result = False
        for linear_board in self._columns:
            result = result or linear_board.is_victory(char)
        return result

    def _any_horizontal_victory(self, char):
        """
        Crea un tablero transpuesto y le pregunta por victorias verticales (H -> V).
        """
        #result = True
        transpose_matrix = transpose(self.as_matrix())
        transpose_board = SquareBoard.from_list(transpose_matrix)
        #for linear_board in transpose_board:
        #    result = result and linear_board.is_victory(char)
        return transpose_board._any_vertical_victory(char)

    def _any_descending_diagonal(self, char):
        """
        Desplaza filas (displace_matrix) y pregunta por victoria horizontal (Dv -> H -> V)
        """
        matrix = self.as_matrix()
        dm = displace_matrix(matrix)
        displace_board = SquareBoard.from_list(dm)
        return displace_board._any_horizontal_victory(char)

    def _any_ascending_diagonal(self, char):
        """
        Invierte cada columna, con lo que las diagonales ascendentes se
        convierten en descendentes, y pregunta por diagonal descendente (D^ -> Dv -> H -> V)
        """
        matrix = self.as_matrix()
        rm = reverse_matrix(matrix)
        reverse_board = SquareBoard.from_list(rm)
        return reverse_board._any_descending_diagonal(char)

class BoardCode:
    """
    Representación de una posición como cadena (ejemplo 'xo..|o...|....').
    Sirve como clave de la caché del oráculo y como jugada almacenable
    en un Move, ya que un SquareBoard cambia.
    """
    def __init__(self, board):
        self._str_board = colpase_matrix(board.as_matrix())

    @property
    def str_board(self):
        return self._str_board
    # Dos códigos con el mismo texto son el mismo código.
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return self._str_board == other.str_board
    def __hash__(self):
        return hash(self._str_board)
    def __repr__(self):
        return f'{self._str_board}:{self.__class__}'
