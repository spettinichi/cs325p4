
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
    """ calulate length of tour """
    tourLength = calcTourLength(adjacencyList, distanceMatrix)
    """print("calculated tour length")"""

    """ write results to file """
    writeToFile(fileName, tourLength, adjacencyList)

    """ end time """
    print("%s seconds" % (time.time() - startTime))

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

def nearestInt(aNumber):
    fractNum, intNum = math.modf(aNumber)
    if fractNum >= 0.5:
        nearInt = math.ceil(aNumber)
    else:
        nearInt = math.floor(aNumber)
    return int(nearInt)

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

def readInFile(fileName):
    vertices = []
    with open(fileName, 'r') as fileD:
        for line in fileD:
            lineList = line.split()
            vertices.append([int(lineList[1]), int(lineList[2])])
    return vertices


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
    
if __name__ == "__main__":
    main(sys.argv)
