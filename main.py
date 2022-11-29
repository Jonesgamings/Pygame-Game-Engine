from screen import Game, Map, Camera
from object import Object
import pygame
from random import randint

MAXOBJECTS = 100
MAXCOORD = 10000
MINCOORD = 0
FPS = 60

surf = pygame.Surface((10, 10), pygame.SRCALPHA)
surf.fill((0, 0, 0))

game = Game(FPS)

#game.addObject(Object((0, 0), surf, (2, 0)))

#game.addObject(Object((100, 0), surf, (1, 0)))

for _ in range(MAXOBJECTS):
    surf = pygame.Surface((50, 50), pygame.SRCALPHA)
    surf.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
    x = randint(MINCOORD, MAXCOORD)
    y = randint(MINCOORD, MAXCOORD)
    obj = Object((x, y), surf, (randint(-5, 5), randint(-5, 5)))
    game.addObject(obj)

game.mainloop()