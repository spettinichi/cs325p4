
import math
import sys
import time

def main(argv):
    """ start time """
    startTime = time.time()

    """ check command line parameters """
    if len(argv) < 2:
        sys.exit("USAGE: clarkeWright.py <file-name>")
    fileName = argv[1]

    """ read in file """
    vertices = readInFile(fileName)
    """print("file read in")"""

    """ choose hub node """
    numVertices = len(vertices)
    hubNode = numVertices/2

    """ initialize graph """
    adjacencyList = initializeGraph(numVertices, hubNode)
    """print("graph initialized")"""

    """ create distance matrix """
    distanceMatrix = createDistanceMatrix(vertices, numVertices)
    """print("distance matrix created")"""

    """ create savings list """
    savingsList = calculateSavings(distanceMatrix, hubNode, numVertices)
    """print("savings list created")"""

    """ take shortcuts until a Hamiltonian cycle is created """
    hamiltonian = False
    while hamiltonian is False:
        shortcut = savingsList.pop()
        shortcutSuccess = takeShortcut(adjacencyList, shortcut[1], shortcut[2], hubNode)
        if shortcutSuccess is True:
            goodTour = testGoodTour(adjacencyList, hubNode, shortcut[1])
            if goodTour is True:
                hamiltonian = checkHamiltonian(numVertices, adjacencyList)
            else:
                removeShortcut(adjacencyList, shortcut[1], shortcut[2], hubNode)

    """print("found hamiltonian")"""
    """ improve tour with 2-opt """
    twoOpt(adjacencyList, distanceMatrix)

    """ calulate length of tour """
    tourLength = calcTourLength(adjacencyList, distanceMatrix)
    """print("calculated tour length")"""

    """ write results to file """
    writeToFile(fileName, tourLength, adjacencyList)

    """ end time """
    print("%s seconds" % (time.time() - startTime))

"""
 "" Writes tour length and list of vertices in tour order to file.
 "" File is named <fileName>.tour
"""
def writeToFile(fileName, tourLength, adjacencyList):
    resultsFileName = fileName + ".tour"
    with open(resultsFileName, 'w') as fileD:
        fileD.write("{}".format(tourLength))
        fileD.write("\n")
        firstVertex = 0
        lastVertex = firstVertex
        currVertex = -1
        nextVertex = adjacencyList[firstVertex][0]
        tourLength = 0
        while currVertex != firstVertex:
            currVertex = nextVertex
            fileD.write("{}".format(currVertex))
            fileD.write("\n")
            if adjacencyList[currVertex][0] != lastVertex:
                nextVertex = adjacencyList[currVertex][0]
            else:
                nextVertex = adjacencyList[currVertex][1]
            lastVertex = currVertex

"""
 "" Removes a shortcut edge between vertices i and 
 "" j and replaces the edges between i and the 
 "" hubVertex and j and the hubVertex
"""
def removeShortcut(adjacencyList, i, j, hubVertex):
    if i in adjacencyList[j]:
        if j in adjacencyList[i]:
            adjacencyList[i].append(hubVertex)
            adjacencyList[j].append(hubVertex)
            adjacencyList[hubVertex].append(i)
            adjacencyList[hubVertex].append(j)
            adjacencyList[i].remove(j)
            adjacencyList[j].remove(i)
            return True
    return False

"""
 "" Adds a shortcut edge between vertices i and j
 "" and removes the edges between i and the 
 "" hubvertex and j and the hubVertex
 "" Returns True if the shortcut was successfully
 "" added, False if the shortcut couldn't be added
 "" because there weren't edges between the 
 "" hubVertex and each of i and j
"""
def takeShortcut(adjacencyList, i, j, hubVertex):
    if hubVertex in adjacencyList[i]:
        if hubVertex in adjacencyList[j]:
            adjacencyList[i].remove(hubVertex)
            adjacencyList[j].remove(hubVertex)
            adjacencyList[hubVertex].remove(i)
            adjacencyList[hubVertex].remove(j)
            adjacencyList[i].append(j)
            adjacencyList[j].append(i)
            return True
    return False

"""
 "" Tests the current graph to check that it is still
 "" connected (and would yield a complete tour)
"""
def testGoodTour(adjacencyList, hubVertex, changedVertex):
    if len(adjacencyList[hubVertex]) < 2:
        return False
    firstVertex = changedVertex
    lastVertex = firstVertex
    currVertex = -1
    nextVertex = adjacencyList[firstVertex][0]
    while currVertex != firstVertex:
        currVertex = nextVertex
        if currVertex == hubVertex:
            return True
        if adjacencyList[currVertex][0] != lastVertex:
            nextVertex = adjacencyList[currVertex][0]
        else:
            nextVertex = adjacencyList[currVertex][1]
        lastVertex = currVertex
    return False

"""
 "" Calculates the length (distance) of the current
 "" tour.
"""
def calcTourLength(adjacencyList, distanceMatrix):
    firstVertex = 0
    lastVertex = firstVertex
    currVertex = -1
    nextVertex = adjacencyList[firstVertex][0]
    tourLength = 0
    while currVertex != firstVertex:
        currVertex = nextVertex
        if lastVertex > currVertex:
            thisEdge = distanceMatrix[currVertex][lastVertex]
        else:
            thisEdge = distanceMatrix[lastVertex][currVertex]
        tourLength += thisEdge
        if adjacencyList[currVertex][0] != lastVertex:
            nextVertex = adjacencyList[currVertex][0]
        else:
            nextVertex = adjacencyList[currVertex][1]
        lastVertex = currVertex
    return tourLength

"""
 "" Initializes the graph to contain two edges
 "" between each vertex and the hubVertex
"""
def initializeGraph(numVertices, hubVertex):
    adjacencyList = []
    for k in range(0, numVertices):
        adjacencyList.append([])
    for i in range(0, numVertices):
        if i != hubVertex:
            adjacencyList[i].append(hubVertex)
            adjacencyList[i].append(hubVertex)
            adjacencyList[hubVertex].append(i)
            adjacencyList[hubVertex].append(i)
    return adjacencyList

"""
 "" Returns the nearest int to the passed-in float
"""
def nearestInt(aNumber):
    fractNum, intNum = math.modf(aNumber)
    if fractNum >= 0.5:
        nearInt = math.ceil(aNumber)
    else:
        nearInt = math.floor(aNumber)
    return int(nearInt)

"""
 "" Calculates the distance between each pair of 
 "" vertices and stores it in a matrix
"""
def createDistanceMatrix(vertices, numVertices):
    """ initialize matrix """
    distanceMatrix = []
    for v in range(0, numVertices):
        newRow = []
        for v2 in range(0, numVertices):
            newRow.append(0)
        distanceMatrix.append(newRow)
    """ calculate distances """
    for i in range(0, numVertices):
        for j in range(i, numVertices):
            if i != j:
                xdiff = vertices[i][0] - vertices[j][0]
                ydiff = vertices[i][1] - vertices[j][1]
                squaresum = math.pow(xdiff, 2) + math.pow(ydiff, 2)
                distance = math.sqrt(squaresum)
                distanceMatrix[i][j] = nearestInt(distance)
    return distanceMatrix

"""
 "" Calculates the savings for each pair of vertices 
 "" (excluding the hubVertex) and stores it in a list
 "" The savings is calculated as the length of the 
 "" edge (i, hubVertex) + the length of the edge (j, 
 "" hubvertex) - the length of the edge (i, j)
 "" Sorts the list of savings with the greatest savings
 "" at the bottom of the list
"""
def calculateSavings(distanceMatrix, hubVertex, numVertices):
    savingsList = []
    for i in range(0, numVertices):
        for j in range(i, numVertices):
            if (i != j) and (hubVertex != i) and (hubVertex != j):
                if hubVertex > i:
                    costHI = distanceMatrix[i][hubVertex]
                else:
                    costHI = distanceMatrix[hubVertex][i]
                if hubVertex > j:
                    costHJ = distanceMatrix[j][hubVertex]
                else:
                    costHJ = distanceMatrix[hubVertex][j]
                costIJ = distanceMatrix[i][j]
                savings = costHI + costHJ - costIJ
                savingsList.append([savings, i, j])
    savingsList.sort(key=lambda saving: saving[0])
    return savingsList

"""
 "" Reads in a file of vertices in format: ID, X, Y
 "" Returns a list of vertices with ID as the index,
 "" and [X, Y] as the value
"""
def readInFile(fileName):
    vertices = []
    with open(fileName, 'r') as fileD:
        for line in fileD:
            lineList = line.split()
            vertices.append([int(lineList[1]), int(lineList[2])])
    return vertices

"""
 "" Checks if the current graph contains a Hamiltonian
 "" cycle
"""
def checkHamiltonian(numVertices, adjacencyList):
    """ start at a vertex and walk until return to that vertex """
    """ as each vertex is visited, add to visited set """
    """ if at any point before returning to the start, a vertex cannot be added, then there isn't a Hamiltonian cycle """
    """ if reach the start, check that the visited set matches the complete vertex set """
    firstVertex = 0
    lastVertex = firstVertex
    currVertex = -1
    nextVertex = adjacencyList[firstVertex][0]
    visitedSet = set()
    while currVertex != firstVertex:
        currVertex = nextVertex
        if currVertex in visitedSet:
            return False
        else:
            visitedSet.add(currVertex)
        if adjacencyList[currVertex][0] != lastVertex:
            nextVertex = adjacencyList[currVertex][0]
        else:
            nextVertex = adjacencyList[currVertex][1]
        lastVertex = currVertex
    if len(visitedSet) == numVertices:
        return True
    else:
        return False

"""
 "" Completes a 2-OPT optimization to the graph,
 "" by checking each pair of edges to see if 
 "" swapping the edges decreases the tour length.
 "" Looks at the graph twice.
"""
def twoOpt(adjacencyList, distanceMatrix):
    for j in range(0, 2):
        for i in range(0, len(adjacencyList)):
            swap = False
            firstVertex = i
            lastVertex = firstVertex
            currVertex = adjacencyList[firstVertex][0]
            if adjacencyList[currVertex][0] != lastVertex:
                nextVertex = adjacencyList[currVertex][0]
            else:
                nextVertex = adjacencyList[currVertex][1]
            lastVertex = currVertex
            secondVertex = currVertex
            """ calculate distance of first edge """
            if firstVertex > secondVertex:
                firstEdge = distanceMatrix[secondVertex][firstVertex]
            else:
                firstEdge = distanceMatrix[firstVertex][secondVertex]
            """ travel around the cycle until either a swap is made or reach the beginning """
            while (nextVertex != firstVertex) and not swap:
                currVertex = nextVertex
                if adjacencyList[currVertex][0] != lastVertex:
                    nextVertex = adjacencyList[currVertex][0]
                else:
                    nextVertex = adjacencyList[currVertex][1]
                """ check if swap improves tour """
                """ find distance of second edge """
                if nextVertex > currVertex:
                    secondEdge = distanceMatrix[currVertex][nextVertex]
                else:
                    secondEdge = distanceMatrix[nextVertex][currVertex]
                """ find distances of edges that would be created if swap happened """
                if firstVertex > currVertex:
                    newFirstEdge = distanceMatrix[currVertex][firstVertex]
                else:
                    newFirstEdge = distanceMatrix[firstVertex][currVertex]
                if secondVertex > nextVertex:
                    newSecondEdge = distanceMatrix[nextVertex][secondVertex]
                else:
                    newSecondEdge = distanceMatrix[secondVertex][nextVertex]
                """ if swap improves tour, swap """
                """print("original: {}\n new: {}".format(firstEdge + secondEdge, newFirstEdge + newSecondEdge))"""
                if (firstEdge + secondEdge) > (newFirstEdge + newSecondEdge):
                    swapEdges(firstVertex, secondVertex, currVertex, nextVertex, adjacencyList)
                    swap = True
                lastVertex = currVertex

"""
 "" Swaps the edges (firstVertex, secondVertex) and (currVertex, nextVertex)
 "" for the edges (firstVertex, currVertex) and (secondVertex, nextVertex)
"""
def swapEdges(firstVertex, secondVertex, currVertex, nextVertex, adjacencyList):
    """ remove current edges """
    adjacencyList[firstVertex].remove(secondVertex)
    adjacencyList[secondVertex].remove(firstVertex)
    adjacencyList[currVertex].remove(nextVertex)
    adjacencyList[nextVertex].remove(currVertex)
    """ add new edges """
    adjacencyList[firstVertex].append(currVertex)
    adjacencyList[currVertex].append(firstVertex)
    adjacencyList[secondVertex].append(nextVertex)
    adjacencyList[nextVertex].append(secondVertex)

    
if __name__ == "__main__":
    main(sys.argv)
