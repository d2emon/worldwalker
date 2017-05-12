#! /usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame import Surface, Color, QUIT
import random
import math

WIN_HEIGHT = 640
WIN_WIDTH = 800
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#000000"
START_POS = (400, 300)


class SPoint:
    def __init__(self, x=0, y=0, z=0, value = 255):
        self.x = x
        self.y = y
        self.z = z
        self.value = value
        print(self.value)

    def change(self, values, r):
        res = []
        for v in values:
            a = v - r
            if a > 0:
                res.append(a)
            else:
                res.append(0)
        return res

    def f(self, *coords):
        res = []
        mycoords = (self.x, self.y, self.z)
        for i in range(3):
            c = coords[i]
            mc = mycoords[i]
            if c == mc:
                res.append(1000000)
            else:
                res.append(int(self.value * 1000000 / math.pow(mc - c, 2)))
        return res

    def draw(self, s):
        scale = 1
        if self.value >= 0:
            vr = self.value * scale
            vb = 0
        else:
            vr = 0
            vb = -1 * self.value * scale
        vg = self.z * scale
        r = 1
        d = 5
        while (vr + vg + vb) > 0:
            vr, vg, vb = self.change([vr, vg, vb], r)
            print((vr / scale), (vg / scale), (vb / scale), 0)
            c = Color((vr / scale), (vg / scale), (vb / scale), 0)
            pygame.draw.circle(s, c, (self.x, self.y), r*d, d)
            print(r, (vr, vg, vb), c, self.z)
            r = r + 1


def point(x, y, z, points):
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

def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Space")
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))

    points = [SPoint(),]
    for i in range(10):
        points.append(SPoint(
            random.randint(0, WIN_WIDTH),
            random.randint(0, WIN_HEIGHT),
            random.randint(0, 255),
            random.randint(-128, 255)
        ))
    for p in points:
        p.draw(bg)

    dx = 20
    dy = 20
    for x in range(40):
        vals = []
        for y in range(30):
            vals.append(point(x*dx, y*dy, 0, points))
            c = Color(255, 0, 0, 0)
            # pygame.draw.circle(bg, c, (x*dx, y*dy), 5, 5)
        print(vals)

    while 1:
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit, "QUIT"
        screen.blit(bg, (0, 0))
        pygame.display.update()


if __name__ == "__main__":
    main()
