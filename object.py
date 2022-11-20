import pygame

class Object:

    def __init__(self, pos, sprite: pygame.Surface) -> None:
        self.pos = pos
        self.sprite = sprite
        self.rect = self.sprite.get_rect()

    def moveBy(self, dx, dy):
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    def moveTo(self, x, y):
        self.pos = (x, y)

    def draw(self, screen: pygame.Surface, zoom, camStart):
        x = self.pos[0] / zoom
        y = self.pos[1] / zoom
        screenPosX = (x - camStart[0] / zoom) - self.rect.width / 2
        screenPosY = (y - camStart[1] / zoom) - self.rect.height / 2
        toBlit = pygame.transform.rotozoom(self.sprite, 0, 1/zoom)
        screen.blit(toBlit, (screenPosX, screenPosY))
