import time

from Algorithms.Dijkstra.Graph import generateInternalPoints, Node, Point
from Graphics.GraphicTemplate import GraphicTemplate
import pygame

class AnimationFrame(GraphicTemplate):
    def __init__(self, obstacles, trajectoryX, trajectoryY):
        super().__init__()
        self.obstacles = obstacles
        self.trajectoryX = trajectoryX
        self.trajectoryY = trajectoryY

    def animate(self):
        for i in range(len(self.trajectoryX) - 1):
            innerPoints = generateInternalPoints(Node(Point(self.trajectoryX[i], self.trajectoryY[i]), 0), Node(Point(self.trajectoryX[i+1], self.trajectoryY[i+1]), 0))
            for innerPoint in innerPoints:
                pygame.draw.circle(self.display, self.red, (innerPoint.coord.x, innerPoint.coord.y), 15, 2)
                for ob in self.obstacles:
                    pygame.draw.rect(self.display, self.color, ob)
                pygame.draw.rect(self.display, self.blue, self.mapBorder, 1)
                self.display.blit(self.text, self.textRect)
                self.display.blit(self.scaleImage, (60, 30))
                pygame.draw.rect(self.display, self.color, self.textContour, 2)
                pygame.draw.rect(self.display, self.blue, self.mapBorder, 1)
                pygame.display.update()
                time.sleep(0.01)
                


        flag = True
        resetButtonText = self.font.render('Reset', True, self.blue)
        self.buttonText = self.font.render('Finish', True, self.blue)
        self.text = self.font.render('Trajectory', True, self.green)
        while flag:
            self.textContour = pygame.Rect(self.width // 2 - self.textWidth // 2, 20, self.textWidth, self.textHeight)
            timeTextContour = pygame.Rect(self.width // 2 + 20 + self.textWidth // 1.85, 20, 410, 40)
            lengthTextContour = pygame.Rect(self.width // 2 + 20 + self.textWidth // 1.85, 80, 410, 40)
            self.buttonContour = pygame.Rect(self.width - self.buttonWidth - self.mapOffset,
                                             self.height - self.buttonHeight - self.mapOffset, self.buttonWidth,
                                             self.buttonHeight)
            animationButtonContour = pygame.Rect(2 * self.mapOffset + self.buttonWidth,
                                                 self.height - self.buttonHeight - self.mapOffset, self.buttonWidth,
                                                 self.buttonHeight)
            dijkstraButtonContour = pygame.Rect(self.width - 2 * self.buttonWidth - 2 * self.mapOffset,
                                                self.height - self.buttonHeight - self.mapOffset, self.buttonWidth,
                                                self.buttonHeight)
            rrtButtonContour = pygame.Rect(self.width - 3 * self.buttonWidth - 3 * self.mapOffset,
                                           self.height - self.buttonHeight - self.mapOffset, self.buttonWidth,
                                           self.buttonHeight)
            resetButtonContour = pygame.Rect(self.mapOffset, self.height - self.buttonHeight - self.mapOffset,
                                             self.buttonWidth,
                                             self.buttonHeight)
            self.mapBorder = pygame.Rect(self.mapOffset, 3 * self.mapOffset + self.textHeight,
                                         self.width - 2 * self.mapOffset,
                                         self.height - 5 * self.mapOffset - self.textHeight - self.buttonHeight)

            self.textRect = self.text.get_rect()
            self.textRect.center = (self.width // 2, self.textHeight // 2 + 15)
            self.buttonTextRect = self.buttonText.get_rect()
            self.buttonTextRect.center = (
                self.width - self.buttonWidth // 2 - self.mapOffset,
                self.height - self.buttonHeight // 2 - self.mapOffset)
            dijkstraButtonTextRect = self.dijkstraButtonText.get_rect()
            animationButtonTextRect = self.animationButtonText.get_rect()
            rrtButtonTextRect = self.RRTButtonText.get_rect()
            resetButtonTextRect = resetButtonText.get_rect()
            dijkstraButtonTextRect.center = (self.width - int(1.5 * self.buttonWidth) - 2 * self.mapOffset,
                                             self.height - self.buttonHeight // 2 - self.mapOffset)
            rrtButtonTextRect.center = (self.width - int(2.5 * self.buttonWidth) - 3 * self.mapOffset,
                                        self.height - self.buttonHeight // 2 - self.mapOffset)
            resetButtonTextRect.center = (self.mapOffset + self.buttonWidth // 2,
                                          self.height - self.buttonHeight // 2 - self.mapOffset)
            animationButtonTextRect.center = (
            self.mapOffset + self.buttonWidth // 2, self.height - self.buttonHeight // 2 - self.mapOffset)
            counter = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.buttonContour.x < pygame.mouse.get_pos()[
                        0] < self.buttonContour.x + self.buttonContour.width and self.buttonContour.y < \
                            pygame.mouse.get_pos()[1] < self.buttonContour.y + self.buttonContour.height:
                        self.finishKey = True
                        flag = False
                        break
                    elif dijkstraButtonContour.x < pygame.mouse.get_pos()[
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
                    elif resetButtonContour.x < pygame.mouse.get_pos()[
                        0] < resetButtonContour.x + resetButtonContour.width and resetButtonContour.y < \
                            pygame.mouse.get_pos()[1] < resetButtonContour.y + resetButtonContour.height:
                        self.resetKey = True
                        flag = False
                        break
                    elif animationButtonContour.x < pygame.mouse.get_pos()[
                        0] < animationButtonContour.x + animationButtonContour.width and animationButtonContour.y < \
                            pygame.mouse.get_pos()[1] < animationButtonContour.y + animationButtonContour.height:
                        self.animationMode = True
                        flag = False
                        break

            for ob in self.obstacles:
                pygame.draw.rect(self.display, self.color, ob)
            for point in self.points:
                pygame.draw.circle(self.display, self.red, point, 5)
            for i in range(len(self.trajectoryX) - 1):
                pygame.draw.line(self.display, self.red, (self.trajectoryX[i], self.trajectoryY[i]),
                                 (self.trajectoryX[i + 1], self.trajectoryY[i + 1]), 3)

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
            pygame.draw.rect(self.display, self.color, timeTextContour, 2)
            pygame.draw.rect(self.display, self.color, lengthTextContour, 2)
            pygame.draw.rect(self.display, self.color, resetButtonContour)
            pygame.draw.rect(self.display, self.color, dijkstraButtonContour)
            pygame.draw.rect(self.display, self.color, rrtButtonContour)
            pygame.draw.rect(self.display, self.blue, self.mapBorder, 1)
            self.display.blit(self.text, self.textRect)
            self.display.blit(self.scaleImage, (60, 30))
            self.display.blit(self.buttonText, self.buttonTextRect)
            self.display.blit(resetButtonText, resetButtonTextRect)
            self.display.blit(self.dijkstraButtonText, dijkstraButtonTextRect)
            self.display.blit(self.RRTButtonText, rrtButtonTextRect)
            pygame.display.update()

