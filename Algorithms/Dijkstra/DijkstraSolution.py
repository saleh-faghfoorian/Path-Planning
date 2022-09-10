import heapq
from Algorithms.Dijkstra.Graph import Graph
import time


class DijkstraSolution:
    def __init__(self, obstacles, nodes, boundary):
        self.calculationTime = None
        self.nodes = nodes
        self.newObstacles = obstacles
        self.trajectoryX = []
        self.trajectoryY = []
        self.boundary = boundary

    def  solve(self):
        startTime = time.time()
        counter = 0
        for i in range(len(self.nodes) - 1):
            startTime = time.time()
            graph = Graph(self.boundary)
            graph.create(self.newObstacles, self.nodes[i], self.nodes[i + 1])
            # print("declaration : " + str(time.time() - startTime))
            # startTime = time.time()
            dijkstra(graph, graph.get_vertex('0'), graph.get_vertex('1'))
            target = graph.get_vertex('1')
            path = [target.get_id()]
            shortest(target, path)
            # print(f'Solution : {time.time() - startTime}')
            path = path[::-1]
            for j in range(len(path)):
                if path[j] == '0':
                    xGenerated = self.nodes[counter].coord.x
                    yGenerated = self.nodes[counter].coord.y
                elif path[j] == '1':
                    xGenerated = self.nodes[counter + 1].coord.x
                    yGenerated = self.nodes[counter + 1].coord.y
                else:
                    xGenerated = graph.nodes[int(path[j])].coord.x
                    yGenerated = graph.nodes[int(path[j])].coord.y
                self.trajectoryX.append(xGenerated)
                self.trajectoryY.append(yGenerated)
            counter = counter + 1

        self.calculationTime = 1000 * (time.time() - startTime)

    def getPath(self):
        return self.trajectoryX, self.trajectoryY

    def getCalculationTime(self):
        return self.calculationTime


def dijkstra(aGraph, start, target):
    start.set_distance(0)
    unvisited_queue = [(ver.distance, ver) for ver in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        for next in current.adjacent:
            if next.visited:
                continue
            new_dist = current.distance + current.get_weight(next)

            if new_dist < next.distance:
                next.set_distance(new_dist)
                next.set_previous(current)

        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        unvisited_queue = [(v.distance, v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)


def shortest(v, path):
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return
