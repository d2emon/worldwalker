"""
#define CHAR1 255
#define CHAR2 655300
"""


def byte_put(x, y, z):
    x[y - 1] = z
    return x


def byte_fetch(x, y):
    return x[y - 1]


def bit_fetch(x, y):
    return x[y]


def bit_set(x, y):
    x[y] = True


def bit_clear(x, y):
    x[y] = False
