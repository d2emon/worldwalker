import config
# from games.breakout import Breakout as Game
# from games.middleearth import MiddleEarth as Game
from games.space import Space as Game


if __name__ == "__main__":
    game = Game(
        frame_rate=config.FRAME_RATE,
        width=config.WIN_WIDTH,
        height=config.WIN_HEIGHT,
        caption=config.TITLE,
    )
    game.play()
    game.end_game()
