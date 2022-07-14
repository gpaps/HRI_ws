import math
import cmath
import numpy as np

# mode is either "D" for degree, otherwise it assumes  radians or "R" for radians
def get_quaternion_from_euler(roll, pitch, yaw, mode):

    if mode == "D":
        roll = roll * np.pi / 180
        pitch = pitch * np.pi / 180
        yaw = yaw * np.pi / 180

    qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)
    qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2)
    qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2)
    qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)

    return [qx, qy, qz, qw]


def quadratic_eq(a, b, c):
    ''' f(x) =  ax**2 + bx + c
    '''
    # calc the discriminant
    d = (b ** 2) - (4 * a * c)

    print("diakrinoysa=",d)
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
    """
    Straight line through TWO points will have an equation in the form
    y = m*x + c , the function imports: loc_a[x1, y1],loc_b[x2, y2]
    """
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
    """"
    Two Dimension Euclidian Distance,
    loc_1[q1, q2],   loc_2[p1, p2],
    d(p,q = sqrt( (q1-p1)**2 - (q2-p2)**2 )
    """
    dist = math.sqrt((loc_1[0] - loc_2[0]) ** 2 + (loc_1[1] - loc_2[1]) ** 2)
    return dist


def find_pos_Rel2Hum(location_r, location_h, d):
    '''
    First input: Robot location
    Second input: Human location
    Third input: Distance from Human
    '''

    # set human location at [0,0]
    loc_r=[location_r[0]-location_h[0], location_r[1]-location_h[1]]
    loc_h=[0,0]
    pos_found = 0 #no solution is found yet

    # print("Human:(",loc_h[0],loc_h[1],")   Robot:(",loc_r[0], loc_r[1],")")
    sol_l, a, b = linear_eq(loc_r, loc_h)
    # print("eq:",sol_l, a, b)
    if sol_l > 0:
        # sol_q, x1, x2 = quadratic_eq(a ** 2 + 1, 2 * a * b, b ** 2 - d * d)
        sol_q, x1, x2 = quadratic_eq(a ** 2+1, 2 * a * b - 2 * a*loc_h[1]-2*loc_h[0], b ** 2 +loc_h[1]** 2 -2*b*loc_h[1] - d * d)
        # print("sol_q:", sol_q, "       ,",x1, x2)
        if sol_q > 0:
            y1 = a * x1 + b
            # dist = euc_dist([loc_h[0] + x1, loc_h[1] + y1], loc_h)
            dist = euc_dist([x1, y1], loc_h)
            # print("toGo1:(", x1, y1,")   ", dist)
            # print("toGo1:(", loc_h[0] + x1, loc_h[1] + y1,")   ", dist)
            y2 = a * x2 + b
            # dist = euc_dist([loc_h[0] + x2, loc_h[1] + y2], loc_h)
            dist = euc_dist([x2, y2], loc_h)
            # print("toGo2:(", loc_h[0] + x2, loc_h[1] + y2,")   ", dist)
            # print("toGo2:(", x2, y2,")   ", dist)
            # if (loc_h[0] < loc_h[0] + x1 < loc_r[0]) or (loc_h[0] > loc_h[0] + x1 > loc_r[0]):
            #     print("epistrefei thn 1h")
            #     return loc_h[0] + x1, loc_h[1] + y1

            if loc_h[0] < loc_h[0] + x1 < loc_r[0]:
                # print(loc_h[0],'<', loc_h[0] + x1 ,'<', loc_r[0],"epistrefei thn 1hA")
                pos_found = 1
                return pos_found, location_h[0] + x1, location_h[1] + y1

            if loc_h[0] > loc_h[0] + x1 > loc_r[0]:
                # print(loc_h[0],'>', loc_h[0] + x1 ,'>', loc_r[0],"epistrefei thn 1hB")
                pos_found = 1
                return pos_found, location_h[0] + x1, location_h[1] + y1

            if loc_h[0] < loc_h[0] + x2 < loc_r[0]:
                # print(loc_h[0],'<', loc_h[0] + x2 ,'<', loc_r[0],"epistrefei thn 2hA")
                pos_found = 1
                return pos_found, location_h[0] + x2, location_h[1] + y2

            if loc_h[0] > loc_h[0] + x2 > loc_r[0]:
                # print(loc_h[0],'>', loc_h[0] + x2 ,'>', loc_r[0],"epistrefei thn 2hB")
                pos_found = 1
                return pos_found, location_h[0] + x2, location_h[1] + y2
        else:
            print("Can't find location to send robot")
            return pos_found, loc_h[0], loc_h[1]

    elif sol_l == 0:
        return pos_found, loc_h[0], loc_h[1]
        pass

    else:
        print('problem')
        return pos_found, loc_h[0], loc_h[1]



def find_pos_0(loc_r, loc_h, d):
    pos_found = 0

    '''
    First input Robot location
    Second input Human location
    Third input Distance from Human
    '''
    print("Human:(",loc_h[0],loc_h[1],")   Robot:(",loc_r[0], loc_r[1],")")
    sol_l, a, b = linear_eq(loc_r, loc_h)
    print("eq:",sol_l, a, b)
    if sol_l > 0:
        # sol_q, x1, x2 = quadratic_eq(a ** 2 + 1, 2 * a * b, b ** 2 - d * d)
        sol_q, x1, x2 = quadratic_eq(a ** 2+1, 2 * a * b - 2 * a*loc_h[1]-2*loc_h[0], b ** 2 +loc_h[1]** 2 -2*b*loc_h[1] - d * d)
        print("sol_q:", sol_q, "       ,",x1, x2)
        if sol_q > 0:
            y1 = a * x1 + b
            # dist = euc_dist([loc_h[0] + x1, loc_h[1] + y1], loc_h)
            dist = euc_dist([x1, y1], loc_h)
            print("toGo1:(", x1, y1,")   ", dist)
            # print("toGo1:(", loc_h[0] + x1, loc_h[1] + y1,")   ", dist)
            y2 = a * x2 + b
            # dist = euc_dist([loc_h[0] + x2, loc_h[1] + y2], loc_h)
            dist = euc_dist([x2, y2], loc_h)
            # print("toGo2:(", loc_h[0] + x2, loc_h[1] + y2,")   ", dist)
            print("toGo2:(", x2, y2,")   ", dist)
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
        return pos_found, loc_h[0], loc_h[1]
        pass

    else:
        print('problem')
        return pos_found, loc_h[0], loc_h[1]


if __name__ == '__main__':
    pass
