import itertools

def backTracking():
    if isComplete():
        return goalPuzzle
    else:
        cell = selectEmptyCell()
        for value in cellDomain[cell]:
            goalPuzzle[cell] = value
            if checkConstraints(cell, examplePuzzle2):
                result = backTracking()
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
        print(cage)
        target = cage[1]
        operation = cage[2]
        cells = puzzle[cage]
        isFull = True
        cellValueList = []

        for cell in cells:
            value = goalPuzzle[cell]
            if value == None:
                isFull = False
                break
            cellValueList.append(value)
            # print("==>", cellValueList)

        if isFull:
            print("=========")
            if operation == "+":
                print("==========>", cellValueList)
                return sum(cellValueList) == target
            elif operation == "*":
                multiply = 1
                for value in cellValueList:
                    # print(value)
                    multiply *= value
                return multiply == target
            elif operation == "-":
                return abs(cellValueList[0] - cellValueList[1]) == target
            elif operation == "/":
                return (max(cellValueList) / min(cellValueList)) == target
            else:
                return cellValueList[0] == target

    return True

def selectEmptyCell():
    # Find the next cell which has the smallest domain to track. Set minSizeDomain to sqrSize+1 to make sure all domains
    # are considered.
    minSizeDomain = sqrSize+1
    nextCell = ()
    for cell, domain in cellDomain.items():
        if len(domain) < minSizeDomain and goalPuzzle[cell] is None:
            nextCell = cell
            minSizeDomain = len(domain)
    return nextCell


def isComplete():
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


if __name__ == '__main__':
    examplePuzzle = {("C1", 2, ""): [(1, 1)], ("C2", 18, "*"): [(1, 2), (1, 3), (2, 3), (3, 3)],
                     ("C3", 2, "-"): [(2, 1), (2, 2)], ("C4", 2, "/"): [(3, 1), (3, 2)]}

    examplePuzzle2 = {("C1", 6, "*"): [(1, 1), (1, 2), (2, 1)], ("C2", 2, "/"): [(1, 3), (1, 4)],
                      ("C3", 3, "-"): [(2, 2), (2, 3)], ("C4", 1, "-"): [(2, 4), (3, 4)],
                      ("C5", 7, "+"): [(3, 1), (4, 1), (4, 2)], ("C6", 5, "+"): [(3, 2), (3, 3)],
                      ("C7", 4, "+"): [(4, 3), (4, 4)]}

    # goalPuzzle = {(1, 1): None, (1, 2): None, (1, 3): None, (1, 4): None, (2, 1): None, (2, 2): None, (2, 3): None,
    #               (2, 4): None,
    #               (3, 1): None, (3, 2): None, (3, 3): None, (3, 4): None, (4, 1): None, (4, 2): None, (4, 3): None,
    #               (4, 4): None}

    cellDomain = {}
    cageDomain = {}
    sqrSize = getMax(examplePuzzle2)
    domain = list(range(1,sqrSize+1))
    generateCageDomain(examplePuzzle2)
    generateCellDomain(examplePuzzle2)
    # print(backTracking())

    goalPuzzle = {(1, 2): 1, (3, 2): 2, (1, 3): 4, (3, 3): 3, (4, 1): 4, (3, 1): 1, (4, 4): 1, (1, 4): 2, (2, 4): 3, (2, 3): 1, (2, 1): 2, (4, 3): 2, (2, 2): 4, (4, 2): 3, (3, 4): 4, (1, 1): 3}
    print(isCorrect(examplePuzzle2))
