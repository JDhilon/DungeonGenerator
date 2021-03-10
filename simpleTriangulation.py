import numpy as np
import math
import simpleGraph
import itertools
import random

# Helper function to find 2d distance
def dist(a, b):
    return math.sqrt(((a[0] - b[0]) * (a[0] - b[0])) + ((a[1] - b[1]) * (a[1] - b[1])))

# Divide points into sets of up to 3, then merge them 
# TODO: Make this work with a graph, and add in edges as needed
def dividePoints(points, graph):
    if len(points) <= 1:
        # Should not happen, but it means we have 0 or 1 rooms
        return 0    
    elif len(points) == 3:
        a = points[0]
        b = points[1]
        c = points[2]
        graph.setEdge(a[0], b[0], dist(a[1], b[1]))
        graph.setEdge(a[0], c[0], dist(a[1], c[1]))
        graph.setEdge(b[0], c[0], dist(b[1], c[1]))
        return points
    elif len(points) == 2:
        a = points[0]
        b = points[1]
        graph.setEdge(a[0], b[0], dist(a[1], b[1]))
        return points
    else:
        # Split functionality from https://stackoverflow.com/a/47704499
        mid = math.floor(len(points)/2)
        a = points[:mid]
        b = points[mid:]
        pointsA = dividePoints(a, graph)
        pointsB = dividePoints(b, graph)
        return mergePoints(pointsA, pointsB, graph)

def mergePoints(pointsA, pointsB, graph):
    # Select a point in A and connect it to a point in B, then merge the 2 sets
    a = random.randint(0, len(pointsA) - 1)
    b = random.randint(0, len(pointsB) - 1)
    graph.setEdge(pointsA[a][0], pointsB[b][0], dist(pointsA[a][1], pointsB[b][1]))
    return pointsA + pointsB


def main():
    # For tests
    # Room ID, Mid Point
    t = [
        [0, [6, 2]],
        [1, [1, 3]],
        [2, [5, 7]],
        [3, [1, 2]],
        [4, [5, 2]],
        [5, [7, 4]],
        [6, [1, 5]],
        [7, [8, 1]]
    ]
    # Sort by second element
    t.sort(key = lambda x: x[1])

    g = simpleGraph.Graph(len(t))
    dividePoints(t, g)
    g.printMatrix()
    g.primMST()

    # Previous, dict based implementation
    # testPoints = {
    #     0: [6, 2],
    #     1: [1, 3],
    #     2: [5, 7],
    #     3: [1, 2],
    #     4: [5, 2],
    #     5: [7, 4],
    #     6: [1, 5],
    #     7: [8, 1]
    # }

    # tmp = sorted(testPoints.items(), key=lambda item: item[1])
    # sortedPoints = {
    #         k: v for k, v in tmp
    #     }

if __name__ == "__main__":
    main()