from random import randrange
import time
from Algorithms.Dijkstra.Graph import Node, Point, dist, generateInternalPoints

Max_Step_Size = 50
nodeNumbers = 1200
robotSize = 15

class RRTStarSolution:
    def __init__(self, obstacles, points, boundary):
        self.newTrajectoryX = []
        self.newTrajectoryY = []
        self.calculationTime = None
        self.obstacles = obstacles
        self.points = points
        self.trajectoryX = []
        self.trajectoryY = []
        self.boundary = boundary

    def solve(self):
        startTime = time.time()
        for k in range(len(self.points) - 1):
            self.points[k].setParent(0)
            startNode = self.points[k]
            goalNode = self.points[k + 1]
            nodes = [startNode]
            for i in range(nodeNumbers):
                if abs(nodes[len(nodes) - 1].coord.x - goalNode.coord.x) < 5 and abs(
                        nodes[len(nodes) - 1].coord.y - goalNode.coord.y) < 5:
                    break
                A = generateRandomNode(nodes, self.obstacles, self.boundary)
                newNode = A[0]
                nearNode = A[1]
                newNode.setCost(dist(newNode, nearNode) + float(nearNode.cost))
                r = 30
                q_nearest = []
                for j in range(len(nodes)):
                    if dist(nodes[j], newNode) <= r:
                        q_nearest.append(nodes[j])

                q_min = nearNode
                for j in range(len(nodes)):
                    if nodes[j].coord.x == q_min.coord.x and nodes[j].coord.y == q_min.coord.y:
                        newNode.setParent(j)
                nodes.append(newNode)
            D = []
            [D.append(dist(node, goalNode)) for node in nodes]

            minIndex = D.index(min(D))
            goalNode.setParent(minIndex)
            q_end = goalNode
            nodes.append(goalNode)
            trajectory = []

            while not (q_end.parent == 0):
                start = q_end.parent
                trajectory.append(q_end.coord)
                q_end = nodes[start]
            trajectory.append(startNode.coord)
            if len(nodes) == 2:
                xGenerated = [startNode.coord.x, goalNode.coord.x]
                yGenerated = [startNode.coord.y, goalNode.coord.y]
            else:
                xGenerated = [q.x for q in trajectory]
                yGenerated = [q.y for q in trajectory]
            nodes.clear()

            xGenerated = xGenerated[::-1]
            yGenerated = yGenerated[::-1]
            self.newTrajectoryX.append(xGenerated[0])
            self.newTrajectoryY.append(yGenerated[0])
            i = 0
            flag = True
            while i < len(xGenerated) and flag:
                for j in range(len(xGenerated) - 1, i, -1):
                    if not collisionCheck(Node(Point(xGenerated[j], yGenerated[j]), 0),
                                          Node(Point(xGenerated[i], yGenerated[i]), 0), self.obstacles):
                        self.newTrajectoryX.append(xGenerated[j])
                        self.newTrajectoryY.append(yGenerated[j])
                        i = j - 1
                        if j == len(xGenerated) - 1:
                            flag = False
                        break
                i = i + 1

        self.calculationTime = 1000 * (time.time() - startTime)

    def getPath(self):
        return self.newTrajectoryX, self.newTrajectoryY

    def getCalculationTime(self):
        return self.calculationTime


def generateRandomNode(nodes, obstacles, boundary):
    xMin = boundary[0]
    xMax = boundary[1]
    yMin = boundary[2]
    yMax = boundary[3]
    counter = 0
    while True:
        randomNode = Node(Point(randrange(xMin + robotSize, xMax - robotSize), randrange(yMin + robotSize, yMax - robotSize)), 0)
        node_distance = []
        [node_distance.append(dist(node, randomNode)) for node in nodes]
        value = min(node_distance)
        nearNode = nodes[node_distance.index(value)]
        newNode = Node(steer(randomNode, nearNode, value, Max_Step_Size), 0)
        if not collisionCheck(nearNode, newNode, obstacles):
            break
        counter = counter + 1

    return [newNode, nearNode]


def collisionCheck(startNode, goalNode, obstacles):
    internalPoints = generateInternalPoints(startNode, goalNode)
    flag = False
    for innerPoint in internalPoints:
        for obstacle in obstacles:
            if obstacle.isInBox(innerPoint):
                flag = True
                break
        if flag:
            break
    return flag


def steer(qr, qn, val, eps):
    if val > eps:
        newNode = Point(qn.coord.x + (qr.coord.x - qn.coord.x) * eps / val,
                        qn.coord.y + (qr.coord.y - qn.coord.y) * eps / val)
    else:
        newNode = Point(qr.coord.x, qr.coord.y)
    return newNode
