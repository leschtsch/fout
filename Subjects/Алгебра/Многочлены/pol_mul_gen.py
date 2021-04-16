# многочлены
# & ax + by + c = d


#  TODO: несколько переменных
#  TODO: Настройка

from numpy.polynomial.polynomial import Polynomial as P
from random import randint, shuffle
import re
import sys
import os

#  TODO красивый вывод

sys.path.insert(0, os.getcwd().split("Subjects")[0])
os.chdir(os.getcwd().split("Subjects")[0])
from export import export
from Visualiser import *


def list_poly_repr(a):
    a = [poly_repr(i, True) for i in a]
    s = '(' + ')('.join(a) + ')'
    return s


def poly_repr(a, sh=False):
    s = str(a)
    return s


def generate_one():
    P1 = P([randint(-10, 10), randint(-10, 10), randint(-3, 3)])
    P2 = P([randint(-10, 10), randint(-10, 10), randint(-3, 3)])
    res = list_poly_repr([P1, P2]) + ' = ' + poly_repr(P1 * P2)
    if len(res) > 20:
        res = r'= \newline ='.join(res.split('='))
    return res


def square_of_sum():
    P1 = P([randint(-10, 10), randint(-10, 10)])
    P2 = P([randint(-5, 5), randint(-5, 5)])
    polynoms = [P1, P1, P2]
    shuffle(polynoms)
    res = list_poly_repr(polynoms) + ' = ' + poly_repr(P1 * P1 * P2)
    if len(res) > 20:
        res = r'= \newline ='.join(res.split('='))
    return res


def difference_of_squares():
    a = randint(-10, 10)
    b = randint(-10, 10)
    P1 = P([a, b])
    P2 = P([a, -b])
    P3 = P([randint(-5, 5), randint(-5, 5)])
    polynoms = [P1, P2, P3]
    shuffle(polynoms)
    res = list_poly_repr(polynoms) + ' = ' + poly_repr(P1 * P2 * P3)
    if len(res) > 20:
        res = r'= \newline ='.join(res.split('='))
    return res


def cube_of_sum():
    P1 = P([randint(-5, 5), randint(5, 5)])
    res = list_poly_repr([P1, P1, P1]) + ' = ' + poly_repr(P1 * P1 * P1)
    if len(res) > 20:
        res = r'= \newline ='.join(res.split('='))
    return res


def sum_of_cubes():
    a = randint(-10, 10)
    b = randint(-10, 10)
    P1 = P([a, b])
    P2 = P([a * a, -a * b, b * b])
    res = list_poly_repr([P1, P2]) + ' = ' + poly_repr(P1 * P2)
    if len(res) > 20:
        res = r'= \newline ='.join(res.split('='))
    return res


def generate():
    a = get_interface_input('''
    numb(количество заданий, 0, 20);numb(количество заданий, quantity, 1);
        ''')
    a = [i.strip() for i in a.split(',')]
    params = {}
    for i in a:
        b = i.split(' : ')
        params[b[0]] = b[1]
    r = generate_one()
    for i in range(int(params['quantity'])):
        pass
    print(r)
    # export('$y=x^2$')


generate()
