def find_n(elements, needle, n):
    """
    Devuelve True si en elements hay n o más ocurrencias de needle
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
    return find_n(elements, needle, 1)

def find_strike(elements, needle, n):
    """

    :param elements:
    :param needle:
    :param n:
    :return:
    """
    if n >= 0:
        index = 0
        count = 0
        #strike = False
        while count < n and index < len(elements):
            if needle == elements[index]:
                #strike = True
                count += 1
            else:
                #strike = False
                count = 0
            index += 1
        return count >= n #and strike
    else:
        return False

def make_list(length, filler):

    result = []
    index = 0
    while index < length:
        result.append(filler)
        index += 1
    return result

def index_first_element(elements, needle):
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
    :param elements:
    :param transform:
    :return:
    """
    result = []
    for element in elements:
        result.append(transform(element))
    return result

def make_list_from_factory(length, factory):
    """
    Crea una lista de listas que son fabricadas por mi fábrica que es LinearBoard
    :param length:
    :param factory:
    :return:
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
    d = []
    for i in range(len(matrix)):
        d.append(displace(matrix[i], i - 1, filler))
    return d

def reverse_list(elements):
    return elements[::-1]

def reverse_matrix(matrix):
    result = []
    for col in matrix:
        result.append(reverse_list(col))
    return result

def all_the_same_score(elements):
    """
    No controla lista vacía. De momento no pasa nada.
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
    result = ''
    for elt in matrix:
        result = result + sep + colapse_list(elt, empty)
    return result[1:]

def colapse_list(elements, empty = '.'):
    result = ''
    for elt in elements:
        if elt is None:
            result = result + empty
        else:
            result = result + elt
    return result

def explode_list(list_of_strings): #['x..o', 'oxoo']
    result = []
    for element in list_of_strings:
        result.append(list(element))
    return result

def replace_all(matrix, old, new):
    new_matrix = []
    for element in matrix:
        new_matrix.append(replace_in_list(element, old, new))
    return new_matrix

def replace_in_list(elements, old, new):
    result = []
    for elt in elements:
        if elt == old:
            result.append(new)
        else:
            result.append(elt)
    return result









