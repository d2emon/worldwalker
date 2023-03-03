"""Items for map."""

import random
from ..items import ITEMS


def __random_pos(size, step=100):
    max_pos = [int(i / step) for i in size]
    return [random.randrange(0, max_pos[i]) * step for i in range(2)]


def load_items(scale, size, step=100):
    """Items loader.

    Yields:
        pygame.Sprite: Map item
    """
    # print(ITEMS)
    print('STEP', step)
    for item in ITEMS:
        scale_diff = item.scale - scale
        if scale_diff < 0:
            print('<', item.name, 'DISABLED', scale_diff)
            continue
        if scale_diff > 2:
            print('>', item.name, 'DISABLED', scale_diff)
            continue

        yield item(__random_pos(size, step), scale)
