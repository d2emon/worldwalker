from pygame import image, draw, transform, Surface, Color, Rect
from pygame.sprite import DirtySprite
from . import data
from .. import resources


class BgMap(DirtySprite):
    def __init__(self, x, y):
        self._layer = 1
        super().__init__()
        self.speed = 0, 0
        self.start_pos = x, y
        self.x, self.y = self.start_pos
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
        for sea in data.SEAS:
            seapoints += BgMap.by_points(sea)
        for land in data.LANDS:
            points += BgMap.by_points(land, seapoints)
        for p in points:
            rect = Rect(p[0] * data.MOVE_SPEED, p[1] * data.MOVE_SPEED, 32, 32)
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

    def set_speed(self, speed):
        self.speed = speed
        if (speed[0] == 0) and (speed[1] == 0):
            self.speed = 0, 0

    def update(self):
        self.x += self.speed[0]
        self.y += self.speed[1]
        self.moveTo(self.x, self.y)

    def moveTo(self, x, y):
        self.rect.x = data.MOVE_SPEED * (12 - x)
        self.rect.y = data.MOVE_SPEED * (9 - y)
        self.testBounds()

    def testBounds(self):
        if self.x <= data.CONSTS[0][0]:
            self.x = data.CONSTS[0][0] + 32
        if self.x >= data.CONSTS[0][1]:
            self.x = data.CONSTS[0][1] - 32
        if self.y <= data.CONSTS[1][0]:
            self.y = data.CONSTS[1][0] + 32
        if self.y >= data.CONSTS[1][1]:
            self.y = data.CONSTS[1][1] - 32
