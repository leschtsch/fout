# многочлены
# & ax + by + c = d


from numpy.polynomial.polynomial import Polynomial as P
from random import randint
import re
import sys
import os

sys.path.insert(0, os.getcwd().split("Subjects")[0])


def list_poly_repr(a):
    a = [poly_repr(i) for i in a]
    s = '(' + ')('.join(a) + ')'
    return s


def poly_repr(a):
    s = str(a)
    s = s.split(' + ')
    s = s[::-1]
    s = ' + '.join(s)
    s = ' ' + s + ' '
    s = re.sub(r'\*\*', '^', s)
    s = re.sub(r'x\^1', 'x', s)
    s = re.sub(r'\.0', '', s)
    s = re.sub(r' 0 x\^[1234567890]* \+ ', '', s)
    s = re.sub(r' x', 'x', s)
    s = s.strip()
    return s


def generate():
    P1 = P([randint(1, 10), randint(1, 10), randint(0, 3)])
    P2 = P([randint(1, 10), randint(1, 10), randint(0, 3)])
    print(P1)
    return list_poly_repr([P1, P2]) + ' = ' + poly_repr(P1 * P2)


if __name__ == '__main__':
    print(generate())
