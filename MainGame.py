import itertools

examplePuzzle = {("C1", 2, "") : [(1,1)], ("C2", 18, "*") : [(1,2),(1,3),(2,3),(3,3)],
                 ("C3", 2, "-") : [(2,1),(2,2)], ("C4", 2, "/") : [(3,1),(3,2)]}

goalPuzzle = {(1,1):None, (1,2):None, (1,3):None, (2,1):None, (2,2):None, (2,3):None, (3,1):None, (3,2):None, (3,3):None}


def backTracking(puzzle, cellDomain):
    if isComplete(goalPuzzle):
        return goalPuzzle
    else:
        cell = selectEmptyCell(puzzle, cellDomain)
        print(cell)
        for value in cellDomain[cell]:
            if checkConstraints(cell, puzzle):
                result = backTracking(puzzle, cellDomain)
                if result != "":
                    return result
            goalPuzzle[cell] = 0
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
        cells = puzzle[cage]
        if cage[2] == "+":
            total = 0
            for cell in cells:
                total += goalPuzzle[cell]
            if total != cage[1]:
                return False
        if cage[2] == "x":
            total = 1
            for cell in cells:
                total *= goalPuzzle[cell]
            if total != cage[1]:
                return False
        if cage[2] == "-":
            firstNum = cells[0]
            secondNum = cells[1]
            if (firstNum-secondNum != cage[1]) or (secondNum-firstNum != cage[1]):
                return False
        if cage[2] == "/":
            firstNum = cells[0]
            secondNum = cells[1]
            if (firstNum/secondNum != cage[1]) or (secondNum/firstNum != cage[1]):
                return False
    return True


def selectEmptyCell(puzzle, cellDomain):
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


def generateCellDomain(puzzle, cellDomain):
    # Generate domain for each empty cell
    for cage in puzzle:
        cells = puzzle[cage]
        for cell in cells:

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


# TODO: Debug
def generateCageDomain(puzzle):
    for cage in puzzle:
        target = cage[1]
        operation = cage[2]
        count = len(puzzle[cage])
        combinations = itertools.combinations_with_replacement(domain, count)
        domainSet = set()
        for comb in combinations:
            total = 0 if operation == "+" else 1
            subDiv = target
            for value in comb:
                if operation == "+":
                    total += value
                elif operation == "-":
                    subDiv -= value
                elif operation == "x":
                    total *= value
                elif operation == "/":
                    subDiv /= value
                else:
                    total = value
                if value not in domainSet:
                    domainSet.add(value)
            if (total == target and operation in ["+", "x"]) or (subDiv == 0 and operation == "-") or (subDiv == 1 and operation == "/"):
                cageDomain[cage] = domainSet



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
# print(findNeighbors((1,1)))
generateCellDomain(examplePuzzle, cellDomain)
print(selectEmptyCell(examplePuzzle, cellDomain))
# print(backTracking(examplePuzzle, cellDomain))