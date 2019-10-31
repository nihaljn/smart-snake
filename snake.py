import pygame
import cube
import random

class Snake(object):

    def __init__(self, color, pos):

        self.color = color
        self.head = cube.Cube(pos)
        self.dirnx = 0
        self.dirny = 1

        # list of Cube objects representing the body of the player
        self.body = []
        self.body.append(self.head)

        # dictionary to store the positions at which some turn was made
        # {position : turnDirection}
        self.turns = {}

    def move(self, keys = {}):

        # updating turns accordingly
        # to record the turn made at that position
        if keys == pygame.K_LEFT:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif keys == pygame.K_RIGHT:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif keys == pygame.K_UP:
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif keys == pygame.K_DOWN:
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, cube in enumerate(self.body):
            
            currentPos = cube.pos[:]

            if currentPos in self.turns:
                # currentPos is unhandled
                turn = self.turns[currentPos]

                # handling currentPos
                cube.move(turn[0],turn[1])

                if i == len(self.body)-1:
                    # all the cubes have gone through this turn
                    self.turns.pop(currentPos)
            else:
                # checking for fold conditions 
                # updating position accordingly
                if cube.dirnx == -1 and cube.pos[0] <= 0: 
                    cube.pos = (cube.rows-1, cube.pos[1])
                elif cube.dirnx == 1 and cube.pos[0] >= cube.rows-1: 
                    cube.pos = (0,cube.pos[1])
                elif cube.dirny == 1 and cube.pos[1] >= cube.rows-1: 
                    cube.pos = (cube.pos[0], 0)
                elif cube.dirny == -1 and cube.pos[1] <= 0: 
                    cube.pos = (cube.pos[0],cube.rows-1)
                else:
                    # move the cube without updating directions
                    cube.move(cube.dirnx,cube.dirny)
    
    def add_cube(self):

        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # adding new cube to appropriate position in the snake
        if dx == 1 and dy == 0:
            self.body.append(cube.Cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube.Cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube.Cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube.Cube((tail.pos[0],tail.pos[1]+1)))

        # updating motion of the newly added cube
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):

        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

    def reset(self, pos):

        self.head = cube.Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1