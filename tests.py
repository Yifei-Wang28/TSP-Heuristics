import time
import random
import graph

"""
Generate a table of coordinates in Euclidean setting
"""
def euclideanCoordinates(lowerb, higherb, size):
    coordinates = []
    for i in range(size):
        (a, b) = (random.randint(lowerb, higherb), random.randint(lowerb, higherb))
        # Avoid giving same coordinates
        while (a, b) in coordinates:
            (a, b) = (random.randint(lowerb, higherb), random.randint(lowerb, higherb))
        coordinates.append((a, b))
    return coordinates


def euclideanGenerator(lowerb, higherb, size):
    coordinates = euclideanCoordinates(lowerb, higherb, size)
    f = open('s2106632', 'w')
    for j in range(size):
        f.writelines(str(coordinates[j][0]) + '  ' + str(coordinates[j][1]))
        f.writelines('\n')
    f.close()


"""
A helper method used to check if the metric graph is indeed metric
"""
def checkTriangle(distanceTable):
    valid = True
    for i in range(len(distanceTable) - 2):
        for j in range(i + 1, len(distanceTable) - 1):
            for k in range(j + 1, len(distanceTable)):
                # check if three sides fulfill the triangle inequality
                triangle1 = distanceTable[i][j] + distanceTable[j][k] >= distanceTable[i][k]
                triangle2 = distanceTable[i][j] + distanceTable[i][k] >= distanceTable[j][k]
                triangle3 = distanceTable[i][k] + distanceTable[j][k] >= distanceTable[i][j]
                valid = valid and triangle1 and triangle2 and triangle3
    return valid


"""
Randomly generate distances for a metric graph through given limits
"""
def metricCoordinates(size, limDistance):
    distanceTable = [[None for x in range(size)] for y in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            lowerBound = []
            higherBound = []
            for k in range(i):
                # check all existed related triangles and get their lower bounds and higher bounds
                higherBound.append(distanceTable[k][i] + distanceTable[k][j])
                lowerBound.append(abs(distanceTable[k][i] - distanceTable[k][j]))
            # If there is any element in lower bound or higher bound, then use the bound
            # as restrictions to randomly give values
            if lowerBound or higherBound:
                # we must get the union of all bounds, therefore the biggest lower bound
                # and the smallest higher bound union our own restriction is the final bounds
                distanceTable[i][j] = random.randint(max([max(lowerBound), 1]), min([min(higherBound), limDistance]))
                distanceTable[j][i] = distanceTable[i][j]
            # If there's no calculated bounds at all, then in our defined bound
            # randomly choose numbers
            else:
                distanceTable[i][j] = random.randint(1, limDistance)
                distanceTable[j][i] = distanceTable[i][j]
    return distanceTable


def metricGenerator(size, limDistance):
    distanceTable = metricCoordinates(size, limDistance)
    f = open('s2106632', 'w')
    for i in range(size - 1):
        for j in range(i + 1, size):
            f.writelines(str(i) + ' ' + str(j) + ' ' + str(distanceTable[i][j]))
            f.writelines('\n')
    f.close()


# g = graph.Graph(50, 's2106632')
# print(g.tourValue())
#
# t0 = time.time()
# for i in range(10):
#     g = graph.Graph(50, 's2106632')
#     g.swapHeuristic(50)
#     # print(g.tourValue())
# print((time.time() - t0) / 10)
# print(g.tourValue())
# print('\n')

# t0 = time.time()
# for i in range(10):
#     g = graph.Graph(50, 's2106632')
#     g.TwoOptHeuristic(50)
# # print(g.tourValue())
# print((time.time() - t0) / 10)
# print('\n')
#
# t0 = time.time()
# for i in range(10):
#     g = graph.Graph(50, 's2106632')
#     g.Greedy()
# # print(g.tourValue())
# print((time.time() - t0) / 10)
# print('\n')
#
# t0 = time.time()
# minimum = None
# g = graph.Graph(50, 's2106632')
# for i in range(50):
#     for j in range(i + 1, 50):
#         g.perm = [x for x in range(g.n)]
#         g.CheapestInsertion(i, j)
#         cost = g.tourValue()
#         if minimum is None or cost < minimum:
#             minimum = cost
# # print(minimum)
# print(time.time() - t0)

# euclideanGenerator(50, 1000, 100)
# metricCoordinates(50, 100)
