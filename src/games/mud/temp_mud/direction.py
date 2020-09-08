class Direction:
    def __init__(self, direction_id, title):
        self.direction_id = direction_id
        self.title = title


NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
UP = 4
DOWN = 5


DIRECTIONS = {
    NORTH: Direction(NORTH, "north"),
    EAST: Direction(EAST, "east"),
    SOUTH: Direction(SOUTH, "south"),
    WEST: Direction(WEST, "west"),
    UP: Direction(UP, "up"),
    DOWN: Direction(DOWN, "down"),
}
