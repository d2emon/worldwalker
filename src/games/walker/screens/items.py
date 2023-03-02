"""Items for map."""

import random
from ..items import ITEMS


def __random_pos(size):
    delta = 100
    max_pos = int(size / delta)
    return [random.randrange(0, max_pos) * delta for _ in range(2)]


def load_items(scale, size):
    """Items loader.

    Yields:
        pygame.Sprite: Map item
    """
    for item in ITEMS:
        scale_diff = item.base_scale - scale
        if scale_diff < 0:
            print('<', item.name, 'DISABLED', scale_diff)
            continue
        if scale_diff > 2:
            print('>', item.name, 'DISABLED', scale_diff)
            continue

        yield item(__random_pos(size), scale)
