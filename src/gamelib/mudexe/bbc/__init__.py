"""
Code for doing hardware windowed output on BBC GTSS terminals
Removed on UNIX version
"""
from ..key import Key


class BBC:
    def __init__(self, tty=0):
        self.tty = tty
        if tty == 4:
            # initbbc()
            self.__initscr()
            self.__topscr()
        Key.setup()

    @classmethod
    def disconnect(cls):
        Key.setback()

    @classmethod
    def reprint(cls):
        Key.reprint()

    @classmethod
    def __initscr(cls):
        pass

    @classmethod
    def __topscr(cls):
        pass


"""
void btmscr()
{
	;
}
"""
