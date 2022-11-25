import pygame
import math

class Object:

    def __init__(self, pos, sprite: pygame.Surface, velocity = (0, 0)) -> None:
        self.type = "DEFAULT"
        self.pos = pos
        self.sprite = sprite
        self.rect = self.sprite.get_rect()
        self.vx, self.vy = velocity
        self.updateRect()

    def __str__(self) -> str:
        return f"{self.type}: {self.sprite.get_at((0, 0))}"

    def __repr__(self) -> str:
        return f"{self.type}: {self.sprite.get_at((0, 0))}"

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
        self.moveBy(self.vx, self.vy)

    def checkClick(self, pos):
        self.updateRect()
        if self.rect.collidepoint(pos):
            return True

        return False

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

class GravityObject(Object):

    GRAVCONSTANT = 0.00005

    def __init__(self, pos, sprite: pygame.Surface, mass) -> None:
        super().__init__(pos, sprite)
        self.type = "GRAVITY_OBJECT"
        self.mass = mass

    def normalize(self, vector):
        currentLen = math.sqrt((vector[0] ** 2) + (vector[1] ** 2))
        newVector = vector[0] / currentLen, vector[1] / currentLen
        return newVector

    def update(self, game):
        super().update(game)
        for object in game.map.objects:
            if object != self:
                if object.type == self.type:
                    normal = self.normalize((object.pos[0] - self.pos[0], object.pos[1] - self.pos[1]))
                    force = normal[0] * GravityObject.GRAVCONSTANT * object.mass, normal[1] * GravityObject.GRAVCONSTANT * object.mass
                    self.vx += force[0]
                    self.vy += force[1]

        self.moveBy(self.vx, self.vy)