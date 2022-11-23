import pygame

class Object:

    def __init__(self, pos, sprite: pygame.Surface) -> None:
        self.pos = pos
        self.sprite = sprite
        self.rect = self.sprite.get_rect()
        self.updateRect()

    def updateRect(self):
        self.sprite.get_rect()
        self.rect.topleft = self.pos

    def moveBy(self, dx, dy):
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
        self.updateRect()

    def moveTo(self, x, y):
        self.pos = (x, y)
        self.updateRect()

    def draw(self, screen: pygame.Surface, camera):
        x = self.pos[0] / camera.zoom
        y = self.pos[1] / camera.zoom
        screenPosX = (x - camera.displayingArea.topleft[0] / camera.zoom)
        screenPosY = (y - camera.displayingArea.topleft[1] / camera.zoom)
        toBlit = pygame.transform.rotozoom(self.sprite, 0, 1 / camera.zoom)
        screen.blit(toBlit, (screenPosX, screenPosY))

    def update(self, game):
        pass

    def imageToJSON(self):
        pass

    def JSONtoImage(self):
        pass

    def save(self):
        data = {
            "POSITION": self.pos,
            "WIDTH": self.rect.width,
            "HEIGHT": self.rect.height,
            "IMAGE": None
        }
        return data

    @classmethod
    def createMe(self, jsonFile):
        pos = jsonFile["POSITION"]
        width = jsonFile["WIDTH"]
        height = jsonFile["HEIGHT"]
        imageRaw = jsonFile["IMAGE"]
        return Object(pos, imageRaw)
