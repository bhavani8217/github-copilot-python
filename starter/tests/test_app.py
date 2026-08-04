from app import CURRENT


def test_index_returns_html(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.mimetype == 'text/html'


def test_new_game_returns_nine_by_nine_puzzle(client):
    response = client.get('/new?clues=35')

    assert response.status_code == 200
    data = response.get_json()

    assert 'puzzle' in data
    puzzle = data['puzzle']
    assert len(puzzle) == 9
    assert all(len(row) == 9 for row in puzzle)


def test_new_game_supports_difficulty_query_parameter(client):
    response = client.get('/new?difficulty=easy')

    assert response.status_code == 200
    data = response.get_json()
    puzzle = data['puzzle']

    assert len(puzzle) == 9
    assert all(len(row) == 9 for row in puzzle)
    assert sum(cell != 0 for row in puzzle for cell in row) == 45


def test_check_solution_returns_empty_incorrect_list_for_correct_board(client):
    client.get('/new?clues=35')
    solution = CURRENT['solution']

    response = client.post('/check', json={'board': solution})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': []}


def test_check_solution_reports_wrong_cells(client):
    client.get('/new?clues=35')
    puzzle = [row[:] for row in CURRENT['puzzle']]
    solution = CURRENT['solution']
    row = 0
    col = 0
    while puzzle[row][col] != 0:
        row = (row + 1) % 9
        col = (col + 1) % 9

    board = [row[:] for row in solution]
    board[row][col] = 9

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': [[row, col]]}


def test_check_solution_without_game_returns_error(client):
    response = client.post('/check', json={'board': [[0] * 9 for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_hint_returns_one_correct_value_for_an_empty_cell(client):
    client.get('/new?clues=35')
    board = [row[:] for row in CURRENT['puzzle']]
    solution = CURRENT['solution']

    response = client.post('/hint', json={'board': board})

    assert response.status_code == 200
    data = response.get_json()
    assert data['row'] >= 0 and data['row'] < 9
    assert data['col'] >= 0 and data['col'] < 9
    assert board[data['row']][data['col']] == 0
    assert data['value'] == solution[data['row']][data['col']]
    assert data['value'] != 0


def test_check_solution_ignores_mutations_to_original_clue_cells(client):
    client.get('/new?clues=35')
    solution = CURRENT['solution']
    puzzle = [row[:] for row in CURRENT['puzzle']]

    row = 0
    col = 0
    while puzzle[row][col] == 0:
        row = (row + 1) % 9
        col = (col + 1) % 9

    board = [row[:] for row in solution]
    board[row][col] = puzzle[row][col] + 1

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    data = response.get_json()
    assert [row, col] not in data['incorrect']


def test_hint_restores_original_clue_cells_before_searching_for_an_empty_cell(client):
    client.get('/new?clues=35')
    puzzle = [row[:] for row in CURRENT['puzzle']]
    solution = CURRENT['solution']

    row = 0
    col = 0
    while puzzle[row][col] == 0:
        row = (row + 1) % 9
        col = (col + 1) % 9

    board = [row[:] for row in puzzle]
    board[row][col] = 0

    response = client.post('/hint', json={'board': board})

    assert response.status_code == 200
    data = response.get_json()
    assert (data['row'], data['col']) != (row, col)
    assert data['value'] == solution[data['row']][data['col']]


def test_hint_does_not_alter_cells_that_are_already_filled(client):
    client.get('/new?clues=35')
    board = [row[:] for row in CURRENT['puzzle']]
    solution = CURRENT['solution']

    row = 0
    col = 0
    while board[row][col] != 0:
        row = (row + 1) % 9
        col = (col + 1) % 9

    board[row][col] = 9
    original_board = [row[:] for row in board]

    response = client.post('/hint', json={'board': board})

    assert response.status_code == 200
    data = response.get_json()
    assert data['row'] != row or data['col'] != col
    assert board == original_board
    assert data['value'] == solution[data['row']][data['col']]
