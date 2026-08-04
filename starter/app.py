from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    clues = request.args.get('clues')
    difficulty = request.args.get('difficulty')
    if clues is None:
        puzzle, solution = sudoku_logic.generate_puzzle(difficulty=difficulty)
    else:
        puzzle, solution = sudoku_logic.generate_puzzle(clues=int(clues), difficulty=difficulty)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle})

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    puzzle = CURRENT.get('puzzle')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    if puzzle is None:
        return jsonify({'error': 'No game in progress'}), 400

    board = [row[:] for row in board]
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if puzzle[i][j] != sudoku_logic.EMPTY:
                board[i][j] = puzzle[i][j]

    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})


@app.route('/hint', methods=['POST'])
def get_hint():
    data = request.json or {}
    board = data.get('board')
    solution = CURRENT.get('solution')
    puzzle = CURRENT.get('puzzle')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    if puzzle is None:
        return jsonify({'error': 'No game in progress'}), 400
    if board is None:
        return jsonify({'error': 'Invalid board'}), 400
    if len(board) != sudoku_logic.SIZE:
        return jsonify({'error': 'Invalid board'}), 400
    for row in board:
        if len(row) != sudoku_logic.SIZE:
            return jsonify({'error': 'Invalid board'}), 400

    board = [row[:] for row in board]
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if puzzle[i][j] != sudoku_logic.EMPTY:
                board[i][j] = puzzle[i][j]

    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] == sudoku_logic.EMPTY:
                return jsonify({'row': i, 'col': j, 'value': solution[i][j]})
    return jsonify({'error': 'No empty cells remaining'}), 400


if __name__ == '__main__':
    app.run(debug=True)