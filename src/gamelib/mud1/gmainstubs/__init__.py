from ...file_services import LogFile
from ..obdat import objects
# import stdio
# import sys.errno
# import sys.file
# from ..object import *
# from ..system import *
# from ..flock import *


class GMainStubs:
    ttyt = 0


def qcrypt(data):
    return data


def dcrypt(data):
    return data


def cls():
    """
    This isnt used on unix

    :return:
    """
    print("\t...\tcls()")


def getty():
    """
    We dont use this on the unix version

    :return:
    """
    print("\t...\tgetty()")


"""
void fcloselock(file)
FILE *file;
{
	flock(fileno(file),LOCK_UN);
	fclose(file);
}
"""

def validname(name):
    """

    :param name:
    :return:
    """
    try:
        resword(name)
    except ValueError:
        raise ValueError("Sorry I cant call you that")
    if len(name) > 10:
        raise ValueError()
    if " " in name:
        raise ValueError()
    if fobn(name) is not None:
        raise ValueError("I can't call you that , It would be confused with an object")


RESERVED = [
    "the",
    "me",
    "myself",
    "it",
    "them",
    "him",
    "her",
    "someone",
    "there",
]


def resword(name):
    if name.lower() in RESERVED:
        raise ValueError()


def fobn(name):
    x = name.lower()
    for ct in objects:
        if x == ct.o_name:
            return ct
    return None


def syslog(text):
    try:
        LogFile.log(text)
    except FileNotFoundError:
        # loseme()
        raise Exception("Log fault : Access Failure")
