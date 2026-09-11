from conecta_4.settings import BOARD_LENGTH, VICTORY_STRIKE
from conecta_4.list_utils import find_strike, make_list, index_first_element

class LinearBoard:
    """
    Representamos una sola columna.
    Fichas "x" y "o", vacío es None.
    """
    @classmethod
    def from_list(cls, data):
        """
        Crea una columna LinearBoard a partir de una lista ya hecha.
        Se queda con la lista recibida, no hace copia.
        :param data: lista de caracteres de la columna
        :return: LinearBoard
        """
        board = cls()
        board._columns = data
        return board

    def __init__(self):
        # Crea columna vacía.
        self._columns = make_list(BOARD_LENGTH, None)

    # Dos columnas son iguales si tienen el mismo contenido.
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return self._columns == other._columns

    def __hash__(self):
        return hash(tuple(self._columns))

    #Cosas que puede hacer
    def get_columns(self):
        """
        Devuelve la lista interna de casillas (no una copia): modificarla
        modifica la columna.
        :return: lista de caracteres de la columna
        """
        return self._columns

    def is_full(self):
        return self._columns[-1] is not None

    def add(self, char):
        """
        Coloca una ficha en la primera casilla libre empezando por abajo (simula gravedad).
        :param char: ficha del personaje que añade
        :return: None
        """
        if not self.is_full():
            i = index_first_element(self._columns, None)
            # i = self._column.index(None)
            self._columns[i] = char

    def is_victory(self, char):
        """
        True si hay VICTORY_STRIKE fichas consecutivas de char en la columna.
        :param char: ficha del personaje que añade
        """
        return find_strike(self._columns, char, VICTORY_STRIKE)

    def is_tie(self, char_1, char_2):
        """
        Predicado que determina el empate.
        :param char_1: Ficha del personaje 1
        :param char_2: Ficha del personaje 2
        :return: bool
        """
        return ((self.is_victory(char_1) == False) and
                (self.is_victory(char_2) == False))
