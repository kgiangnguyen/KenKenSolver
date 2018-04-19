import itertools

examplePuzzle = {("C1", 2, "") : [(1,1)], ("C2", 18, "*") : [(1,2),(1,3),(2,3),(3,3)],
                 ("C3", 2, "-") : [(2,1),(2,2)], ("C4", 2, "/") : [(3,1),(3,2)]}

goalPuzzle = {(1,1):None, (1,2):None, (1,3):None, (2,1):None, (2,2):None, (2,3):None, (3,1):None, (3,2):None, (3,3):None}


def backTracking(puzzle):
    if isComplete(goalPuzzle):
        return goalPuzzle
    else:
        cell = selectEmptyCell(puzzle)
        for value in cellDomain[cell]:
            goalPuzzle[cell] = value
            if checkConstraints(cell, puzzle):
                result = backTracking(puzzle)
                if result != "":
                    return result
            goalPuzzle[cell] = None
    return ""


def checkConstraints(cell, puzzle):
    return isUnique(cell) and isCorrect(puzzle)


def isUnique(cell):
    neighbors = findNeighbors(cell)
    for neighbor in neighbors:
        if goalPuzzle[neighbor] == goalPuzzle[cell]:
            return False
    return True


def isCorrect(puzzle):
    for cage in puzzle:
        target = cage[1]
        operation = cage[2]
        cells = puzzle[cage]
        cellValueList = []
        for cell in cells:
            cellValueList.append(goalPuzzle[cell])
        if operation == "+":
            return sum(cellValueList) == target
        elif operation == "*":
            multiply = 1
            for value in cellValueList:
                multiply *= value
            return multiply == target
        elif operation == "-":
            # print(cellValueList)
            return abs(cellValueList[0] - cellValueList[1]) == target
        elif operation == "/":
            return (max(cellValueList) / min(cellValueList)) == target
        else:
            return cellValueList[0] == target


def selectEmptyCell(puzzle):
    # Find the next cell which has the smallest domain to track. Set minSizeDomain to sqrSize+1 to make sure all domains
    # are considered.
    minSizeDomain = sqrSize+1
    nextCell = ()
    for cell, domain in cellDomain.items():
        if len(domain) < minSizeDomain and goalPuzzle[cell] is None:
            nextCell = cell
            minSizeDomain = len(domain)
    return nextCell


def isComplete(puzzle):
    for cell in goalPuzzle:
        if goalPuzzle[cell] is None:
            return False
    return True


def generateCellDomain(puzzle):
    for cage in puzzle:
        cells = puzzle[cage]
        for cell in cells:
            cellDomain[cell] = cageDomain[cage]
    return cellDomain


def findNeighbors(cell):
    neighbors = []
    for col in range(1, sqrSize+1):
        potentialNeighbor = (cell[0], col)
        if potentialNeighbor != cell and potentialNeighbor not in neighbors:
            neighbors.append(potentialNeighbor)
    for row in range(1, sqrSize+1):
        potentialNeighbor = (row, cell[1])
        if potentialNeighbor != cell and potentialNeighbor not in neighbors:
            neighbors.append(potentialNeighbor)
    return neighbors


def generateCageDomain(puzzle):
    for cage in puzzle:
        cageDomain[cage] = set()
        target = cage[1]
        operation = cage[2]
        count = len(puzzle[cage])
        combinations = itertools.combinations_with_replacement(domain, count)
        for comb in combinations:
            domainSet = set()
            if operation in ["+", "*", ""]:
                sumMul = 0 if operation == "+" else 1
                for value in comb:
                    if operation == "+":
                        sumMul += value
                    elif operation == "*":
                        sumMul *= value
                    else:
                        sumMul = value
                    if value not in domainSet:
                        domainSet.add(value)
                if (sumMul == target and operation in ["+", "*", ""]):
                    for value in domainSet:
                        cageDomain[cage].add(value)
            else:
                if operation == "-":
                    subDiv = abs(comb[0] - comb[1])
                else:
                    subDiv = max(comb[0], comb[1]) / min(comb[0], comb[1])
                if subDiv == target:
                    for value in comb:
                        cageDomain[cage].add(value)

    return cageDomain


def getMax(puzzle):
    max = 0
    for cage in puzzle:
        cells = puzzle[cage]
        for i in range(0, len(cells)):
            cell = cells[i]
            if cell[0] > max:
                max = cell[0]
            elif cell[1] > max:
                max = cell[1]
    return max


cellDomain = {}
cageDomain = {}
sqrSize = getMax(examplePuzzle)
domain = list(range(1,sqrSize+1))
generateCageDomain(examplePuzzle)
generateCellDomain(examplePuzzle)
print(backTracking(examplePuzzle))