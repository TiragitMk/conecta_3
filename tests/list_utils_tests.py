from conecta_4.list_utils import *

def find_strike_test():
    assert find_strike([2,1,3], 2, 0)
def displace_test():
    pass

print(displace(["o","x","o"],2,None))
print(displace_matrix([["o","x","o","x"],["x","x", "o", "o"], ["x","x","o", "o"], [None, "o", "x", None]]))
find_strike_test()