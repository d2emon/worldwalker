"""
Code for doing hardware windowed output on BBC GTSS terminals
Removed on UNIX version
"""


class BBC:
    def __init__(self, tty=0):
        self.tty = tty
        if tty == 4:
            # initbbc()
            self.initscr()
            self.topscr()

    @classmethod
    def initscr(cls):
        pass

    @classmethod
    def topscr(cls):
        pass


"""
void btmscr()
{
	;
}
"""
