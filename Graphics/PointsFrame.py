import pygame

from Algorithms.Dijkstra.Graph import Node, Point
from Graphics.GraphicTemplate import GraphicTemplate


class PointsFrame(GraphicTemplate):
    def __init__(self, obstacles, boundary):
        super().__init__()
        self.readFileMode = False
        self.dijkstraButtonText = self.font.render('Dijkstra', True, self.blue)
        self.RRTButtonText = self.font.render('RRT', True, self.blue)
        self.RRTStarButtonText = self.font.render('RRT Star', True, self.blue)
        self.obstacles = obstacles
        self.solutionMode = None
        self.boundary = boundary

    def show(self):

        flag = True
        while flag:
            text = self.font.render('Create Points', True, self.green)
            textContour = pygame.Rect(self.width // 2 - self.textWidth // 2, 20, self.textWidth, self.textHeight)
            dijkstraButtonContour = pygame.Rect(self.width - 2 * self.buttonWidth - 2 * self.mapOffset,
                                                self.height - self.buttonHeight - self.mapOffset, self.buttonWidth,
                                                self.buttonHeight)
            rrtButtonContour = pygame.Rect(self.width - 3 * self.buttonWidth - 3 * self.mapOffset,
                                           self.height - self.buttonHeight - self.mapOffset, self.buttonWidth,
                                           self.buttonHeight)
            rrtStarButtonContour = pygame.Rect(self.width - 4 * self.buttonWidth - 4 * self.mapOffset,
                                               self.height - self.buttonHeight - self.mapOffset, self.buttonWidth,
                                               self.buttonHeight)
            mapBorder = pygame.Rect(self.mapOffset, 3 * self.mapOffset + self.textHeight,
                                    self.width - 2 * self.mapOffset,
                                    self.height - 5 * self.mapOffset - self.textHeight - self.buttonHeight)

            textRect = text.get_rect()
            textRect.center = (self.width // 2, self.textHeight // 2 + 15)
            dijkstraButtonTextRect = self.dijkstraButtonText.get_rect()
            rrtButtonTextRect = self.RRTButtonText.get_rect()
            rrtStarButtonTextRect = self.RRTStarButtonText.get_rect()
            dijkstraButtonTextRect.center = (self.width - int(1.5 * self.buttonWidth) - 2 * self.mapOffset,
                                             self.height - self.buttonHeight // 2 - self.mapOffset)
            rrtButtonTextRect.center = (self.width - int(2.5 * self.buttonWidth) - 3 * self.mapOffset,
                                        self.height - self.buttonHeight // 2 - self.mapOffset)
            rrtStarButtonTextRect.center = (self.width - int(3.5 * self.buttonWidth) - 4 * self.mapOffset,
                                            self.height - self.buttonHeight // 2 - self.mapOffset)
            boundary = pygame.Rect(self.boundary[0],
                                   self.height - 2 * self.mapOffset - self.buttonHeight - self.boundary[3] +
                                   self.boundary[2], self.boundary[1] - self.boundary[0] + self.mapOffset,
                                   self.boundary[3] - self.boundary[2])

            counter = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if dijkstraButtonContour.x < pygame.mouse.get_pos()[
                        0] < dijkstraButtonContour.x + dijkstraButtonContour.width and dijkstraButtonContour.y < \
                            pygame.mouse.get_pos()[1] < dijkstraButtonContour.y + dijkstraButtonContour.height:
                        self.solutionMode = 1
                        flag = False
                        break
                    elif rrtButtonContour.x < pygame.mouse.get_pos()[
                        0] < rrtButtonContour.x + rrtButtonContour.width and rrtButtonContour.y < \
                            pygame.mouse.get_pos()[1] < rrtButtonContour.y + rrtButtonContour.height:
                        self.solutionMode = 2
                        flag = False
                        break
                    elif self.readFilesButtonContour.x < pygame.mouse.get_pos()[
                        0] < self.readFilesButtonContour.x + self.readFilesButtonContour.width and self.readFilesButtonContour.y < \
                            pygame.mouse.get_pos()[
                                1] < self.readFilesButtonContour.y + self.readFilesButtonContour.height:
                        self.getPointsFromFile()
                        break
                    elif rrtStarButtonContour.x < pygame.mouse.get_pos()[
                        0] < rrtStarButtonContour.x + rrtStarButtonContour.width and rrtStarButtonContour.y < \
                            pygame.mouse.get_pos()[
                                1] < rrtStarButtonContour.y + rrtStarButtonContour.height:
                        self.solutionMode = 3
                        flag = False
                        break
                    elif mapBorder.x < pygame.mouse.get_pos()[0] < mapBorder.x + mapBorder.width and mapBorder.y < \
                            pygame.mouse.get_pos()[1] < mapBorder.y + self.mapBorder.height:
                        self.points.append(pygame.mouse.get_pos())

            for obs in self.obstacles:
                pygame.draw.rect(self.display, self.color, obs)
            for point in self.points:
                pygame.draw.circle(self.display, self.red, point, 3)
            for j in range((self.width - 2 * self.mapOffset) // self.gridLength):
                pygame.draw.line(self.display, self.gray,
                                 (self.mapOffset + (j + 1) * self.gridLength, 3 * self.mapOffset + self.textHeight),
                                 (self.mapOffset + (j + 1) * self.gridLength,
                                  self.height - 2 * self.mapOffset - self.buttonHeight), 1)
            for j in range((self.height - 5 * self.mapOffset - self.textHeight - self.buttonHeight) // self.gridLength):
                pygame.draw.line(self.display, self.gray,
                                 (self.mapOffset, 3 * self.mapOffset + self.textHeight + (j + 1) * self.gridLength),
                                 (self.width - self.mapOffset,
                                  3 * self.mapOffset + self.textHeight + (j + 1) * self.gridLength), 1)
            pygame.draw.rect(self.display, self.color, boundary, 2)
            pygame.draw.rect(self.display, self.color, textContour, 2)
            pygame.draw.rect(self.display, self.color, dijkstraButtonContour)
            pygame.draw.rect(self.display, self.color, self.readFilesButtonContour)
            pygame.draw.rect(self.display, self.color, rrtButtonContour)
            pygame.draw.rect(self.display, self.color, rrtStarButtonContour)
            pygame.draw.rect(self.display, self.blue, mapBorder, 1)
            self.display.blit(text, textRect)
            self.display.blit(self.scaleImage, (100, 30))
            self.display.blit(self.dijkstraButtonText, dijkstraButtonTextRect)
            self.display.blit(self.readFilesText, self.readFilesTextRect)
            self.display.blit(self.RRTButtonText, rrtButtonTextRect)
            self.display.blit(self.RRTStarButtonText, rrtStarButtonTextRect)
            pygame.display.update()

    def getPoints(self):
        nodes = []
        [nodes.append(Node(Point(point[0], point[1]), 0)) for point in self.points]
        return nodes

    def getPointsFromFile(self):
        nodes = []
        self.points = []
        numberOfPoints = sum(1 for line in open('points.txt'))
        pointsFile = open("points.txt", "r+")
        for j in range(numberOfPoints):
            data = pointsFile.readline().split(" ")
            x = int(data[0])
            y = int(data[1])
            self.points.append((x + self.mapOffset, self.height - 2 * self.mapOffset - self.buttonHeight - y))
            nodes.append(Node(Point(x + self.mapOffset, self.height - 2 * self.mapOffset - self.buttonHeight - y), 0))
        pointsFile.close()
        return nodes
