import pygame
import config
from .background import Background
from .grid import Grid
from .map.image import MapImage
from .coord_label import CoordLabel
from .order_label import OrderLabel
from .loading import LoadingLabel


__cache = {}


def load_cached(key):
    """Load resource from cache or create new.

    Args:
        key (Any): Cache key.
    """
    def wrapper(func):
        def wrapped(*args, force=False, **kwargs):
            image = __cache.get(key) if not force else None

            if image is not None:
                print(f"LOAD FROM CACHE '{key}'")
                return image

            print(f"CREATE NEW '{key}'")
            image = func(*args, **kwargs)
            __cache[key] = image
            return image

        return wrapped
    return wrapper


# Images


@load_cached('player_image')
def player_image():
    """Get player image.

    Returns:
        pygame.Surface: Player image.
    """
    return pygame.image.load(config.Universe.PLAYER)


@load_cached('map_image')
def map_image():
    """Get map image.

    Returns:
        pygame.Surface: Map image.
    """
    return pygame.image.load(config.Universe.GLOBAL_MAP)


@load_cached('map_grid')
def map_grid(size, step=10):
    """Get map image.

    Returns:
        pygame.Surface: Map grid.
    """
    return Grid(size=size, step=step)


# Sprites

@load_cached('main_screen_background')
def main_screen_background(rect):
    """Get main screen background.

    Args:
        rect (pygame.Rect): Screen rect.

    Returns:
        pygame.Sprite: Background sprite.
    """
    return Background(rect)


@load_cached('map_background')
def map_background(rect):
    """Get map background.

    Args:
        rect (pygame.Rect): Screen rect.

    Returns:
        pygame.Sprite: Background sprite.
    """
    return main_screen_background(rect)


@load_cached('map_sprite')
def map_sprite(size, grid):
    """Get map sprite.

    Returns:
        pygame.Sprite: Map sprite.
    """
    return MapImage(
        map_image(),
        size=size,
        grid=grid,
    )


@load_cached('coord_label')
def coord_label(rect):
    """Get coord label.

    Args:
        rect (pygame.Rect): Sprite rect.

    Returns:
        pygame.Sprite: Coord label.
    """
    return CoordLabel(rect)


@load_cached('order_label')
def order_label(rect):
    """Get coord label.

    Args:
        rect (pygame.Rect): Sprite rect.

    Returns:
        pygame.Sprite: Order label.
    """
    return OrderLabel(rect)


@load_cached('loading')
def loading(rect):
    """Get loading label.

    Args:
        rect (pygame.Rect): Sprite rect.

    Returns:
        pygame.Sprite: Loading label.
    """
    return LoadingLabel(rect)
