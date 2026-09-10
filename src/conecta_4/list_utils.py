# Funciones puras sobre listas y matrices.

def find_n(elements, needle, n):
    """
    Devuelve True si en elements hay n o más ocurrencias de needle, no necesariamente consecutivas.
    :param elements: list
    :param needle: int
    :param n: int
    :return: bool
    """
    if n >= 0:
        index = 0
        count = 0
        while count < n and index < len(elements):
            if needle == elements[index]:
                count += 1
            index += 1
        return count >= n
    else:
        return False

def find_one(elements, needle):
    """
    find_n para buscar una sola ocurrencia. Igual, pero n=1 constante.
    """
    return find_n(elements, needle, 1)

def find_strike(elements, needle, n):
    """
    Devuelve True si hay n ocurrencias consecutivas (streak) de needle.
    Es la función que decide si hay victoria.
    :param elements:
    :param needle:
    :param n:
    :return:
    """
    if n >= 0:
        index = 0
        count = 0
        while count < n and index < len(elements):
            if needle == elements[index]:
                count += 1
            else:
                count = 0
            index += 1
        return count >= n
    else:
        return False

def make_list(length, filler):
    """
    Crea una lista de longitud length repitiendo filler.
    Actualmente se usa con None, si el objeto fuera mutable podrían compartir objeto (aliasing).
    :param length: int
    :param filler:
    :return: list
    """
    result = []
    index = 0
    while index < length:
        result.append(filler)
        index += 1
    return result

def index_first_element(elements, needle):
    """
    Devuelve el índice de la primera aparición de needle, o None si no está.
    :param elements: list
    :param needle:
    :return: int o None
    """
    index = 0
    while index < len(elements):
        if needle == elements[index]:
            return index
        else:
            index += 1
    return None

def map_list(elements, transform):
    """
    Creo una lista nueva aplicando transform a cada elemento
    :param elements: list
    :param transform: function
    :return: list
    """
    result = []
    for element in elements:
        result.append(transform(element))
    return result

def make_list_from_factory(length, factory):
    """
    Crea una lista llamando a factory() una vez por posición.
    Se diferencia de make_list en que aquí cada elemento es un objeto NUEVO,
    que es lo que hace falta para las columnas del tablero.
    :param length: int
    :param factory: function
    :return: list
    """
    result = []
    index = 0
    while index < length:
        result.append(factory())
        index += 1
    return result

def transpose(matrix):
    """
    Intercambia filas y columnas. Funciona con matrices no cuadradas.
    Convierte el problema de "victoria horizontal" en uno vertical.
    Devuelve listas nuevas.
    :param matrix: list
    :return: list
    """
    if not matrix:
        return []
    height = len(matrix[0])
    result = []
    for i in range(height):
        sub_result = []
        for j in range(len(matrix)):
            sub_result.append(matrix[j][i])
        result.append(sub_result)
    return result

def displace(l, distancia, filler = None):
    """
    Desplaza los elementos de una lista, rellenando los huecos con filler.
    Lo que se sale por los extremos se pierde. La longitud no cambia.
    :param l: list
    :param distancia: int
    :param filler:
    :return: list
    """
    n = len(l)
    result = []
    for i in range(n):
        index = i - distancia
        if 0 <= index < n:
            result.append(l[index])
        else:
            result.append(filler)
    return result

def displace_matrix(matrix, filler = None):
    """
    Desplaza cada columna i una cantidad i-1.
    Las diagonales descendentes pasan a ser filas, por lo que se pueden buscar como victorias horizontales.
    :param matrix: list
    :param filler:
    :return: list
    """
    d = []
    for i in range(len(matrix)):
        d.append(displace(matrix[i], i - 1, filler))
    return d

def reverse_list(elements):
    """
    Se usa en reverse_matrix.
    :param elements: list
    :return: list
    """
    return elements[::-1]

def reverse_matrix(matrix):
    """
    Invierte la matriz. Se usa para: convertir diagonales ascendentes en descendentes,
    y poner el tablero derecho antes de imprimirlo.
    """
    result = []
    for col in matrix:
        result.append(reverse_list(col))
    return result

def all_the_same_score(elements):
    """
    Devuelve True si todos los elementos son iguales entre sí, o sea misma clasificación según __eq__.
    No controla lista vacía.
    :param elements: list
    :return: bool
    """
    if not elements:
        return True
    first_element = elements[0]
    result = True
    for element in elements:
        if element != first_element:
            result = False
    return result

def colpase_matrix(matrix, empty = '.', sep = '|'):
    """
    Convierte la matriz del tablero en una sola cadena siguiendo un molde.
    Cada columna se separa con sep, las celdas vacías son empty.
    Es importante conservar estos valores predeterminados, otras funciones usan los mismos.
    Podrían convertirse en una constante.
    :param matrix: list
    :param empty: "."
    :param sep: "|"
    :return: str
    """
    result = ''
    for elt in matrix:
        result = result + sep + colapse_list(elt, empty)
    return result[1:]

def colapse_list(elements, empty = '.'):
    """
    Convierte una columna en texto: None se escribe como '.' y las fichas
    se escriben tal cual (x, o).
    :param elements: list
    :param empty: "."
    :return: str
    """
    result = ''
    for elt in elements:
        if elt is None:
            result = result + empty
        else:
            result = result + elt
    return result

def explode_list(list_of_strings): #['x..o', 'oxoo']
    """
    Inversa de colapse_list: convierte cada cadena en lista de
    caracteres. Primer paso para reconstruir un tablero desde su código.
    :param list_of_strings: list
    :return: list
    """
    result = []
    for element in list_of_strings:
        result.append(list(element))
    return result

def replace_all(matrix, old, new):
    """
    Sustituye un valor por otro en todas las filas de la matriz.
    Se usa para cambiar los '.' del código por None.
    :param matrix: list
    :param old: str
    :param new: str
    :return: list
    """
    new_matrix = []
    for element in matrix:
        new_matrix.append(replace_in_list(element, old, new))
    return new_matrix

def replace_in_list(elements, old, new):
    """
    Devuelve una lista nueva con old sustituido por new. No modifica la original.
    :param elements: list
    :param old: str
    :param new: str
    :return: list
    """
    result = []
    for elt in elements:
        if elt == old:
            result.append(new)
        else:
            result.append(elt)
    return result
