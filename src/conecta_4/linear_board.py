from conecta_4.settings import BOARD_LENGTH, VICTORY_STRIKE
from conecta_4.list_utils import find_strike, make_list, index_first_element

class LinearBoard:
    """
    Representamos una sola columna.
    Los jugadores son:
    - Jugador 1 : x
    - Jugador 2 : o
    - Las posiciones vacías van a ser None
    """
    @classmethod
    def from_list(cls, data):
        board = cls()
        board._columns = data
        return board

    #Dunders. Cosas que yo le puedo preguntar
    def __init__(self):
        self._columns = make_list(BOARD_LENGTH, None)
        # [None for i in range(BOARD_LENGTH)]

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        else:
            return self._columns == other._columns

    def __hash__(self):
        return hash(tuple(self._columns))

    #Cosas que puede hacer
    def get_columns(self):
        return self._columns

    def is_full(self):
        """
        Pregunto si el último valor es un None
        """
        return self._columns[-1] is not None

    def add(self, char):
        if not self.is_full():
            i = index_first_element(self._columns, None)
            # i = self._column.index(None)
            self._columns[i] = char

    def is_victory(self, char):
        return find_strike(self._columns, char, VICTORY_STRIKE)

    def is_tie(self, char_1, char_2):
        return ((self.is_victory(char_1) == False) and
                (self.is_victory(char_2) == False))










