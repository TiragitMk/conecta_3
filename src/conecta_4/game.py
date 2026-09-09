import pyfiglet
from beautifultable import BeautifulTable

from enum import auto

from conecta_4.match import *
from conecta_4.player import *
from conecta_4.list_utils import *

class RoundType(Enum):
    Human_vs_Computer = auto()
    Computer_vs_Computer = auto()

class Level(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

class Game:
    def __init__(self):
        #Más adelante deberemos guardar algunos datos

        #Inicializamos con un square_board
        self.board = SquareBoard()

    def start_game(self):
        self._print_logo()
        self._configuration()
        self._game_loop()

    def _print_logo(self):
        """
        Imprime logo del juego
        :return:
        """
        logo = pyfiglet.Figlet(font = "swamp_land")
        print(logo.renderText("Conecta 4"))

    def _configuration(self):
        """
        Configuración pedida al usuario
        :return:
        """
        #Pedimos un tipo de ronda
        self.round_type = self._get_round_type()
        #Pedimos un nivel de dificultad
        if self.round_type == RoundType.Human_vs_Computer:
            self._difficulty_level = self._get_level()
        #Pedimos un nombre de usuario. Lo podeis hace aqui o al crear la partida
        #Se crea la partida
        self.match = self._match()


    def _get_round_type(self):
        """
        Usuario setea las opciones disponibles de rondas
        :return:
        """
        print("""
        Selecciona las opciones disponibles:
        
        1) Humano vs Computadora
        2) Computer vs Computadora
        """)
        respuesta = ""
        while respuesta != '1' and respuesta != '2':
            respuesta = input('Selecciona 1 ó 2: ')
        if respuesta == '1':
            return RoundType.Human_vs_Computer
        else:
            return RoundType.Computer_vs_Computer

    def _get_level(self):
        """
        Usuario setea las opciones disponibles de dificultad
        :return:
        """
        print("""
        Selecciona las opciones disponibles:

        1) Fácil
        2) Intermedio
        3) Difícil
        """)
        while True:
            repuesta = input("Selecciona entre 1, 2 ó 3: ")
            if repuesta == '1':
                level = Level.LOW
                break
            elif repuesta == '2':
                level = Level.MEDIUM
                break
            elif repuesta == '3':
                level = Level.HIGH
                break
        return level

    def _match(self):
        """
        Creamos los dos jugadores. El primero siempre va a ser ordenador
        :return:
        """
        _levels = {Level.LOW: BaseOracle(),
                   Level.MEDIUM : SmartOracle(),
                   Level.HIGH : LearningOracle()}
        if self.round_type == RoundType.Computer_vs_Computer:
            player1 = ReportingPlayer('Ordenador 1', oracle=LearningOracle())
            player2 = ReportingPlayer('Ordenador 2', oracle=LearningOracle())
        else:
            player1 = ReportingPlayer('Computer', oracle=_levels[self._difficulty_level]) #Posible bug # Resolución bug: Es _difficulty_level
            player2 = HumanPlayer(name = input('Ingrese su nombre: '))
        return Match(player1, player2)


    def _game_loop(self):
        """
        hace el bucle de eventos
        :return:
        """
        #Bucle inifinito.
        while True:
            #Seleccionamos el jugador
            jugador_actual = self.match.get_next_player
            #Una vez con el juagador lo mandamos a jugar
            jugador_actual.play(self.board)
            #Muestro la jugada
            self._print_move(jugador_actual)
            #Muestro el tablero
            self._print_board()
            # Evaluamos el tablero. ¿Algún vencedor? ¿Empate?
            if self._winner_or_tie():
                #Muestro resultado
                self._print_result()
                #Pregunto si le apetece otra partida
                if self.match.play_more():
                    self.board = SquareBoard()
                    self._print_board()
                else:
                    break

    def _print_board(self):
        """
        Imprime tablero
        :return:
        """
        #Covertimos tablero en una matriz y le damos la vuelta
        board_matrix = reverse_matrix(self.board.as_matrix())
        bt = BeautifulTable()
        for col in board_matrix:
            bt.columns.append(col)
        bt.columns.header = [str(i) for i in range(BOARD_LENGTH)]

        #Imprimimos la tabla
        print(bt)

    def _print_result(self):
        ganador = self.match.get_winner(self.board)
        perdedor = self.match.get_loser(self.board)
        if ganador is not None:
            print(f'{ganador.name} ({ganador.char}) GANA VS {perdedor.name} ({perdedor.char})')
        else:
            print('EMPATE')



    def _print_move(self, player):
        """
        Muestra por pantalla la juagada de player
        :param player:
        :return:
        """
        print(f'{player.name} ({player.char} ha movido en {player.last_moves[0].position})')

    def _winner_or_tie(self):
        """
        El juego termina y vemos si hay un empate o un ganador
        :return:
        """
        ganador = self. match.get_winner(self.board)
        if ganador is not None:
            ganador.opponent._on_lose()
            return True
        elif self.board.is_full():
            return True
        else:
            return False





