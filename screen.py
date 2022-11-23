import pygame
import json
from object import Object
from random import randint
from time import time

pygame.init()
pygame.font.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)

class GUI:

    def __init__(self) -> None:
        pass

class Game:

    def __init__(self, mapSize, fps) -> None:
        self.mapSize = mapSize
        self.FPS = fps

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.map = Map(self.mapSize, self.mapSize)
        self.camera = Camera(self.map, self.screen)
        self.running = False

    def displayObjects(self):
        displayedArea = self.camera.getDisplayedArea()
        objects = self.map.getObjects(displayedArea)
        for object in objects:
            object.draw(self.screen, self.camera)

    def addObject(self, object):
        self.map.addObject(object)

    def doMoveInputs(self, dt):
        moveVertical = 0
        moveHorizontal = 0
        keys = pygame.key.get_pressed()
        buttons = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            moveVertical -= self.camera.moveSpeed * self.camera.zoom * dt

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            moveVertical += self.camera.moveSpeed * self.camera.zoom * dt

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            moveHorizontal -= self.camera.moveSpeed * self.camera.zoom * dt

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            moveHorizontal += self.camera.moveSpeed * self.camera.zoom * dt

        if buttons[0]:
            pass

        if buttons[1]:
            pass

        if buttons[2]:
            pass
        
        self.camera.moveBy(moveHorizontal, moveVertical)

    def doZoomInputs(self, event, dt):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.camera.zoomBy(-self.camera.zoomSpeed * dt)

            if event.button == 5:
                self.camera.zoomBy(self.camera.zoomSpeed * dt)

    def displayTextInfo(self):
        FONTSIZE = 20
        font = pygame.font.SysFont("arial", FONTSIZE, True)

        fps = f"FPS: {round(self.clock.get_fps(), 1)}"
        fpsSurf = font.render(fps, False, RED)

        pos = f"X: {round(self.camera.pos[0], 1)}, Y: {round(self.camera.pos[1], 1)}"
        posSurf = font.render(pos, False, RED)

        zoom = f"ZOOM: {round(1/self.camera.zoom, 3)}"
        zoomSurf = font.render(zoom, False, RED)

        self.screen.blit(fpsSurf, (0, 0))
        self.screen.blit(posSurf, (0, FONTSIZE))
        self.screen.blit(zoomSurf, (0, FONTSIZE * 2))

        pygame.draw.circle(self.screen, (230, 230, 230), (self.screen.get_size()[0] / 2, self.screen.get_size()[1] / 2), 3)

    def mainloop(self):
        self.running = True
        start = time()
        lastTick = 0
        while self.running:
            
            gametime = time() - start

            dt = (gametime - lastTick) * self.clock.get_fps()
            print(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                self.doZoomInputs(event, dt)

            self.doMoveInputs(dt)

            self.screen.fill(WHITE)
            self.displayObjects()
            self.displayTextInfo()

            lastTick = gametime

            self.clock.tick(self.FPS)
            pygame.display.flip()

        pygame.quit()

class Camera:

    def __init__(self, map, screen) -> None:
        self.screen = screen
        self.map = map
        self.pos = (0, 0)
        self.zoom = 1
        self.moveSpeed = 5
        self.zoomSpeed = 0.05
        self.displayingArea = None

    def updateDisplayedArea(self):
        screenX, screenY = self.screen.get_size()
        topLX = self.pos[0] - ((screenX * self.zoom) / 2)
        topLY = self.pos[1] - ((screenY * self.zoom) / 2)
        width = screenX * self.zoom
        height = screenY * self.zoom
        if (topLX * -1) < width and (topLY * -1) < height:
            if (topLX < self.map.width) and (topLY < self.map.height):
                self.displayingArea = pygame.Rect(topLX, topLY, width, height)
                return True

            else:
                return False
        
        return False

    def moveTo(self, x, y):
        old = self.pos
        self.pos = (x, y)
        if not self.updateDisplayedArea():
            self.pos = old

    def moveBy(self, dx, dy):
        old = self.pos
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
        if not self.updateDisplayedArea():
            self.pos = old

    def zoomTo(self, zoom):
        self.zoom = zoom

    def zoomBy(self, zoom):
        self.zoom += zoom

    def getDisplayedArea(self):
        self.updateDisplayedArea()
        return self.displayingArea

class Map:

    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.objects = []

    def getObjects(self, displayedArea: pygame.Rect):
        objectsInView = []
        for object in self.objects:
            if displayedArea.colliderect(object.rect):
                objectsInView.append(object)
        return objectsInView

    def addObject(self, object):
        self.objects.append(object)

    def saveMap(self, filename):
        data = {}
        for i, object in enumerate(self.objects):
            data[i] = object.save()
        
        with open(f"{filename}.json", "w") as file:
            json.dump(data, file, indent=4)

    def loadMap(self, filename):
        with open(f"{filename}.json", "r") as file:
            data = json.load(file)

        for object in data.values():
            toAdd = Object.createMe(object)
            self.objects.append(toAdd)

if __name__ == "__main__":
    MAXOBJECTS = 5000
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