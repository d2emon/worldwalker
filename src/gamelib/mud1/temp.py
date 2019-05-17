ttyt = None


def gethostname(*args):
    result = "DAVIDPOOTER"
    print('\tgethostname', args, result)
    return result


def getty(*args):
    print('\tgetty', args)


def stat(*args):
    print('\tstat', args)


def ctime(time, *args):
    print('\tctime', time, args)
    return time


def cls(*args):
    print('\tcls', args)


def time(*args):
    print('\ttime', args)


def cuserid(*args):
    print('\tcuserid', args)


def syslog(*args):
    print('\tsyslog', args)


def talker(*args):
    print('\ttalker', args)


def crapup(*args):
    print('\tcrapup', args)


def openlock(*args):
    print('\tfclose', args)
