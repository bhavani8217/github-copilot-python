import sudoku_logic


def count_solutions(board, limit=2):
    def is_valid(board, row, col, num):
        for x in range(sudoku_logic.SIZE):
            if board[row][x] == num or board[x][col] == num:
                return False
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if board[r][c] == num:
                    return False
        return True

    def backtrack(board):
        for row in range(sudoku_logic.SIZE):
            for col in range(sudoku_logic.SIZE):
                if board[row][col] == sudoku_logic.EMPTY:
                    solutions = 0
                    for num in range(1, sudoku_logic.SIZE + 1):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            solutions += backtrack(board)
                            board[row][col] = sudoku_logic.EMPTY
                            if solutions >= limit:
                                return solutions
                    return solutions
        return 1

    return backtrack([row[:] for row in board])


def is_valid_sudoku_board(board):
    for row in board:
        if sorted(row) != list(range(1, 10)):
            return False

    for col in range(sudoku_logic.SIZE):
        column_values = [board[row][col] for row in range(sudoku_logic.SIZE)]
        if sorted(column_values) != list(range(1, 10)):
            return False

    for box_row in range(0, sudoku_logic.SIZE, 3):
        for box_col in range(0, sudoku_logic.SIZE, 3):
            box_values = []
            for row in range(box_row, box_row + 3):
                for col in range(box_col, box_col + 3):
                    box_values.append(board[row][col])
            if sorted(box_values) != list(range(1, 10)):
                return False

    return True


def test_create_empty_board_returns_nine_by_nine_grid():
    board = sudoku_logic.create_empty_board()

    assert len(board) == 9
    assert all(len(row) == 9 for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_generate_puzzle_returns_full_solution_and_shape():
    puzzle, solution = sudoku_logic.generate_puzzle(35)

    assert len(puzzle) == 9
    assert len(solution) == 9
    assert all(len(row) == 9 for row in puzzle)
    assert all(len(row) == 9 for row in solution)


def test_generated_solution_is_a_valid_sudoku_board():
    _, solution = sudoku_logic.generate_puzzle(35)

    assert is_valid_sudoku_board(solution)


def test_puzzle_cells_match_solution_where_clues_exist():
    puzzle, solution = sudoku_logic.generate_puzzle(35)

    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            if puzzle[row][col] != sudoku_logic.EMPTY:
                assert puzzle[row][col] == solution[row][col]


def test_generated_puzzle_has_exactly_one_unique_solution():
    puzzle, _ = sudoku_logic.generate_puzzle(35)

    assert count_solutions(puzzle) == 1


def count_clues(board):
    return sum(cell != sudoku_logic.EMPTY for row in board for cell in row)


def test_difficulty_levels_change_puzzle_clue_counts():
    easy_puzzle, _ = sudoku_logic.generate_puzzle(difficulty='easy')
    medium_puzzle, _ = sudoku_logic.generate_puzzle(difficulty='medium')
    hard_puzzle, _ = sudoku_logic.generate_puzzle(difficulty='hard')

    assert count_clues(easy_puzzle) == 45
    assert count_clues(medium_puzzle) == 35
    assert count_clues(hard_puzzle) == 27
    assert count_clues(easy_puzzle) > count_clues(medium_puzzle) > count_clues(hard_puzzle)


def test_generated_puzzle_has_exactly_one_unique_solution_for_all_difficulties():
    for difficulty in ('easy', 'medium', 'hard'):
        puzzle, _ = sudoku_logic.generate_puzzle(difficulty=difficulty)

        assert count_solutions(puzzle) == 1
