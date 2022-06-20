import math
import cmath
import numpy as np


def quadratic_eq(a, b, c):
    # calc the discriminant
    d = (b ** 2) - (4 * a * c)

    if d < 0:
        print('Quadratic eq has No-real solution, d<0')
    elif d == 0:
        x = (-b + cmath.sqrt(d) / 2 * a)
        print('Quadratic has One-solution, d==0')
    else:
        x1 = (-b - cmath.sqrt(d)) / (2 * a)
        x2 = (-b + cmath.sqrt(d)) / (2 * a)
        print('Quadratic has Two-solution, x1,x2')
        return x1, x2


def linear_eq(loc_a, loc_b):
    x1, y1 = loc_a[0], loc_a[1]
    x2, y2 = loc_b[0], loc_b[1]
    a = (y2-y1) / (x2-x1)
    # y = aX + b
    b = a*x2 - y2

    return a, b


if __name__ == '__main__':
    pass
