from screen import Game, Map, Camera
from object import Object, GravityObject
import pygame
from random import randint

MAXOBJECTS = 100
MAXCOORD = 10000
MINCOORD = 0

surf = pygame.Surface((50, 50), pygame.SRCALPHA)
surf.fill((0, 0, 0))

game = Game(10 ** 8, 0)

for _ in range(MAXOBJECTS):
    surf = pygame.Surface((50, 50), pygame.SRCALPHA)
    surf.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
    x = randint(MINCOORD, MAXCOORD)
    y = randint(MINCOORD, MAXCOORD)
    obj = Object((x, y), surf)
    game.addObject(obj)

game.mainloop()