brmode = 0


class Room:
    def __init__(self, room , mode):
        self.room = room
        self.mode = mode

    def close(self):
        pass


def openroom(room, mode):
    return Room(room, mode)


def sendsys(*args):
    print("SEND", args)


def eorte():
    pass


def gamrcv():
    pass


def gamecom(cmd):
    pass