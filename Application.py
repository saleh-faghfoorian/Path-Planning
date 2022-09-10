from Algorithms.RRT_Star.RRTStarSolution import RRTStarSolution
from Graphics.ObstaclesFrame import ObstaclesFrame
from Graphics.PointsFrame import PointsFrame
from Graphics.ShowSolutionFrame import SolutionFrame
from Algorithms.Dijkstra.DijkstraSolution import DijkstraSolution
from Algorithms.RRT.RRTSolution import RRTSolution
import pygame
import time


def writeAnswers(X, Y):
    answers = open("answers.txt", "w+")
    [answers.write(str(round((X[i] - 250)/100, 4)) + "," + str(round((Y[i] - 250)/100, 4)) + "\n") for i in range(len(X))]
    answers.close()

    # length = sum(1 for line in open("answers.txt")
    # listOfPoints = []
    trajectory = open("answers.txt", "r+")
    # for i in range(length):
    #     string = trajectory.readline().split(",")
    #     listOfPoints.append([float(string[0]), float(string[1])])
    # trajectory.close()
    # print(listOfPoints)


if __name__ == '__main__':
    flag = True
    changeMode = 0
    while True:
        if flag:
            obstacleFrame = ObstaclesFrame()
            obstacleFrame.show()
            obstacles = obstacleFrame.getObstacles()

            if obstacleFrame.readFileMode:
                boundary = obstacleFrame.boundary
            else:
                boundary = [10, 1180, 130, 720]

            pygame.event.clear()
            time.sleep(1)

            pointsFrame = PointsFrame(obstacleFrame.obstacles, boundary)
            pointsFrame.show()
            points = pointsFrame.getPoints()

        trajectoryX = []
        trajectoryY = []
        calculationTime = 0

        if pointsFrame.solutionMode == 1 or changeMode == 1:
            dijkstra = DijkstraSolution(obstacles, points, boundary)
            startTime = time.time()
            dijkstra.solve()
            trajectoryX, trajectoryY = dijkstra.getPath()
            calculationTime = dijkstra.getCalculationTime()
        elif pointsFrame.solutionMode == 2 or changeMode == 2:
            rrt = RRTSolution(obstacles, points, boundary)
            rrt.solve()
            trajectoryX, trajectoryY = rrt.getPath()
            calculationTime = rrt.getCalculationTime()
        elif pointsFrame.solutionMode == 3 or changeMode == 3:
            rrt = RRTStarSolution(obstacles, points, boundary)
            rrt.solve()
            trajectoryX, trajectoryY = rrt.getPath()
            calculationTime = rrt.getCalculationTime()

        pointsFrame.solutionMode = 0

        solutionFrame = SolutionFrame(boundary)
        solutionFrame.show(obstacleFrame.obstacles, pointsFrame.points, trajectoryX, trajectoryY, calculationTime)

        for i in range(len(trajectoryX)):
            trajectoryY[i] = 720 - trajectoryY[i]
            trajectoryX[i] = trajectoryX[i] - 10
        writeAnswers(trajectoryX, trajectoryY)

        flag = solutionFrame.resetKey
        changeMode = solutionFrame.solutionMode
        if solutionFrame.finishKey:
            break
