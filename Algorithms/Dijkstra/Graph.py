import math
import time
from Graphics.GraphicTemplate import Box


class Graph:
    def __init__(self, boundary):
        self.nodes = None
        self.vert_dict = {}
        self.num_vertices = 0
        self.xMin = boundary[0]
        self.xMax = boundary[1]
        self.yMin = boundary[2]
        self.yMax = boundary[3]

    def create(self, obstacles, startNode, goalNode):
        # startNode.coord.y = 720 - startNode.coord.y
        # goalNode.coord.y = 720 - goalNode.coord.y
        self.nodes = [startNode, goalNode]
        self.add_vertex('0')
        self.add_vertex('1')
        id = 2
        for obstacle in obstacles:
            if obstacle.x0 > self.xMin and obstacle.y0 > self.yMin:
                self.nodes.append(Node(Point(obstacle.x0, obstacle.y0), 0))
                self.add_vertex(id)
                id = id + 1
            if obstacle.x0 > self.xMin and obstacle.y1 < self.yMax:
                self.nodes.append(Node(Point(obstacle.x0, obstacle.y1), 0))
                self.add_vertex(id)
                id = id + 1
            if obstacle.x1 < self.xMax and obstacle.y0 > self.yMin:
                self.nodes.append(Node(Point(obstacle.x1, obstacle.y0), 0))
                self.add_vertex(id)
                id = id + 1
            if obstacle.x1 < self.xMax and obstacle.y1 < self.yMax:
                self.nodes.append(Node(Point(obstacle.x1, obstacle.y1), 0))
                self.add_vertex(id)
                id = id + 1
        # print(id - 2)
        # startTime = time.time()
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):

                innerPoints = generateInternalPoints(self.nodes[i], self.nodes[j])
                flag = True
                for k in range(len(innerPoints)):
                    for obstacle in obstacles:
                        if obstacle.isInBox(innerPoints[k]):
                            flag = False
                            break
                    if not flag:
                        break
                if flag:
                    distance = dist(self.nodes[i], self.nodes[j])
                    self.add_edge(str(i), str(j), distance)

                # q1 = self.nodes[i]
                # q2 = self.nodes[j]
                # x1 = self.nodes[i].coord.x
                # y1 = self.nodes[i].coord.y
                # x2 = self.nodes[j].coord.x
                # y2 = self.nodes[j].coord.y
                # for obstacle in obstacles:
                #     flag = True
                #     print(f'obstacle : x0 = {obstacle.x0}, x1 = {obstacle.x1}, y0 = {obstacle.y0}, y1 = {obstacle.y1}')
                #     print(f'q1 : ({x1},{y1})')
                #     print(f'q2 : ({x2},{y2})')
                #     if x1 == x2:
                #         if obstacle.x0 < x1 < obstacle.x1 and (
                #                 (y1 < obstacle.y0 and y2 > obstacle.y1) or (
                #                 y2 < obstacle.y0 and y1 > obstacle.y1)):
                #             flag = False
                #             break
                #     elif y1 == y2:
                #         if obstacle.y0 < y1 < obstacle.y1 and (
                #                 (x1 < obstacle.x0 and x2 > obstacle.x1) or (
                #                 x2 < obstacle.x0 and x1 > obstacle.x1)):
                #             flag = False
                #             break
                #     else:
                #         slope = (y1 - y2) / (x1 - x2)
                #         b = y2 - slope*x2
                #         print(f'slope : {slope}, b : {b}')
                #         line = lambda x: slope * x + b
                #         print(f'Left : {obstacle.y0 + 1 < line(obstacle.x0) < obstacle.y1 - 1}')
                #         print(f'Left intersection : {line(obstacle.x0)}')
                #         print(f'Right : {obstacle.y0 + 1 < line(obstacle.x1) < obstacle.y1 - 1}')
                #         print(f'Right intersection : {line(obstacle.x1)}')
                #         print(f'Down : {obstacle.x0 + 1 < (obstacle.y1 - b) / slope < obstacle.x1 - 1}')
                #         print(f'Down intersection : {(obstacle.y1 - b) / slope}')
                #         print(f'Up : {obstacle.x0 + 1 < (obstacle.y0 - b) / slope < obstacle.x1 - 1}')
                #         print(f'Up intersection : {(obstacle.y0 - b) / slope}')
                #         if obstacle.y0 + 1 < line(obstacle.x0) < obstacle.y1 - 1 or \
                #                 obstacle.y0 + 1 < line(obstacle.x1) < obstacle.y1 - 1 or \
                #                 obstacle.x0 + 1 < (obstacle.y0 - b) / slope < obstacle.x1 - 1 or \
                #                 obstacle.x0 + 1 < (obstacle.y1 - b) / slope < obstacle.x1 - 1:
                #             flag = False
                # if flag:
                #     distance = dist(q1, q2)
                #     self.add_edge(str(i), str(j), distance)

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, id):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(id)
        self.vert_dict[id] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous


class Vertex:
    def __init__(self, id):
        self.id = id
        self.adjacent = {}
        self.distance = 10000000
        self.visited = False
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def __lt__(self, other):
        return self.distance < other.distance


def generateInternalPoints(q_near, q_new):
    L = dist(q_near, q_new)
    if L < 50:
        n = 30
    elif L < 100:
        n = 40
    elif L < 200:
        n = 50
    elif L < 300:
        n = 60
    else:
        n = 100
    l = L / (n + 1)
    if q_near.coord.x == q_new.coord.x:
        theta = math.pi / 2
    else:
        theta = math.atan((q_near.coord.y - q_new.coord.y) / (q_near.coord.x - q_new.coord.x))
    if q_near.coord.x > q_new.coord.x:
        q_temp = q_new
        q_new = q_near
        q_near = q_temp
    innerPoints = [q_near, q_new]
    [innerPoints.append(
        Node(Point(q_near.coord.x + i * l * math.cos(theta), q_near.coord.y + i * l * math.sin(theta)), 0)) for i in
        range(n)]
    return innerPoints


def dist(q1, q2):
    return math.sqrt((float(q1.coord.x) - float(q2.coord.x)) ** 2 + (float(q1.coord.y) - float(q2.coord.y)) ** 2)


class Node:
    def __init__(self, coord, cost):
        self.parent = None
        self.coord = coord
        self.cost = cost

    def setParent(self, parent):
        self.parent = parent

    def setCost(self, cost):
        self.cost = cost


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
