import math
import pygame
import random
from pygame import Surface, Color, QUIT
from games.space.s_point import SPoint


class SpaceWindow:
    WIN_HEIGHT = 640
    WIN_WIDTH = 800
    DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
    BACKGROUND_COLOR = "#000000"
    START_POS = (400, 300)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.DISPLAY)
        pygame.display.set_caption("Space")
        self.bg = Surface((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.bg.fill(Color(self.BACKGROUND_COLOR))

        points = [SPoint(), ]
        for i in range(10):
            points.append(SPoint(
                random.randint(0, self.WIN_WIDTH),
                random.randint(0, self.WIN_HEIGHT),
                random.randint(0, 255),
                random.randint(-128, 255)
            ))
        for p in points:
            p.draw(self.bg)

        dx = 20
        dy = 20
        for x in range(40):
            vals = []
            for y in range(30):
                vals.append(self.point(x * dx, y * dy, 0, points))
                c = Color(255, 0, 0, 0)
                # pygame.draw.circle(bg, c, (x*dx, y*dy), 5, 5)
            print(vals)

        self.is_running = True

    def run(self):
        while self.is_running:
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.is_running = False
            self.screen.blit(self.bg, (0, 0))
            pygame.display.update()
        raise SystemExit("QUIT")

    @classmethod
    def point(cls, x, y, z, points):
        res = [0, 0, 0, 0]
        scale = 10
        sd = []
        for p in points:
            res[0] = (res[0] + p.x - x) / scale
            res[1] = (res[1] + p.y - y) / scale
            res[2] = (res[2] + p.z - z) / scale
            f = p.f(x, y, z)
            print("f", (x, y, z), p.f(x, y, z))
            d = math.sqrt(sum([math.pow(c, 2) for c in f]))
            print("d", d)
            ds = math.pow(d, 2)
            if ds > 0:
                sd.append(int(10000000 / ds))
            else:
                sd.append(-1)
        print(sd)
        dx = [p.x for p in points]
        dy = [p.y for p in points]
        dz = [p.z for p in points]
        print(dx, dy, dz)
        res[3] = sum(sd)
        return res
