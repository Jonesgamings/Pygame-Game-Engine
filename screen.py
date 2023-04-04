import pygame
import json
from object import Object
from time import time

pygame.init()
pygame.font.init()

#EVERY TIME OBJECT MOVE CHECK IF IN FRAME
#ADD VISIBEL TO OBJECT
#JUST DRAW VISIBLE OBJECTS

WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHTGREY = (210, 210, 210)

class Game:

    def __init__(self,fps) -> None:
        self.FPS = fps

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screenWidth, self.screenHeight = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.map = Map()
        self.camera = Camera(self.screen)
        self.running = False

    def displayObjects(self):
        displayedArea = self.camera.getDisplayedArea()
        objects = self.map.getObjects(displayedArea)
        for object in objects:
            object.draw(self.screen, self.camera)

    def updateObjects(self):
        for object in self.map.objects:
            object.update(self.map)

    def addObject(self, object):
        self.map.addObject(object)

    def doMoveInputs(self, dt):
        moveVertical = 0
        moveHorizontal = 0
        keys = pygame.key.get_pressed()
        buttons = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            moveVertical -= self.camera.moveSpeed * self.camera.zoom * dt

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            moveVertical += self.camera.moveSpeed * self.camera.zoom * dt

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            moveHorizontal -= self.camera.moveSpeed * self.camera.zoom * dt

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            moveHorizontal += self.camera.moveSpeed * self.camera.zoom * dt

        if buttons[0]: #LEFT
            pass

        if buttons[2]: #RIGHT
            pass

        if buttons[1]: #MIDDLE
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

        pygame.draw.circle(self.screen, (230, 230, 230), (self.screenWidth / 2, self.screenHeight / 2), 3)

    def mainloop(self):
        self.running = True
        start = time()
        lastTick = 0
        while self.running:
            
            gametime = time() - start

            dt = (gametime - lastTick) * self.clock.get_fps()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                self.doZoomInputs(event, dt)

            self.doMoveInputs(dt)
            self.updateObjects()

            self.screen.fill(WHITE)
            self.displayObjects()
            self.displayTextInfo()

            lastTick = gametime

            self.clock.tick(self.FPS)
            pygame.display.flip()

        pygame.quit()

class Camera:

    def __init__(self, screen) -> None:
        self.screen = screen
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
        self.displayingArea = pygame.Rect(topLX, topLY, width, height)
        return True

    def moveTo(self, x, y):
        self.pos = (x, y)
        self.updateDisplayedArea()

    def moveBy(self, dx, dy):
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
        self.updateDisplayedArea()

    def zoomTo(self, zoom):
        self.zoom = zoom
        self.updateDisplayedArea()

    def zoomBy(self, zoom):
        self.zoom += zoom
        self.updateDisplayedArea()

    def getDisplayedArea(self):
        self.updateDisplayedArea()
        return self.displayingArea

class Map:

    def __init__(self) -> None:
        self.objects = []

    def getObjects(self, displayedArea: pygame.Rect):
        objectsInView = []
        for object in self.objects:
            if displayedArea.colliderect(object.rect):
                objectsInView.append(object)
        return objectsInView

    def addObject(self, object):
        self.objects.append(object)

    def collides(self, rect, objectCasting):
        new_list = self.objects.copy()
        new_list.remove(objectCasting)
        index = rect.collidelist(new_list)
        if index == -1:
            return False
        
        else:
            return new_list[index]