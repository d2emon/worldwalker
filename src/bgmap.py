import resources
from pygame import image, sprite, draw, transform, Surface, Color, Rect


MOVE_SPEED = 32
WIDTH = 800
HEIGHT = 600
# CONSTS = ((-1600, 1600), (-1280, 1280))
LENGTH = 3200 * MOVE_SPEED
CONSTS = ((-LENGTH, LENGTH), (-LENGTH, LENGTH))
POINTS = (
    (17, 0),
    (17, 1),
    (18, 1),
    (18, 3),
    (17, 3),
    (17, 4),
    (18, 4),
    (18, 5),
    (20, 5),
    (20, 6),
    (22, 6),
    (22, 4),
    (20, 4),
    (20, 3),
    (19, 3),
    (19, 2),
    (20, 2),
    (20, 0),
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
        points = BgMap.by_points(POINTS)
        for p in points:
            rect = Rect(p[0] * MOVE_SPEED, p[1] * MOVE_SPEED, 32, 32)
            draw.rect(fg, Color(0, 255, 0), rect)
        self.image.blit(fg, (0, 0))

    @staticmethod
    def by_points(points):
        lines = dict()
        for i in range(32):
            lines[i] = []
        edges = [(p, points[i-1]) for i, p in enumerate(points)]
        for edge in edges:
            if edge[0][0] > edge[1][0]:
                maxx = edge[0][0]
                minx = edge[1][0]
            else:
                maxx = edge[1][0]
                minx = edge[0][0]

            if edge[0][1] > edge[1][1]:
                maxy = edge[0][1]
                miny = edge[1][1]
            else:
                maxy = edge[1][1]
                miny = edge[0][1]

            for x in range(minx, maxx):
                lines[maxy].append(x)
            for y in range(miny, maxy):
                lines[y].append(maxx)

        p = []
        for j in range(32):
            line = lines.get(j)
            if line is None:
                continue
            for i in line:
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
