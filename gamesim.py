import time
from nn import Brain
import numpy as np
import pygame

class GameSim:

    def __init__(self):
        
        self.width = 1000
        self.height = 1000
        self.rows = 40

        # Initialize player at a random position
        x = np.random.randint(1, self.rows)
        y = np.random.randint(1, self.rows)
        
        # instantiate the player
        self.player = Snake((x, y))
        # placing a snack cube at a random position
        self.snack = Cube(self.random_snack())

    def random_snack(self):
        positions = self.player.body
        while True:
            x = np.random.randint(1, self.rows)
            y = np.random.randint(1, self.rows)
            # ensuring the snack does not occur
            # along the body of snake
            if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0 or self.hits_wall((x, y)):
                continue
            else:
                break
        return (x,y)

    def hits_wall(self, pos):
        if pos[0] <= 0 or pos[1] <= 0 or pos[0] >= self.rows-1 or pos[1] >= self.rows-1:
            return True
        return False

    def sense_percepts(self):
        '''
        Retrieves percept from all 4 directions
        '''
        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]
        # Food
        dirf = np.zeros(4)
        # Obstacle
        diro = np.zeros(4)
        x, y = self.player.body[0].pos
        body_pos = []
        for b in self.player.body:
            body_pos.append(b.pos)
        for i in range(4):
            nx = x
            ny = y
            distance = 0
            # Look in that direction until hit by wall
            while not self.hits_wall((nx, ny)):
                if (nx, ny) == self.snack.pos:
                    # Found food in direction 'i'
                    dirf[i] = 1
                nx += dx[i]
                ny += dy[i]
                distance += 1
                if (nx, ny) in body_pos and diro[i] == 0:
                    # Found tail in this direction
                    diro[i] = 1 / distance
            if diro[i] == 0:
                diro[i] = 1 / max(distance, 1)
        percept = np.concatenate([dirf, diro])
        return percept

    def play(self, brain):

        '''
        Plays the game using self's player and snack.
        '''
        self.player.add_cube()
        self.player.add_cube()
        flag = True
        currentMove = 0
        prevMove = 0
        cnt_moves = 0
        lifetime = 0
        while flag:
            lifetime += 1
            '''
            275: LEFT
            273: RIGHT
            274: DOWN
            276: UP
            '''
            # Gameplay by Neural Net
            keys = [275, 273, 274, 276]
            percept = self.sense_percepts()
            moves = brain.move(percept)
            keyPressed = {}
            for i, key in enumerate(keys):
                keyPressed[key] = moves[i]
            
            for key in (275, 273, 274, 276):
                if keyPressed[key]:
                    prevMove = currentMove
                    currentMove = key
                    if prevMove == 0:
                        prevMove = currentMove
                    if prevMove == 273 and currentMove == 274 or prevMove == 274 and currentMove == 273:
                        return len(self.player.body), lifetime
                    if prevMove == 275 and currentMove == 276 or prevMove == 276 and currentMove == 275:
                        return len(self.player.body), lifetime
                    break

            self.player.move(currentMove)

            if self.player.body[0].pos == self.snack.pos:
                self.player.add_cube()
                self.snack = Cube(self.random_snack())
                cnt_moves = 0

            # Exit if hits the wall
            if self.hits_wall(self.player.body[0].pos):
                return len(self.player.body), lifetime
            
            if (len(self.player.body) > 1 and self.player.body[0].pos in list(map(lambda z:z.pos,self.player.body[1:]))) or cnt_moves > 300:
                return len(self.player.body), lifetime

            cnt_moves += 1


class Snake:

    def __init__(self, pos):

        self.head = Cube(pos)
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
            self.body.append(Cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0],tail.pos[1]+1)))

        # updating motion of the newly added cube
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


class Cube:

    rows = 40
    w = 1000

    def __init__(self, start, dirnx = 1, dirny = 0):

        # current position of cube
        self.pos = start
        # horizontal direction of movement of cube
        self.dirnx = 1
        # vertical direction of movement of cube
        self.dirny = 0

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

if __name__ == '__main__':

    game = GameSim()
    print(game.play(Brain([8, 16])))