"""Items for map."""

import random
from ..items.hubble_deep_field import HubbleDeepField
from ..items.hcb_greate_wall import HerculesCoronaBorealisGreatWall
from ..items.gigaparsec import Gigaparsec
from ..items.eridanus_supervoid import EridanusSupervoid
from ..items.distance_great_attractor import DistanceToGreatAttractor
from ..items import ITEMS


def __random_pos():
    return [random.randrange(0, 10) * 100 for _ in range(2)]


def load_items(scale):
    """Items loader.

    Yields:
        pygame.Sprite: Map item
    """
    items = [
        HubbleDeepField,
        HerculesCoronaBorealisGreatWall,
        Gigaparsec,
        EridanusSupervoid,
        DistanceToGreatAttractor,
        *ITEMS,
    ]
    for item in ITEMS:
        scale_diff = item.base_scale - scale
        if scale_diff < 0:
            print('<', item.name, 'DISABLED', scale_diff)
            continue
        if scale_diff > 2:
            print('>', item.name, 'DISABLED', scale_diff)
            continue

        yield item(__random_pos(), scale)
