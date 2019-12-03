""" Functions needed fot the search algorithm """

import numpy as np
from numpy import abs
from numpy.linalg import norm


def search(t, grid, precision, V, D1, D2):
    """
    Find the position (vector p_min) and value (min) of the minimum on each point of the grid
    Args:
        t (float) : search step
        grid (list[np.array([x,y,z])]) :
        precision (float) :
        V (np.array([x,y,z])) : Volume
        D1, D2 : Measurement class
            Measurements nb. 1 and 2
    Return:
        rv: list(list(p_min, min))
    """
    rv=[]
    for p in grid:
        p_min = p
        min = 10e100 #(infini)
        while p[2]<=V[2]:
            val = evaluatePoint(p, D1, D2)
            if val < min :
                min = val
                p_min = p
            p += t*p #search along d
        p_minus1 = p_min - t*d
        p_plus1 = p_min + t*d
        p_min, min  = ternarySearch(precision, p_minus1, p_plus1, D1, D2)
        rv.append([p_min, min])
    return rv

def ternarySearch(absolutePrecision, lower, upper, D1, D2):
    """
    Find the maximum in the interval [<lower>, <upper>] with a precision of <absolutePrecision>.
    Recursive function.
    Args:
        absolutePrecision : float
            Precision of the search interval
        lower : np.array([x,y,z])
            Current lower bound of search domain
        upper : np.array([x,y,z])
            Current upper bound of search domain
        D1, D2 : Measurement class
            Measurements nb. 1 and 2
    Return:
        p_min : np.array([x,y,z])
        min :
    """
    # Note : upper = lower+c*d with d the search direction.
    # Everything works with vectors
    if abs(norm(upper - lower)) < absolutePrecision:
        p_min = (lower + upper)/2
        min = evaluatePoint(p_min, D1, D2)
        return p_min, min
    lowerThird = (2*lower + upper)/3
    upperThird = (lower + 2*upper)/3

    if evaluatePoint(lowerThird, D1, D2) < evaluatePoint(upperThird,  D1, D2):
        ternarySearch(absolutePrecision, lowerThird, upper, D1, D2)
    else:
        ternarySearch(absolutePrecision, lower, upperThird, D1, D2)


def m1(n1, n2):
    """Inconsistensy of the current point p.
    Definition: m=1-absolute_value( n1<dot_product>n2 )
    Args:
        n1, n2 : np.array([x,y,z])
    """
    return 1 - np.abs(n1@n2)

def m2(n1, n2):
    """Inconsistensy of the current point p.
    Definition : m=n1<cross_product>n2
    Args:
        n1, n2 : np.array([x,y,z])"""
    return norm(np.cross(n1, n2))


def evaluatePoint(p, D1, D2):
    """
    Evaluate the inconsistensy m of two measurements D1 and D2 at a point p
    Args:
        p = np.array([x,y,z])
        D1, D2 : measurements nb. 1 and 2
    Returns:
        Inconsistensy
    """
    n1 = normal_at(p, D1)
    n2 = normal_at(p,D2)
    return m1(n1, n2)



def normal_at(p, Di):
    """
    TO DO
    Evaluates the normal at a point p from a measurement Di
    Args:
        p = np.array([x,y,z])
        Di: measurement of camera i
    returns
        n = np.array([x,y,z]) (unit vector)
    """
    return None




































#
