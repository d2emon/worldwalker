#! /usr/bin/python
import config
# from games.breakout import Breakout as Game
# from games.middleearth import MiddleEarth as Game
from games.space import Space as Game
from windows.walker import WalkerWindow


def main():
    window = WalkerWindow()
    window.run()

    game = Game(
        frame_rate=config.FRAME_RATE,
        width=config.SCREEN_WIDTH,
        height=config.SCREEN_HEIGHT,
        caption=config.TITLE,
    )
    game.play()
    game.end_game()


if __name__ == "__main__":
    main()
