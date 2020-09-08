#! /usr/bin/python
import config
# from games.breakout import Breakout as Game
# from games.middleearth import MiddleEarth as Game
from games.space import Space as Game


def main():
    game = Game(
        frame_rate=config.FRAME_RATE,
        width=config.SCREEN.WIDTH,
        height=config.SCREEN.HEIGHT,
        caption=config.SCREEN.CAPTION,
    )
    game.play()
    game.end_game()


if __name__ == "__main__":
    main()
