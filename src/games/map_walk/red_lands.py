class Transport:
    def __init__(self, acc, max_speed):
        self.acc = acc
        self.max_speed = max_speed


HUMAN_SPEED = 6
HORSE_BAD_SPEED = 8
HORSE_NORMAL_SPEED = 10
HORSE_GOOD_SPEED = 10

CARRIAGE = Transport(5, 10)
BICYCLE = Transport(3, 8)
BIKE = Transport(4, 14)
CAR_BAD = Transport(3, 10)
CAR_NORMAL = Transport(5, 16)
CAR_GOOD = Transport(8, 28)
LORRY = Transport(4, 14)

PLAYER_SPEED = CARRIAGE.max_speed
