import pygame

from Graphics.GraphicTemplate import GraphicTemplate, Box


class ObstaclesFrame(GraphicTemplate):
    def __init__(self):
        self.boundary = []
        self.readFileMode = False
        self.firstCorners = []
        self.secondCorners = []
        super().__init__()

    def show(self):
        flag = True
        while flag:
            counter = 0
            for event in pygame.event.get():
                firstCorner = None
                secondCorner = None
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttonContour.x < pygame.mouse.get_pos()[
                        0] < self.buttonContour.x + self.buttonContour.width and self.buttonContour.y < \
                            pygame.mouse.get_pos()[1] < self.buttonContour.y + self.buttonContour.height:
                        flag = False
                        break
                    elif self.readFilesButtonContour.x < pygame.mouse.get_pos()[
                        0] < self.readFilesButtonContour.x + self.readFilesButtonContour.width and self.readFilesButtonContour.y < \
                            pygame.mouse.get_pos()[
                                1] < self.readFilesButtonContour.y + self.readFilesButtonContour.height:
                        flag = False
                        self.readFileMode = True
                        break
                    else:
                        self.firstCorners.append(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONUP:
                    self.secondCorners.append(pygame.mouse.get_pos())
                    counter = counter + 1
                if len(self.secondCorners) > 10:
                    break

            if counter > 0:
                x = self.firstCorners[len(self.firstCorners) - 1][0]
                y = self.firstCorners[len(self.firstCorners) - 1][1]
                obstacleWidth = self.secondCorners[len(self.secondCorners) - 1][0] - x
                obstacleHeight = self.secondCorners[len(self.secondCorners) - 1][1] - y
                self.obstacles.append(pygame.Rect(x, y, obstacleWidth, obstacleHeight))

            for obs in self.obstacles:
                pygame.draw.rect(self.display, self.color, obs)
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

            pygame.draw.rect(self.display, self.color, self.textContour, 2)
            pygame.draw.rect(self.display, self.color, self.buttonContour)
            pygame.draw.rect(self.display, self.blue, self.mapBorder, 1)
            pygame.draw.rect(self.display, self.color, self.readFilesButtonContour)
            self.display.blit(self.scaleImage, (100, 30))
            self.display.blit(self.text, self.textRect)
            self.display.blit(self.buttonText, self.buttonTextRect)
            self.display.blit(self.readFilesText, self.readFilesTextRect)
            pygame.display.update()
        if self.readFileMode:
            self.getObstaclesFromFile()

    def getObstacles(self):
        newObstacles = []
        [newObstacles.append(Box(obstacle[0], obstacle[1], obstacle[2] + obstacle[0], obstacle[3] + obstacle[1])) for
         obstacle
         in self.obstacles]
        return newObstacles

    def getObstaclesFromFile(self):
        self.obstacles = []
        newObstacles = []
        numberOfObstacles = sum(1 for line in open('obstacles.txt'))
        obstaclesFile = open("obstacles.txt", "r+")
        for j in range(numberOfObstacles - 1):
            data = obstaclesFile.readline().split(" ")
            x0 = int(data[0])
            y0 = int(data[1])
            x1 = int(data[2])
            y1 = int(data[3])
            newObstacles.append(Box(x0 + self.mapOffset, self.height - 2 * self.mapOffset - self.buttonHeight - y0, x1 + self.mapOffset, self.height - 2 * self.mapOffset - self.buttonHeight - y1))
            self.obstacles.append(pygame.Rect(x0 + self.mapOffset, self.height - 2 * self.mapOffset - self.buttonHeight - y1, x1 - x0, y1 - y0))
        boundary = obstaclesFile.readline().split(" ")
        obstaclesFile.close()
        xMin = int(boundary[0]) + self.mapOffset
        xMax = int(boundary[1]) + self.mapOffset
        yMin = self.height - 2 * self.mapOffset - self.buttonHeight - int(boundary[3])
        yMax = self.height - 2 * self.mapOffset - self.buttonHeight - int(boundary[2])
        self.boundary = [xMin, xMax, yMin, yMax]
        return newObstacles
