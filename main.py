import snake
import cube
import pygame
import random

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

    width = 500
    height = 500
    rows = 20

    window = pygame.display.set_mode((width,height))
    player = snake.Snake((255,0,0), (10,10))
    snack = cube.Cube(random_snack(), color = (0,255,0))
    flag = True

    clock = pygame.time.Clock()

    while flag:

        pygame.time.delay(50)
        clock.tick(10)
        player.move()

        if player.body[0].pos == snack.pos:
            player.add_cube()
            snack = cube.Cube(random_snack(), color = (0,255,0))
        
        for x in range(len(player.body)):
            if player.body[x].pos in list(map(lambda z:z.pos,player.body[x+1:])):
                print('Score: ', len(player.body))
                player.reset((10,10))
                break

        redraw_window(window)