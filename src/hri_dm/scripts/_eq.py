import math
import cmath
import numpy as np


def quadratic_eq(a, b, c):
    # calc the discriminant
    d = (b ** 2) - (4 * a * c)

    if d < 0:
        print('Quadratic eq has No-real solution, d<0')
        solutions = 0
        x1 = x2 = 0
    elif d == 0:
        x1 = x2 = ((-b + math.sqrt(d)) / (2 * a))
        print('Quadratic has One-solution, d==0')
        solutions = 1
    else:
        x1 = (-b - math.sqrt(d)) / (2 * a)
        x2 = (-b + math.sqrt(d)) / (2 * a)
        print('Quadratic has Two-solution, x1,x2')
        solutions = 2
    return solutions, x1, x2


def linear_eq(loc_a, loc_b):
    x1, y1 = loc_a[0], loc_a[1]
    x2, y2 = loc_b[0], loc_b[1]

    if math.isclose(x2, x1):
        # line equation can not be defined
        solved = -1
        a = b = 0
        return solved, a, b
    else:
        solved = 1
        a = (y2 - y1) / (x2 - x1)
        # y = aX + b
        # b = a*x2 - y2
        b = y2 - a * x2
        return solved, a, b


def euc_dist(loc_1, loc_2):
    dist = math.sqrt((loc_1[0] - loc_2[0]) ** 2 + (loc_1[1] - loc_2[1]) ** 2)
    return dist


def find_pos(loc_r, loc_h, d):
    pos_found = 0
    '''
    First input Robot location
    Second input Human location
    Third input Distance from Human
    '''
    sol_l, a, b = linear_eq(loc_r, loc_h)
    if sol_l > 0:
        sol_q, x1, x2 = quadratic_eq(a ** 2 + 1, 2 * a * b, b ** 2 - d * d)
        if sol_q > 0:
            y1 = a * x1 + b
            dist = euc_dist([loc_h[0] + x1, loc_h[1] + y1], loc_h)
            print("toGo1:", loc_h[0] + x1, loc_h[1] + y1, dist)
            y2 = a * x2 + b
            dist = euc_dist([loc_h[0] + x2, loc_h[1] + y2], loc_h)
            print("toGo2:", loc_h[0] + x2, loc_h[1] + y2, dist)
            # if (loc_h[0] < loc_h[0] + x1 < loc_r[0]) or (loc_h[0] > loc_h[0] + x1 > loc_r[0]):
            #     print("epistrefei thn 1h")
            #     return loc_h[0] + x1, loc_h[1] + y1

            if loc_h[0] < loc_h[0] + x1 < loc_r[0]:
                # print(loc_h[0],'<', loc_h[0] + x1 ,'<', loc_r[0],"epistrefei thn 1hA")
                pos_found = 1
                return pos_found, loc_h[0] + x1, loc_h[1] + y1

            if loc_h[0] > loc_h[0] + x1 > loc_r[0]:
                # print(loc_h[0],'>', loc_h[0] + x1 ,'>', loc_r[0],"epistrefei thn 1hB")
                pos_found = 1
                return pos_found, loc_h[0] + x1, loc_h[1] + y1

            if loc_h[0] < loc_h[0] + x2 < loc_r[0]:
                # print(loc_h[0],'<', loc_h[0] + x2 ,'<', loc_r[0],"epistrefei thn 2hA")
                pos_found = 1
                return pos_found, loc_h[0] + x2, loc_h[1] + y2

            if loc_h[0] > loc_h[0] + x2 > loc_r[0]:
                # print(loc_h[0],'>', loc_h[0] + x2 ,'>', loc_r[0],"epistrefei thn 2hB")
                pos_found = 1
                return pos_found, loc_h[0] + x2, loc_h[1] + y2
        else:
            print("Can't find location to send robot")
            return pos_found, loc_h[0], loc_h[1]

    elif sol_l == 0:
        pass
        return pos_found, loc_h[0], loc_h[1]

    else:
        print('problem')


if __name__ == '__main__':
    pass
