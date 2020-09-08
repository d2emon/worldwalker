import math
import pygame


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
            c = pygame.Color(int(vr / scale), int(vg / scale), int(vb / scale), 0)
            pygame.draw.circle(s, c, (self.x, self.y), r*d, d)
            print(r, (vr, vg, vb), c, self.z)
            r = r + 1
