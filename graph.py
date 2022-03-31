import math
import random


def euclid(p, q):
    x = p[0] - q[0]
    y = p[1] - q[1]
    return math.sqrt(x * x + y * y)


class Graph:

    # Complete as described in the specification, taking care of two cases:
    # the -1 case, where we read points in the Euclidean plane, and
    # the n>0 case, where we read a general graph in a different format.
    # self.perm, self.dists, self.n are the key variables to be set up.
    def __init__(self, n, filename):
        coordinates = []
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                coordinates.append(line)
            for i in range(len(coordinates)):
                coordinates[i] = coordinates[i].removesuffix("\n")
                coordinates[i] = coordinates[i].split(' ')
                coordinates[i] = tuple([int(x) for x in coordinates[i] if x.isdigit()])
        f.close()
        if n == -1:
            self.n = len(coordinates)
            self.dists = [[None for x in range(len(coordinates))] for y in range(len(coordinates))]
            for i in range(len(coordinates)):
                for j in range(len(coordinates)):
                    if self.dists[i][j] is None:
                        self.dists[i][j] = (euclid(coordinates[i], coordinates[j]))
                        self.dists[j][i] = self.dists[i][j]
            self.perm = [i for i in range(self.n)]

        elif n > 0:
            self.n = n
            self.dists = [[None for x in range(n)] for y in range(n)]
            for i in range(len(coordinates)):
                coordinate = coordinates[i]
                if self.dists[coordinate[0]][coordinate[1]] is None:
                    self.dists[coordinate[0]][coordinate[1]] = coordinate[2]
                    self.dists[coordinate[1]][coordinate[0]] = self.dists[coordinate[0]][coordinate[1]]
            self.perm = [i for i in range(n)]

    # Complete as described in the spec, to calculate the cost of the
    # current tour (as represented by self.perm).
    def tourValue(self):
        cost = 0
        for i in range(self.n):
            cost += self.dists[self.perm[i % self.n]][self.perm[(i + 1) % self.n]]
        return cost

    # Attempt the swap of cities i and i+1 in self.perm and commit
    # commit to the swap if it improves the cost of the tour.
    # Return True/False depending on success.
    def trySwap(self, i):
        costBefore = self.tourValue()
        temp = self.perm[i]
        self.perm[i] = self.perm[(i + 1) % self.n]
        self.perm[(i + 1) % self.n] = temp
        costAfter = self.tourValue()
        if costAfter >= costBefore:
            temp = self.perm[i]
            self.perm[i] = self.perm[(i + 1) % self.n]
            self.perm[(i + 1) % self.n] = temp
            return False
        else:
            return True

    # Consider the effect of reversiing the segment between
    # self.perm[i] and self.perm[j], and commit to the reversal
    # if it improves the tour value.
    # Return True/False depending on success.              
    def tryReverse(self, i, j):
        costBefore = self.tourValue()
        if i == 0:
            self.perm[i: j + 1] = self.perm[j:: -1]
        else:
            self.perm[i: j + 1] = self.perm[j: i - 1: -1]
        costAfter = self.tourValue()
        if costAfter >= costBefore:
            if i == 0:
                self.perm[i: j + 1] = self.perm[j:: -1]
            else:
                self.perm[i: j + 1] = self.perm[j: i - 1: -1]
            return False
        else:
            return True

    def swapHeuristic(self, k):
        better = True
        count = 0
        while better and (count < k or k == -1):
            better = False
            count += 1
            for i in range(self.n):
                if self.trySwap(i):
                    better = True

    def TwoOptHeuristic(self, k):
        better = True
        count = 0
        while better and (count < k or k == -1):
            better = False
            count += 1
            for j in range(self.n - 1):
                for i in range(j):
                    if self.tryReverse(i, j):
                        better = True

    # Implement the Greedy heuristic which builds a tour starting
    # from node 0, taking the closest (unused) node as 'next'
    # each time.
    def Greedy(self):
        newPerm = [0]
        unvisited = [x for x in range(1, self.n)]
        index = 0
        while unvisited:
            distances = self.dists[index].copy()
            distance = self.dists[index].copy()
            minDis = min([x for x in distances if x is not None])
            index = self.dists[index].index(minDis)
            while index not in unvisited:
                distances.remove(minDis)
                distance[index] = None
                minDis = min([x for x in distances if x is not None])
                index = distance.index(minDis)
            newPerm.append(index)
            unvisited.remove(index)
        for i in range(self.n):
            self.perm[i] = newPerm[i]

    def CheapestInsertion(self, i, j):
        unvisited = [x for x in range(self.n) if x != i and x != j]
        # A list storing all existing edges
        currentEdges = [(i, j)]
        while len(currentEdges) < self.n - 1:
            # A list of 3-tuples storing all information about minimum increased cost in each round
            minIncreases = []
            for i in range(len(currentEdges)):
                currentEdge = currentEdges[i]
                currentCost = self.dists[currentEdge[0]][currentEdge[1]]
                candidate = ()
                # The minimum increased cost in current round
                minIncrease = None
                for j in range(len(unvisited)):
                    costIncreased = 0
                    vertexToBeUsed = unvisited[j]
                    edgeAdded1 = (currentEdge[0], vertexToBeUsed)
                    edgeAdded2 = (vertexToBeUsed, currentEdge[1])
                    # As only the path connects the vertex to itself doesn't exist
                    # We can ignore the None values
                    costIncreased = self.dists[edgeAdded1[0]][edgeAdded1[1]] + \
                                    self.dists[edgeAdded2[0]][edgeAdded2[1]] - \
                                    currentCost
                    if minIncrease is None or costIncreased < minIncrease:
                        minIncrease = costIncreased
                        # Storing the current minimum cost information in this round
                        candidate = (currentEdge, vertexToBeUsed, minIncrease)
                minIncreases.append(candidate)
            # Over the candidates, extract the one with the minimum cost
            absoluteMini = min([m[2] for m in minIncreases])
            # Get the index in all candidates
            index = [m[2] for m in minIncreases].index(absoluteMini)
            # Then get all the information, and change the tour by adding and deleting
            # corresponding edges. And update the unvisited vertices
            edgeToBeDeleted = minIncreases[index][0]
            vertexToBeUsed = minIncreases[index][1]
            currentEdges.remove(edgeToBeDeleted)
            unvisited.remove(vertexToBeUsed)
            currentEdges.insert(index, (edgeToBeDeleted[0], vertexToBeUsed))
            currentEdges.insert(index + 1, (vertexToBeUsed, edgeToBeDeleted[1]))
        # At last, change the tour based on the algorithm result
        for a in range(self.n - 1):
            self.perm[a] = currentEdges[a][0]
        self.perm[-1] = (currentEdges[-1][1])
