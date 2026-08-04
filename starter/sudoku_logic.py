import copy
import random

SIZE = 9
EMPTY = 0
DIFFICULTY_CLUES = {
    'easy': 45,
    'medium': 35,
    'hard': 27,
}


def deep_copy(board):
    return copy.deepcopy(board)


def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


def count_solutions(board, limit=2):
    def backtrack(board):
        for row in range(SIZE):
            for col in range(SIZE):
                if board[row][col] == EMPTY:
                    solutions = 0
                    for num in range(1, SIZE + 1):
                        if is_safe(board, row, col, num):
                            board[row][col] = num
                            solutions += backtrack(board)
                            board[row][col] = EMPTY
                            if solutions >= limit:
                                return solutions
                    return solutions
        return 1

    return backtrack(deep_copy(board))


def remove_cells(board, clues):
    attempts = SIZE * SIZE - clues
    while attempts > 0:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        if board[row][col] != EMPTY:
            board[row][col] = EMPTY
            attempts -= 1


def resolve_clues(clues=None, difficulty=None):
    if clues is not None:
        return clues
    difficulty_name = (difficulty or 'medium').lower()
    return DIFFICULTY_CLUES.get(difficulty_name, DIFFICULTY_CLUES['medium'])


def generate_puzzle(clues=None, difficulty=None):
    clues = resolve_clues(clues=clues, difficulty=difficulty)
    while True:
        board = create_empty_board()
        fill_board(board)
        if board[0][0] == 9:
            continue
        solution = deep_copy(board)
        remove_cells(board, clues)
        puzzle = deep_copy(board)
        if count_solutions(puzzle) == 1:
            return puzzle, solution
