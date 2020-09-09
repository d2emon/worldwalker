import pygame


COLLIDE_TOP = 'T'
COLLIDE_BOTTOM = 'B'
COLLIDE_LEFT = 'L'
COLLIDE_RIGHT = 'R'


def intersect(rect1, rect2):
    edges = {
        COLLIDE_LEFT: pygame.Rect(rect2.left, rect2.top, 1, rect2.height),
        COLLIDE_RIGHT: pygame.Rect(rect2.right, rect2.top, 1, rect2.height),
        COLLIDE_TOP: pygame.Rect(rect2.left, rect2.top, rect2.width, 1),
        COLLIDE_BOTTOM: pygame.Rect(rect2.left, rect2.bottom, rect2.width, 1),
    }
    collisions = {edge for (edge, rect) in edges.items() if rect1.colliderect(rect)}

    if not collisions:
        return None

    if len(collisions) == 1:
        return list(collisions)[0]

    if COLLIDE_TOP in collisions:
        if rect1.centery >= rect2.top:
            return COLLIDE_TOP
        return COLLIDE_LEFT if rect1.centerx < rect2.left else COLLIDE_RIGHT

    if COLLIDE_BOTTOM in collisions:
        if rect1.centery < rect2.bottom:
            return COLLIDE_BOTTOM
        return COLLIDE_LEFT if rect1.centerx < rect2.left else COLLIDE_RIGHT

    return None
