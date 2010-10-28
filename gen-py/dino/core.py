#!/usr/bin/env python

from dinoisland.ttypes import Direction

def vectorToOrientation(c):
    """ Returns the general direction of a vector."""
    if c.row > 0 and c.column == 0: return Direction.S
    if c.row < 0 and c.column == 0: return Direction.N
    if c.column > 0 and c.row == 0: return Direction.E
    if c.column < 0 and c.row == 0: return Direction.W
    if c.column > 0 and c.row > 0: return Direction.SE
    if c.column < 0 and c.row > 0: return Direction.SW
    if c.column < 0 and c.row < 0: return Direction.NW
    if c.column > 0 and c.row < 0: return Direction.NE


def vectorToDirections(c):
    ret = list()
    while c.distance() != 0:
        while c.row > 0 and c.column == 0:
            ret.append(Direction.S)
            c.row -= 1
        while c.row < 0 and c.column == 0:
            ret.append(Direction.N)
            c.row += 1
        while c.column > 0 and c.row == 0:
            ret.append(Direction.E)
            c.column -= 1
        while c.column < 0 and c.row == 0:
            ret.append(Direction.W)
            c.column += 1
        while c.column > 0 and c.row > 0:
            ret.append(Direction.SE)
            c.row -= 1
            c.column -= 1
        while c.column < 0 and c.row > 0:
            ret.append(Direction.SW)
            c.row -= 1
            c.column += 1
        while c.column < 0 and c.row < 0:
            ret.append(Direction.NW)
            c.row += 1
            c.column += 1
        while c.column > 0 and c.row < 0:
            ret.append(Direction.NE)
            c.row += 1
            c.column -= 1
    return ret


def counter(init):
    i = init
    while True:
        i += 1
        yield i


def getCone(direction, angle=1):
    ret = set()
    ret.add(direction)
    for i in range(1, angle+1):
        ret.add(range(8)[(direction-i)%8])
        ret.add(range(8)[(direction+i)%8])
    return ret


def minmax(l):
    return min(l), max(l)
