class BBC:
    tty = 4

    @classmethod
    def init_screen(cls):
        if cls.tty != 4:
            return
        print("INIT SCREEN")

    @classmethod
    def top_screen(cls):
        if cls.tty != 4:
            return
        print("\n" * 8)
        print("TOP SCREEN")

    @classmethod
    def bottom_screen(cls):
        if cls.tty != 4:
            return
        print("BOTTOM SCREEN")
