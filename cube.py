import pygame

class Cube(object):

    rows = 20
    w = 500

    def __init__(self, start, dirnx = 1, dirny = 0, color = (255,0,0)):

        # current position of cube
        self.pos = start
        # horizontal direction of movement of cube
        self.dirnx = 1
        # vertical direction of movement of cube
        self.dirny = 0
        # color of cube
        self.color = color

    def draw(self, surface, head = False):

        dist = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dist+1, j*dist+1, dist-2, dist-2))
        if head:
            self.color = (255,255,255)

    def move(self, dirnx, dirny):

        self.dirnx = dirnx
        self.dirny = dirny
        # updating the position of the cube
        if self.dirnx == -1 and self.pos[0] <= 0: 
            self.pos = (self.rows-1, self.pos[1])
        elif self.dirnx == 1 and self.pos[0] >= self.rows-1: 
            self.pos = (0,self.pos[1])
        elif self.dirny == 1 and self.pos[1] >= self.rows-1: 
            self.pos = (self.pos[0], 0)
        elif self.dirny == -1 and self.pos[1] <= 0: 
            self.pos = (self.pos[0],self.rows-1)
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)