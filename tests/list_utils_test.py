import pytest
from conecta_4.list_utils import *
from conecta_4.oracle import *

def test_find_n():
    #el pajar, la aguja y la cantidad de veces que está la aguja
    assert find_n([2, 3, 4, 5, 6], 2, -1) == False
    assert find_n([1, 2, 3, 4, 5], 42, 2) == False
    assert find_n([1, 2, 3, 4, 5], 2, 2) == False
    assert find_n([1, 2, 3, 2, 4, 5], 2, 2)
    assert find_n([1, 2, 3, 4, 5, 4, 6, 4, 7, 4, 6], 4, 2)
    assert find_n([1, 2, 3, 4],'x' , 0)

def test_find_one():
    assert find_one([1, 2, 3, 4], 1)
    assert find_one([1, 2, 3, 4], 5) == False
    assert find_one([1, 2, 3, 4], 4)
    assert find_one([4, 4, 4, 4], 4)

def test_find_strike():
    assert find_strike([2, 1, 3], 2, 0) # Esto es intencionado
    assert find_strike([1, 2, 3, 4], 1, 3) == False
    assert find_strike([1, 1, 1, 4], 1, 3)
    assert find_strike([2, 1, 1, 1], 1, 3)
    assert find_strike([1, 2, 3, 4], 1, -3) == False
    assert find_strike([1, 2, 3, 4], 5, 3) == False
    assert find_strike([1, 1, 3, 1], 1, 3) == False
    assert find_strike([None, 'x', 'x', 'x'], 'x', 3)
    assert find_strike(['o', 'x', 'x', 'x', 'o'], 'x', 3)
    assert find_strike(['x', 'x', 'x', 'x'], 'x', 3)
    assert not find_strike(['x', 'x', 'o', 'x'], 'x', 3)
    assert not find_strike(['x', 'o', 'x', 'x'], 'x', 3)

def test_make_list():
    assert make_list(4, None) == [None, None, None, None]
    assert make_list(3, None) == [None, None, None]
    assert make_list(2, 'x') == ['x', 'x']
    assert make_list(1, 0) == [0]
    assert make_list(0, None) == []
    assert make_list(-2, None) == []

def test_index_first_element():
    assert index_first_element([1, 2, 3], 1) == 0
    assert index_first_element([1, 2, 3], 4) is None
    assert index_first_element(['x', 'o', 'x', 'o'], None) is None

def test_map_list():
    assert map_list([1, 2, 3], lambda x: x * 2) == [2, 4, 6]

def test_transpose():
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    assert transpose(matrix) == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    assert transpose(transpose(matrix)) == matrix
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]

def test_displace_matrix():
    matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    assert displace_matrix(matrix) == [[2, 3, 4, None],
                                      [5, 6, 7, 8],
                                      [None, 9, 10, 11],
                                      [None, None, 13, 14]]
    assert displace_matrix(matrix, '-') == [[2, 3, 4, '-'],
                                           [5, 6, 7, 8],
                                           ['-', 9, 10, 11],
                                           ['-', '-', 13, 14]]

def test_reverse_list():
    assert reverse_list([1, 2, 3]) == [3, 2, 1]
    assert reverse_list(reverse_list([1, 2, 3])) == [1, 2, 3]

def test_reverse_matrix():
    matrix = [[1, 2, 3], [4, 5, 6]]
    assert reverse_matrix(matrix) == [[3, 2, 1], [6, 5, 4]]
    assert reverse_matrix(reverse_matrix(matrix)) == matrix

def test_all_the_same_score():
    assert all_the_same_score([1, 1, 1])
    assert not all_the_same_score([1, 1, 2])
    assert all_the_same_score([ColumnRecommendations(0, ColumnClassification.MAYBE),
                               ColumnRecommendations(3, ColumnClassification.MAYBE)])
    assert not all_the_same_score([ColumnRecommendations(0, ColumnClassification.MAYBE),
                                   ColumnRecommendations(0, ColumnClassification.WIN)])

def test_colpase_matrix_list():
    assert colpase_matrix([['x', 'o', None, None], ['o', None, None, None]]) == 'xo..|o...'
    assert colapse_list(['x', 'o', None, None]) == 'xo..'
    assert colapse_list([]) == ''
def test_explode_list():
    assert explode_list(['x..o', 'oxoo']) == [['x', '.', '.', 'o'], ['o', 'x', 'o', 'o']]

def test_full_code_decode():
    matrix = [['x', 'o', None, None], [None, None, None, None], ['o', 'o', 'x', 'x'], ['x', None, None, None]]
    code = colpase_matrix(matrix)
    assert code == 'xo..|....|ooxx|x...'
    assert replace_all(explode_list(code.split('|')), '.', None) == matrix