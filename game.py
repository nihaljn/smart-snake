import snake
import cube
import pygame
import random
import time
from nn import Brain
import numpy as np

class Game(object):

    def __init__(self):
        
        pygame.init()
        
        self.width = 1000
        self.height = 1000
        self.rows = 40

        # initializes the window and returns a surface of size (width, height)
        self.window = pygame.display.set_mode((self.width,self.height + 50))
        # Initialize player at a random position
        x = np.random.randint(1, self.rows)
        y = np.random.randint(1, self.rows)
        # instantiate the player
        self.player = snake.Snake((255,0,0), (x, y))
        # placing a snack cube at a random position
        self.snack = cube.Cube(self.random_snack(), color = (128,0,128))
        # instantiate an object to help keep track of time
        self.clock = pygame.time.Clock()

    def draw_grid(self):

        sizeBtwn = self.width // self.rows
        x = 0
        y = 0
        for i in range(self.rows):
            x = x + sizeBtwn
            y = y + sizeBtwn
            pygame.draw.line(self.window, (255,255,255), (x,0),(x,self.width))
            pygame.draw.line(self.window, (255,255,255), (0,y),(self.width,y))

    def redraw_window(self):

        self.window.fill((0,0,0))
        self.player.draw(self.window)
        self.snack.draw(self.window)
        # self.draw_grid()
        font = pygame.font.Font('courier_new.ttf', 32)
        text = font.render('Score: '+str(len(self.player.body) - 1), True, (255,255,255))
        self.window.blit(text, (20,510))
        pygame.display.update()

    def random_snack(self):
        positions = self.player.body
        while True:
            x = random.randrange(self.rows)
            y = random.randrange(self.rows)

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
            
    def is_dir_safe(self, pos, dir, steps):

        '''
        Checks whether the specified number of steps along dir would cause any damage. The directions are as described below:
        _______ [0]
        |
        |
        |
        [1]
        left  : (-1, 0)
        right : (1, 0)
        up    : (0, -1)
        down  : (0, 1)

        Arguments:
            pos: The current position of head of player
            dir: The absolute direction in which the player wishes to move
            steps: The number of steps the player wishes to take along specified direction

        Returns:
            True if the move described would not cause any damage, else returns False
        '''

        destX = (pos[0] + (steps*dir[0])) % self.rows
        destY = (pos[1] + (steps*dir[1])) % self.rows

        positions = []
        for c in self.player.body:
            positions.append(c.pos)

        if (destX, destY) in positions or self.hits_wall((destX, destY)):
            return False
        return True

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

    def reset(self):

        self.window = pygame.display.set_mode((self.width,self.height + 50))
        x = np.random.randint(1, self.rows)
        y = np.random.randint(1, self.rows)
        self.player.reset((x, y))
        self.snack = cube.Cube(self.random_snack(), color = (128,0,128))
        self.clock = pygame.time.Clock()

    def play(self, brain=None):

        '''
        Plays the game using self's player and snack.
        '''
        self.player.add_cube()
        self.player.add_cube()
        flag = True
        start = time.time()
        currentMove = 0
        prevMove = 0
        mrk = 0
        cnt_moves = 0
        lifetime = 0
        while flag:
            lifetime += 1
            # pause the game for 50ms amount of time
            # to let the video display update
            pygame.time.delay(50)

            # limit the frame rate to 10fps
            self.clock.tick(30)

            # looping over all the events in the queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # returns {key : isPressed} indicating the boolean isPressed state
            # of all keys on the keyboard
            # COMMENT TO DISABLE AUTOPLAY
            # keyPressed = pygame.key.get_pressed()
            # END UNCOMMENT
            '''
            275: LEFT
            273: RIGHT
            274: DOWN
            276: UP
            '''
            # COMMENT TO DISABLE AUTOPLAY
            # keyPressed = {275:False, 273:False, 274:False, 276:False}
            # diff = time.time() - start
            # if random.random() < (diff/(diff+1)):
            #     now = random.randrange(4) + 273
            #     start = time.time()
            #     keyPressed[now] = True
            # END COMMENT
            
            if brain:
                # Gameplay by Neural Net
                keys = [275, 273, 274, 276]
                percept = self.sense_percepts()
                moves = brain.move(percept)
                keyPressed = {}
                for i, key in enumerate(keys):
                    keyPressed[key] = moves[i]
            else:
                # Human player
                keyPressed = pygame.key.get_pressed()
            
            for key in (pygame.K_LEFT,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_UP):
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
                self.snack = cube.Cube(self.random_snack(), color = (128,0,128))
                cnt_moves = 0

            # Exit if hits the wall
            if self.hits_wall(self.player.body[0].pos):
                return len(self.player.body), lifetime
            
            for x in range(len(self.player.body)):
                if len(self.player.body) > 1 and self.player.body[x].pos in list(map(lambda z:z.pos,self.player.body[x+1:])) or cnt_moves > 300:
                    return len(self.player.body), lifetime

            self.redraw_window()
            cnt_moves += 1

if __name__ == '__main__':

    game = Game()
    game.play()