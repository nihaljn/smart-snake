from game import Game
import time
import importlib

for i in range(3):
    game = Game()
    game.play()
    time.sleep(1)