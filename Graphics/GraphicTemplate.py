import pygame


class GraphicTemplate:

    def __init__(self):
        pygame.init()
        self.width = 1200
        self.height = 800

        self.display: pygame.Surface = pygame.display.set_mode(
            size=(self.width, self.height),
            flags=pygame.SCALED | pygame.SRCALPHA,
            depth=0,
            display=0,
            vsync=1)

        self.obstacles = []
        self.points = []

        self.color = pygame.Color('lightskyblue3')
        self.font = pygame.font.Font('times.ttf', 36)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)
        self.gray = (192, 192, 192)
        self.buttonText = self.font.render('Next', True, self.blue)
        self.textWidth = 300
        self.textHeight = 100
        self.buttonWidth = 150
        self.buttonHeight = 60
        self.mapOffset = 10
        self.gridLength = (self.height - 5 * self.mapOffset - self.textHeight - self.buttonHeight) // 20
        self.scaleImage = pygame.image.load("scale.png")
        self.display.fill((255, 255, 255, 0))

        self.readFilesText = self.font.render('Import Data', True, self.blue)

        self.textContour = pygame.Rect(self.width // 2 - self.textWidth // 2, 20, self.textWidth, self.textHeight)
        self.buttonContour = pygame.Rect(self.width - self.buttonWidth - self.mapOffset,
                                         self.height - self.buttonHeight - self.mapOffset, self.buttonWidth,
                                         self.buttonHeight)
        self.readFilesButtonContour = pygame.Rect(self.width - 7 * self.buttonWidth - 2 * self.mapOffset,
                                                  self.height - self.buttonHeight - self.mapOffset, 2 * self.buttonWidth,
                                                  self.buttonHeight)
        self.mapBorder = pygame.Rect(self.mapOffset, 3 * self.mapOffset + self.textHeight,
                                     self.width - 2 * self.mapOffset,
                                     self.height - 5 * self.mapOffset - self.textHeight - self.buttonHeight)
        self.text = self.font.render('Create obstacles', True, self.green)
        self.textRect = self.text.get_rect()
        self.readFilesTextRect = self.readFilesText.get_rect()
        self.textRect.center = (self.width // 2, self.textHeight // 2 + 15)
        self.buttonTextRect = self.buttonText.get_rect()
        self.buttonTextRect.center = (
            self.width - self.buttonWidth // 2 - self.mapOffset, self.height - self.buttonHeight // 2 - self.mapOffset)
        self.readFilesTextRect.center = (self.width - 6 * self.buttonWidth - 2 * self.mapOffset,
                                                  self.height - int(0.5 * self.buttonHeight) - self.mapOffset)

class Box:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = min(x0, x1)
        self.x1 = max(x0, x1)
        self.y0 = min(y0, y1)
        self.y1 = max(y0, y1)

        self.robotSize = 15
        self.x0 = self.x0 - self.robotSize
        self.y0 = self.y0 - self.robotSize
        self.x1 = self.x1 + self.robotSize
        self.y1 = self.y1 + self.robotSize

    def getCorner(self):
        return self.x0 + self.robotSize, self.y0 + self.robotSize

    def getWidth(self):
        return self.x1 - self.x0 - 2 * self.robotSize

    def getHeight(self):
        return self.y1 - self.y0 - 2 * self.robotSize

    def isInBox(self, node):
        return self.x0 < node.coord.x < self.x1 and self.y0 < node.coord.y < self.y1
