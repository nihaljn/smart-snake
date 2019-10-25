import pygame

class Cube(object):

    rows = 20
    w = 500

    def __init__(self, start, dirnx = 1, dirny = 0, color = (255,0,0)):

        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def draw(self, surface, head = False):

        dist = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dist+1, j*dist+1, dist-2, dist-2))
        if head:
            self.color = (255,255,0)

    def move(self, dirnx, dirny):

        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)