import pygame
import json
from object import Object, GravityObject
from random import randint, uniform
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
        self.camera = Camera(self.map, self.screen)
        self.GUI = GUI((self.screenWidth * 2 / 3, 0), self.screenWidth / 3, self.screenHeight)
        self.running = False

    def displayObjects(self):
        displayedArea = self.camera.getDisplayedArea()
        objects = self.map.getObjects(displayedArea)
        for object in objects:
            object.draw(self.screen, self.camera)

    def updateObjects(self):
        for object in self.map.objects:
            object.update(self)

    def addObject(self, object):
        self.map.addObject(object)

    def screenToReal(self, pos):
        display = self.camera.getDisplayedArea()
        realX = (display.width * pos[0] / self.screenWidth) + display.topleft[0]
        realY = (display.width * pos[1] / self.screenWidth) + display.topleft[1]

        return (realX, realY)

    def checkObjectClicked(self, pos):
        realPos = self.screenToReal(pos)
        for object in self.map.getObjects(self.camera.getDisplayedArea()):
            if object.checkClick(realPos):
                return object

        return None

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
            if not self.GUI.checkClick(mousePos) and self.GUI.selectedObject:
                newObj = self.GUI.selectedObject.copy()
                realPos = self.screenToReal(mousePos)
                newObj.moveTo(realPos[0], realPos[1])
                self.addObject(newObj)

        if buttons[2]: #RIGHT
            if not self.GUI.checkClick(mousePos):
                clickedOn = self.checkObjectClicked(mousePos)
                if clickedOn:
                    self.map.objects.remove(clickedOn)

        if buttons[1]: #MIDDLE
            if not self.GUI.checkClick(mousePos):
                self.GUI.selectedObject = self.checkObjectClicked(mousePos)
        
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

        selected = f"SELECTED: {self.GUI.selectedObject}"
        selectedSurf = font.render(selected, False, RED)

        self.screen.blit(fpsSurf, (0, 0))
        self.screen.blit(posSurf, (0, FONTSIZE))
        self.screen.blit(zoomSurf, (0, FONTSIZE * 2))
        self.screen.blit(selectedSurf, (0, FONTSIZE * 3))

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

                    if event.key == pygame.K_TAB:
                        self.GUI.toggleVisible()

                self.doZoomInputs(event, dt)

            self.doMoveInputs(dt)
            self.updateObjects()

            self.screen.fill(WHITE)
            self.displayObjects()
            self.displayTextInfo()
            self.GUI.draw(self.screen)

            lastTick = gametime

            self.clock.tick(self.FPS)
            pygame.display.flip()

        pygame.quit()

class GUIElement:

    def __init__(self, pos, size, type_, sprite) -> None:
        self.pos = pos
        self.width, self.height = size
        self.objectType = type_
        self.objectSprite = sprite

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def checkClick(self, pos):
        if self.rect.collidepoint(pos):
            return True

        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.objectSprite.get_at((0, 0)), self.rect)

class GUI:

    def __init__(self, pos, width, height) -> None:
        self.pos = pos
        self.width = width
        self.height = height
        self.visible = False

        self.rows = 10
        self.columns = 10

        self.gridX = 0
        self.gridY = 0

        self.surface = pygame.Surface((width, height))
        self.surface.fill(LIGHTGREY)
        self.surface.set_alpha(128)
        self.rect = self.surface.get_rect()
        self.elements = []
        self.selectedObject = None
        self.updateRect()
        self.updateGrid()

    def updateGrid(self):
        self.gridX = self.width / self.columns
        self.gridY = self.height / self.rows
    
    def createElement(self, pos, type_, sprite):
        realX = pos[0] * self.gridX + self.pos[0]
        realY = pos[1] * self.gridY + self.pos[1]
        element = GUIElement((realX, realY), (self.gridX - 1, self.gridY - 1), type_, sprite)
        self.elements.append(element)

    def updateRect(self):
        self.rect = self.surface.get_rect()
        self.rect.topleft = self.pos

    def toggleVisible(self):
        self.visible = not self.visible

    def drawElements(self, screen):
        for element in self.elements:
            element.draw(screen)

    def draw(self, screen):
        if self.visible:
            screen.blit(self.surface, self.pos)
            self.drawElements(screen)

    def checkElementsClick(self, pos):
        for element in self.elements:
            if element.checkClick(pos):
                return Object.createNew(element.objectType, element.objectSprite)

        return None

    def checkClick(self, pos):
        self.updateRect()
        if self.visible:
            if self.rect.collidepoint(pos):
                self.selectedObject = self.checkElementsClick(pos)
                return True

        return False

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

    def zoomBy(self, zoom):
        self.zoom += zoom

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