import snake
import cube
import pygame
import random
import time

def draw_grid(surface):

    global rows, width

    sizeBtwn = width // rows
    x = 0
    y = 0
    for i in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (255,255,255), (x,0),(x,width))
        pygame.draw.line(surface, (255,255,255), (0,y),(width,y))

def redraw_window(surface):

    global rows, width, player, snack

    surface.fill((0,0,0))
    player.draw(surface)
    snack.draw(surface)
    draw_grid(surface)
    font = pygame.font.Font('courier_new.ttf', 32)
    text = font.render('Score: '+str(len(player.body) - 1), True, (255,255,255))
    window.blit(text, (20,510))
    pygame.display.update()

def random_snack():

    global rows, player

    positions = player.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        # ensuring the snack does not occur
        # along the body of snake
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x,y)


if __name__ ==  '__main__':

    global width, rows, player, snack

    pygame.init()

    width = 500
    height = 500
    rows = 20

    # initializes the window and returns a surface of size (width, height)
    window = pygame.display.set_mode((width,height + 50))

    # instantiate the player
    player = snake.Snake((255,0,0), (10,10))

    # placing a snack cube at a random position
    snack = cube.Cube(random_snack(), color = (128,0,128))
    flag = True

    # instantiate an object to help keep track of time
    clock = pygame.time.Clock()

    font = pygame.font.Font('courier_new.ttf', 32)
    text = font.render('Snake', True, (255,255,255))
    window.blit(text, (20,20))
    start = time.time()

    currentMove = 0
    prevMove = 0

    while flag:

        # pause the game for 50ms amount of time
        # to let the video display update
        pygame.time.delay(50)

        # limit the frame rate to 10fps
        clock.tick(10)

        # looping over all the events in the queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # returns {key : isPressed} indicating the boolean isPressed state
        # of all keys on the keyboard
        # UNCOMMENT TO DISABLE AUTOPLAY
        # keyPressed = pygame.key.get_pressed()
        # END UNCOMMENT

        # COMMENT TO DISABLE AUTOPLAY
        keyPressed = {275:False, 273:False, 274:False, 276:False}
        diff = time.time() - start
        if random.random() < (diff/(diff+1)):
            now = random.randrange(4) + 273
            start = time.time()
            keyPressed[now] = True
        # END COMMENT

        for key in (pygame.K_LEFT,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_UP):
            if keyPressed[key]:
                prevMove = currentMove
                currentMove = key
                if prevMove == 0:
                    prevMove = currentMove
                if prevMove == 273 and currentMove == 274 or prevMove == 274 and currentMove == 273:
                    currentMove = prevMove
                if prevMove == 275 and currentMove == 276 or prevMove == 276 and currentMove == 275:
                    currentMove = prevMove
                break
        player.move(currentMove)

        if player.body[0].pos == snack.pos:
            player.add_cube()
            snack = cube.Cube(random_snack(), color = (128,0,128))
        
        for x in range(len(player.body)):
            if player.body[x].pos in list(map(lambda z:z.pos,player.body[x+1:])):
                print('Score: ', len(player.body))
                player.reset((10,10))
                break

        redraw_window(window)