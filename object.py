import pygame
import math

class Object:

    def __init__(self, pos, sprite: pygame.Surface, velocity = (0, 0), canBounce = True) -> None:
        self.type = "DEFAULT"
        self.pos = pos
        self.sprite = sprite
        self.rect = self.sprite.get_rect()
        self.vx, self.vy = velocity
        self.canBounce = canBounce
        self.updateRect()

    def updateRect(self):
        self.sprite.get_rect()
        self.rect.center = self.pos

    def moveBy(self, dx, dy):
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
        self.updateRect()

    def moveTo(self, x, y):
        self.pos = (x, y)
        self.updateRect()

    def draw(self, screen: pygame.Surface, camera):
        self.updateRect()
        x = self.rect.topleft[0] / camera.zoom
        y = self.rect.topleft[1] / camera.zoom
        screenPosX = (x - camera.displayingArea.topleft[0] / camera.zoom)
        screenPosY = (y - camera.displayingArea.topleft[1] / camera.zoom)
        toBlit = pygame.transform.rotozoom(self.sprite, 0, 1 / camera.zoom)
        screen.blit(toBlit, (screenPosX, screenPosY))

    def collides(self, rect):
        self.updateRect()
        if self.rect.colliderect(rect):
            return True

        return False

    def copy(self):
        return Object((0, 0), self.sprite)

    def bounce(self, bounceObj):
        x1, y1 = self.pos
        x2, y2 = bounceObj.pos

        if y1 > y2:
            if self.vy < 0:
                self.vy *= -1

        if y2 > y1:
            if self.vy > 0:
                self.vy *= -1

        if x1 > x2:
            if self.vx < 0:
                self.vx *= -1

        if x2 > x1:
            if self.vx > 0:
                self.vx *= -1

    def update(self, map):
        self.updateRect()
        rect = self.rect.copy()
        rect.center = (self.pos[0] + self.vx, self.pos[1] + self.vy)
        collides = map.collides(rect, self)
        if not collides:
            self.moveBy(self.vx, self.vy)

        else:
            if self.canBounce:
                self.bounce(collides)