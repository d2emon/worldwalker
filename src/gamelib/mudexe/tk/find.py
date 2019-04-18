from ..aber_blib import sec_read


def findstart(unit):
    bk = sec_read(unit, 0, 1)
    return bk[0]


def findend(unit):
    bk = sec_read(unit, 0, 2)
    return bk[1]
