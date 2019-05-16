import config
from breakout import Breakout


if __name__ == "__main__":
    game = Breakout(
        frame_rate=config.FRAME_RATE,
        width=config.WIN_WIDTH,
        height=config.WIN_HEIGHT,
        caption=config.TITLE,
    )
    game.play()
    game.end_game()
