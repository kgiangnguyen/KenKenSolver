import sys
import queue
import copy

# Constant
LIST_ROW = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]


def read_input(domain_for_cell, board):
    input_string = sys.argv[1]
    index_assignment = 0
    for row in LIST_ROW:
        for col in range(1, 10, 1):
            board[row+str(col)] = int(input_string[index_assignment])
            domain_for_cell[row+str(col)] = []
            index_assignment += 1


def ac3(board, domain_for_cell):
    # Generate all constraints of the sudoku board
    arcs_queue = generate_all_arcs()

    while not arcs_queue.empty():
        a_constraint = arcs_queue.get_nowait()
        # A constraint has the form "A1B1", with first 2 letters is first cell, and the last 2 is second cell
        cell_1 = a_constraint[:2]
        cell_2 = a_constraint[2:]
        if revise(domain_for_cell, cell_1, cell_2):
            if len(domain_for_cell[cell_1]) == 0:
                print(a_constraint)
                return False
            else:
                for neighbor in find_neighbor(cell_1):
                    if neighbor != cell_2:
                        arcs_queue.put_nowait(neighbor+cell_1)
    return True


def revise(domain_for_cell, cell_1, cell_2):
    revised = False
    # There is no need to check if any of the domain of cell1 or cell2 is empty
    if len(domain_for_cell[cell_1]) != 0 and len(domain_for_cell[cell_2]) != 0:
        # Loop through all possible value in domain of cell1
        for value in domain_for_cell[cell_1]:
            satisfy = False
            # There must be at least one value in domain of cell2 that is different from "value"
            for value2 in domain_for_cell[cell_2]:
                if value2 != value:
                    satisfy = True
            if not satisfy:
                revised = True
                domain_for_cell[cell_1].remove(value)
    return revised


def generate_all_arcs():
    arcs_queue = queue.Queue()
    # Create all the horizontal constraints
    for row in LIST_ROW:
        list_cell = []
        for col in range(1, 10, 1):
            list_cell.append(row+str(col))
        for cell in list_cell:
            for another_cell in list_cell:
                if another_cell != cell:
                    arcs_queue.put_nowait(cell+another_cell)
    # Create all the vertical constraints
    for col in range(1, 10, 1):
        list_cell = []
        for row in LIST_ROW:
            list_cell.append(row+str(col))
        for cell in list_cell:
            for another_cell in list_cell:
                if another_cell != cell:
                    arcs_queue.put_nowait(cell+another_cell)
    # Create all the square constraints
    for index_row in [0, 3, 6]:
        # Get every-3 letters from the LIST_ROW
        rows = [LIST_ROW[index_row], LIST_ROW[index_row+1], LIST_ROW[index_row+2]]
        for index_col in [1, 4, 7]:
            # Get every 3-numbers from 1 to 9
            cols = [index_col, index_col+1, index_col+2]
            list_cell = []
            # Generate all the cells created by those 3 letters and 3 numbers
            for row in rows:
                for col in cols:
                    list_cell.append(row+str(col))
            for cell in list_cell:
                for another_cell in list_cell:
                    if another_cell != cell:
                        arcs_queue.put_nowait(cell+another_cell)

    return arcs_queue


def find_neighbor(cell):
    neighbors = []
    cell_row = cell[0]
    cell_col = int(cell[1])
    # Generate neighbors in square
    rows = []
    index = None
    if cell_row in LIST_ROW[:3]:
        rows = LIST_ROW[:3]
    elif cell_row in LIST_ROW[3:6]:
        rows = LIST_ROW[3:6]
    else:
        rows = LIST_ROW[6:]
    if cell_col/3 <= 1:
        index = 1
    elif cell_col/3 <= 2:
        index = 4
    else:
        index = 7
    for row in rows:
        for col in range(index, index+3):
            potential_neighbor = row+str(col)
            if potential_neighbor != cell and potential_neighbor not in neighbors:
                neighbors.append(potential_neighbor)
    # Generate neighbors horizontally
    for col in range(1, 10, 1):
        potential_neighbor = cell_row+str(col)
        if potential_neighbor != cell and potential_neighbor not in neighbors:
            neighbors.append(potential_neighbor)
    # Generate neighbors vertically
    for row in LIST_ROW:
        potential_neighbor = row+cell[1]
        if potential_neighbor != cell and potential_neighbor not in neighbors:
            neighbors.append(potential_neighbor)
    return neighbors


def generate_domain_for_cell(domain_for_cell, board):
    domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for cell in board.keys():
        if board[cell] == 0:
            neighbors = find_neighbor(cell)
            taken_value = set()
            for neighbor in neighbors:
                if board[neighbor] != 0:
                    taken_value.add(board[neighbor])
            for value in domain:
                if value not in taken_value:
                    domain_for_cell[cell].append(value)
        else:
            domain_for_cell[cell] = []
    return domain_for_cell


def solved_by_ac3(board, domain_for_cell):
    if ac3(board, domain_for_cell):
        output_string = ""
        for row in LIST_ROW:
            for col in range(1, 10, 1):
                cell = row + str(col)
                domain = domain_for_cell[cell]
                if len(domain) > 1:
                    return ""
                elif len(domain) == 1:
                    output_string += str(domain[0])
                else:
                    output_string += str(board[cell])
        return output_string
    else:
        return ""


def back_tracing_search(board, domain_for_cell):
    return backtrack(board, domain_for_cell)


def backtrack(board, domain_for_cell):
    if is_completed(board):
        return print_assignment(board)
    else:
        cell = select_unassigned_variable(board, domain_for_cell)
    for value in domain_for_cell[cell]:
        board[cell] = value
        if is_consistent(cell, board):
            result = backtrack(board, domain_for_cell)
            if result != "":
                return result
        board[cell] = 0
    return ""


def is_consistent(cell, board):
    neighbors = find_neighbor(cell)
    for neighbor in neighbors:
        if board[neighbor] == board[cell]:
            return False
    return True


def select_unassigned_variable(board, domain_for_cell):
    min_size_domain = 10
    next_cell = ""
    for cell, domain in domain_for_cell.items():
        # If board[cell] != 0, it means that cell is assigned already.
        if len(domain) < min_size_domain and board[cell] == 0:
            next_cell = cell
            min_size_domain = len(domain)
    return next_cell


def is_completed(board):
    for row in LIST_ROW:
        for col in range(1, 10, 1):
            if board[row+str(col)] == 0:
                return False
    return True


def print_assignment(board):
    output_string = ""
    for row in LIST_ROW:
        for col in range(1, 10, 1):
            output_string += str(board[row+str(col)])
    return output_string


def print_to_file(output_string):
    file_out = open("output.txt", "w")
    file_out.write(output_string)
    file_out.close()


def solve_sudoku():
    domain_for_cell = {}
    board = {}
    read_input(domain_for_cell, board)
    generate_domain_for_cell(domain_for_cell, board)
    # Make a deep copy of board and domain_for_cell for each of the method
    board_bst = copy.deepcopy(board)
    domain_for_cell_bst = copy.deepcopy(domain_for_cell)
    output_ac3 = solved_by_ac3(board, domain_for_cell)
    if output_ac3 != "":
        # print(output_ac3 + " AC3")
        return output_ac3 + " AC3"
    else:
        # print(back_tracing_search(board_bst, domain_for_cell_bst) + " BTS")
        return back_tracing_search(board_bst, domain_for_cell_bst) + " BTS"


def main():
    print_to_file(solve_sudoku())

main()