import pygame

def drawGrid(width, rows, surface):
    sizeBtwn = width // rows
    x = 0
    y = 0
    for i in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (255,255,255), (x,0),(x,width))
        pygame.draw.line(surface, (255,255,255), (0,y),(width,y))

def redrawWindow(width, rows, surface):
    surface.fill((0,0,0))
    drawGrid(width, rows, surface)
    pygame.display.update()

def main():
    width = 500
    height = 500
    rows = 20

    window = pygame.display.set_mode((width,height))
    # player = snake((255,0,0), (10,10))
    clock = pygame.time.Clock()

    flag = True
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        redrawWindow(width, rows, window)