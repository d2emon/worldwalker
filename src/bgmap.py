import resources
from pygame import image, sprite, draw, transform, Surface, Color, Rect


MOVE_SPEED = 32
WIDTH = 800
HEIGHT = 600
# CONSTS = ((-1600, 1600), (-1280, 1280))
LENGTH = 3200 * MOVE_SPEED
CONSTS = ((-LENGTH, LENGTH), (-LENGTH, LENGTH))
LANDS = (
    (
        (17, 0),
        (17, 1),
        (18, 1),
        (18, 3),
        (19, 3),
        (19, 5),
        (22, 5),
        (22, 4),
        (20, 4),
        (20, 3),
        (19, 3),
        (19, 1),
        (20, 1),
        (20, 0),
    ),
    (
        (31, 0),
        (31, 6),
        (28, 6),
        (28, 7),
        (26, 7),
        (26, 8),
        (27, 8),
        (27, 10),
        (21, 10),
        (21, 11),
        (23, 11),
        (23, 13),
        (20, 13),

        (20, 13),
        (17, 13),
        (17, 12),
        (16, 12),
        (16, 10),
        (18, 10),
        (18, 9),
        (16, 9),
        (16, 10),
        (13, 10),
        (13, 11),
        (10, 11),
        (10, 12),
        (8, 12),
        (8, 13),
        (6, 13),
        (6, 14),
        (5, 14),
        (5, 16),
        (7, 16),
        (7, 17),
        (6, 17),
        (6, 18),
        (4, 18),
        (4, 20),
        (1, 20),
        (1, 25),
        (2, 25),
        (2, 26),
        (4, 26),
        (4, 27),
        (5, 27),
        (5, 28),
        (6, 28),
        (6, 34),
        (8, 34),
        (8, 36),
        (9, 36),
        (9, 37),
        (12, 37),
        (12, 38),
        (14, 38),
        (14, 39),
        (17, 39),
        (17, 43),
        (19, 43),
        (19, 44),
        (20, 44),
        (20, 46),
        (24, 46),
        (24, 52),
        (25, 52),
        (25, 60),
        (24, 60),
        (24, 61),
        (23, 61),
        (23, 63),
        (21, 63),
        (21, 64),
        (43, 64),
        (43, 65),
        (44, 65),
        (44, 66),
        (46, 66),
        (46, 67),
        (49, 67),
        (49, 76),
        (47, 76),
        (47, 78),
        (46, 78),
        (46, 79),
        (45, 79),
        (45, 80),
        (40, 80),
        (40, 83),
        (39, 83),
        (40, 83),
        (40, 85),
        (39, 85),
        (39, 86),
        (37, 86),
        (37, 87),
        (36, 87),
        (36, 88),
        (35, 88),
        (35, 89),
        (34, 89),
        (34, 90),
        (32, 90),
        (32, 92),
        (31, 92),
        (31, 93),
        (28, 93),
        (28, 94),
        (27, 94),
        (27, 95),
        (26, 95),
        (26, 97),
        (27, 97),
        (27, 100),
        (100, 100),
        (100, 0),
    ),
)

SEAS = (
    (
        (20, 9),
        (20, 12),
        (22, 12),
        (18, 12),
        (18, 11),
        (17, 11),
        (19, 11),
        (19, 9),
    ),
    (
        (19, 9),
        (26, 9),
    ),
    (
        (6, 27),
        (6, 28),
        (9, 28),
        (7, 28),
        (7, 27),
    ),
    (
        (11, 28),
    ),
    (
        (19, 41),
    ),
    (
        (18, 43),
    ),
    (
        (23, 64),
        (25, 64),
        (25, 63),
        (27, 63),
        (27, 64),
        (33, 64),
    ),
    (
        (33, 64),
        (33, 62),
        (35, 62),
        (35, 61),
        (41, 61),
        (41, 64),
    ),
    (
        (42, 61),
    ),
    (
        (42, 63),
        (42, 64),
    ),
    (
        (41, 83),
        (42, 83),
        (42, 82),
        (43, 82),
        (43, 83),
    ),
)


class BgMap(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.startX = x
        self.startY = y
        self.x = self.startX
        self.y = self.startY
        img = image.load(resources.MAPFILE)
        size = img.get_size()
        new_size = (
            int(size[0] * resources.MAPFILE_SCALE),
            int(size[1] * resources.MAPFILE_SCALE),
        )
        self.image = transform.scale(img, new_size)
        self.image.set_alpha(128)
        self.rect = self.image.get_rect()
        self.moveTo(self.x, self.y)
        fg = Surface((self.rect.width, self.rect.height))
        fg.set_alpha(128)
        # fg.fill(Color(0, 255, 0))
        points = []
        seapoints = []
        for sea in SEAS:
            seapoints += BgMap.by_points(sea)
        for land in LANDS:
            points += BgMap.by_points(land, seapoints)
        for p in points:
            rect = Rect(p[0] * MOVE_SPEED, p[1] * MOVE_SPEED, 32, 32)
            draw.rect(fg, Color(255, 255, 0), rect)
        self.image.blit(fg, (0, 0))

    @staticmethod
    def by_points(points, sea=[]):
        size = 128
        lines = dict()
        sealines = dict()
        for s in sea:
            sealine = sealines.get(s[1])
            if sealine is None:
                sealine = []
                sealines[s[1]] = sealine
            sealine.append(s[0])
        for i in range(size):
            lines[i] = []
        edges = [(p, points[i-1]) for i, p in enumerate(points)]
        for edge in edges:
            maxx = max([edge[0][0], edge[1][0]])
            minx = min([edge[0][0], edge[1][0]])
            maxy = max([edge[0][1], edge[1][1]])
            miny = min([edge[0][1], edge[1][1]])

            for x in range(minx, maxx + 1):
                lines[maxy].append(x)
            for y in range(miny, maxy + 1):
                lines[y].append(maxx)

        p = []
        for j in range(size):
            line = lines.get(j)
            if not line:
                continue
            sealine = sealines.get(j)
            if sealine is None:
                sealine = []
            line.sort()
            # for i in line:
            for i in range(line[0], line[-1] + 1):
                if i in sealine:
                    continue
                p.append((i, j))
        return p

    def update(self, xvel, yvel):
        self.xvel = xvel
        self.yvel = yvel
        if (xvel == 0) and (yvel == 0):
            self.xvel = 0
            self.yvel = 0
        self.x += self.xvel
        self.y += self.yvel
        self.moveTo(self.x, self.y)

    def moveTo(self, x, y):
        self.rect.x = MOVE_SPEED * (12 - x)
        self.rect.y = MOVE_SPEED * (9 - y)
        self.testBounds()

    def testBounds(self):
        if self.x <= CONSTS[0][0]:
            self.x = CONSTS[0][0] + 32
        if self.x >= CONSTS[0][1]:
            self.x = CONSTS[0][1] - 32
        if self.y <= CONSTS[1][0]:
            self.y = CONSTS[1][0] + 32
        if self.y >= CONSTS[1][1]:
            self.y = CONSTS[1][1] - 32

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
