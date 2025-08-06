from utils import randcell

class Helicopter:
    def __init__(self, w, h):
        rc = randcell(w,h)
        rx, ry = rc[0], rc[1]
        self.x = rx
        self.h = h
        self.w = w
        self.y = ry
        self.tank = 0
        self.mxtank = 1

    def move(self, dx, dy):
        nx = self.x + dx
        ny = self.y + dy
        if (nx >= 0 and ny >= 0 and nx < self.h and ny < self.w):
            self.x = nx
            self.y = ny

    def print_stats(self):
        print("TANK ", self.tank, "/", self.mxtank, sep="")
