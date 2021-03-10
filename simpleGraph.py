# A graph represented by adjacency matrix
from termcolor import colored

class Graph:

    # Initialize graph with a set number of vertices
    def __init__(self, vertexCount, directed=False):
        self.directed = directed
        self.vertexCount = vertexCount

        # Initialize adjacency matrix with all -1s (no edges)
        self.matrix = []
        for x in range(vertexCount):
            tmp = []
            for y in range(vertexCount):
                tmp.append(-1)
            self.matrix.append(tmp)

    def setEdge(self, a, b, cost=0):
        self.matrix[a][b] = cost
        if not self.directed:
            self.matrix[b][a] = cost

    def getEdges(self):
        edges = []
        for i in range (self.vertexCount):
            for j in range (self.vertexCount):
                if self.matrix[i][j] != -1:
                    edges.append((i, j, self.matrix[i][j]))
        return edges
        
    def getMatrix(self):
        return self.matrix

    # Print formatted matrix to 2 decimal places
    # TODO: Make this work with variable precision
    def printMatrix(self, precision=2):
        print('     ', end='')
        for x in range(self.vertexCount):
            print(x, end='     ')
        print()

        for x in range(self.vertexCount):
            print(x, end=' ')
            tmp = self.matrix[x]

            print('[', end='')
            for y in tmp:
                if y >= 0:
                    print(colored("{:+.2f}".format(y), 'green'), end=' ')
                else:
                    print("{:+.2f}".format(y), end=' ')
            print(']')

    # An internal function to find the min valued vertex not already in the MST
    def minVertex(self, weights, mst): 
        minVal = float('inf')
  
        for x in range(self.vertexCount): 
            if weights[x] < minVal and mst[x] == False: 
                minVal = weights[x] 
                minIndex = x 
  
        return minIndex
    
    # A utility function to print the constructed MST stored in mst 
    def printMST(self, mst): 
        print("Edge    Weight")
        for i in range(0, self.vertexCount): 
            # Handle root
            if mst[i] == -1:
                continue
            print(mst[i], "-", i, "   ", "{:.2f}".format(self.matrix[i][mst[i]]))

    # Returns a minimum spanning tree, using Prim's Algorithm
    # https://en.wikipedia.org/wiki/Prim%27s_algorithm 
    def primMST(self, start=0): 
        # TODO: Test edge cases and make sure that manually selecting start point works
        if start >= self.vertexCount:
            start = 0

        # Give all vertices except start infinite weight
        weights = [float('inf')] * self.vertexCount
        weights[start] = 0

        mst = [None] * self.vertexCount 
        mst[start] = -1 

        mstSet = [False] * self.vertexCount 
  
        for x in range(self.vertexCount): 
  
            # Pick the lowest cost vertex not yet in the MST 
            minVertex = self.minVertex(weights, mstSet) 
  
            # Add the lowest cost vertex in the MST
            mstSet[minVertex] = True
  
            # Update costs of the adjacent vertices if necessary
            for neighbour in range(self.vertexCount): 
                # if a vertex is adjacent to minVertex and it is not in the MST and the edge cost is less than it's current min cost, update it
                if self.matrix[minVertex][neighbour] > 0 and mstSet[neighbour] == False and weights[neighbour] > self.matrix[minVertex][neighbour]: 
                        weights[neighbour] = self.matrix[minVertex][neighbour] 
                        mst[neighbour] = minVertex 
  
        self.printMST(mst)
        return mst 

def main():
    # For tests
    graph = Graph(4)
    graph.matrix = [ 
            [9, 0, 6, 0], 
            [1, 3, 3, 8],  
            [4, 4, 7, 0], 
            [0, 7, 9, 0]] 
    graph.printMatrix()

    graph.primMST()

    graph2 = Graph(4, directed=True)
    graph2.setEdge(1, 3, 1)
    graph2.setEdge(3, 1, 2)

if __name__ == "__main__":
    main()