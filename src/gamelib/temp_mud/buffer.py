# Unknown
class Buffer:
    def __init__(self):
        self.__sysbuf = ""
        makebfr()

    def show(self):
        raise NotImplementedError()

    def add(self, *text, raw=False):
        if raw:
            self.__sysbuf += "".join(text)
        else:
            print("".join(text))
